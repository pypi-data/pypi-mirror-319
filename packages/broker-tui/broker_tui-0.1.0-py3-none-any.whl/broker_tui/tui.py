"""A Terminal User Interface (TUI) application for managing and interacting with Broker.

This module provides a text-based user interface built with the Textual library to manage
host inventories across different providers. It allows users to:

- View and filter host inventories
- Sync inventory data from providers
- Check in/out hosts
- View detailed host information
- Handle multiple providers

Classes:
    ProviderSync: Widget for provider selection and sync functionality
    InventoryTable: DataTable widget for displaying inventory data
    BrokerTUI: Main application class
    ErrorModal: Modal screen for displaying error messages
"""
import asyncio
import subprocess

from textual import work
from textual.app import App
from textual.containers import Container, Horizontal, HorizontalGroup, ScrollableContainer, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Select,
    Static,
    TextArea,
)
from textual.worker import WorkerState

from broker import helpers, settings
from broker.providers import PROVIDERS


def dictlist_to_table(dict_list, show_id=True):
    """Convert a list of dictionaries to a data table."""
    table = DataTable(cursor_type="row")
    if show_id:
        table.add_columns("Id", "Host")
    else:
        table.add_columns("Host")
    # add the rows
    for id_num, data_dict in enumerate(dict_list):
        row = [str(id_num)] if show_id else []
        row.extend([str(value) for value in data_dict.values()])
        table.add_row(*row, key=str(id_num))
    return table


class ProviderSync(HorizontalGroup):
    """A selection and button to sync one or all providers."""

    def __init__(self):
        super().__init__()
        self.value = "All"
        self.providers = ["All"]
        self.providers.extend(
            sorted([prov_name for prov_name, prov_cls in PROVIDERS.items() if not prov_cls.hidden])
        )
        self.provider_select = Select.from_values(
            self.providers, id="provider_select", value=self.value, allow_blank=False
        )
        self.sync_button = Button("Sync", id="sync", variant="success")

    def compose(self):
        """Create child widgets for the provider sync."""
        yield self.provider_select
        yield self.sync_button

    def on_select_changed(self, event):
        """Handle provider selection changes."""
        self.value = event.value
        # Notify parent to update the table
        self.post_message(self.SelectionChanged(self.value))

    class SelectionChanged(Message):
        """Selection changed message."""

        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()


class InventoryTable(DataTable):
    """A DataTable widget that displays and manages inventory data."""

    inventory_data = reactive([], layout=True)

    def __init__(self, show_id=True):
        super().__init__(cursor_type="row")
        self.show_id = show_id

    def watch_inventory_data(self, inventory):
        """React to changes in inventory data."""
        self.clear()
        # Check if we don't have our columns set up
        if not self.columns:
            if self.show_id:
                self.add_columns("Id", "Host")
            else:
                self.add_columns("Host")
        if not inventory:
            if self.show_id:
                self.add_row("X", "No hosts in inventory")
            else:
                self.add_row("No hosts in inventory")
            return

        inventory_fields = {
            "Host": settings.settings.get("inventory_list_vars") or "hostname | name"
        }
        curated_host_info = [
            helpers.inventory_fields_to_dict(
                inventory_fields=inventory_fields,
                host_dict=host,
            )
            for host in inventory
        ]

        for id_num, data_dict in enumerate(curated_host_info):
            row = [str(id_num)] if self.show_id else []
            row.extend([str(value) for value in data_dict.values()])
            self.add_row(*row, key=str(id_num))


class BrokerTUI(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [
        ("i", "inventory_view", "Inventory"),
        ("p", "providers_view", "Providers"),
        ("c", "checkout_view", "Checkout"),
        ("s", "sync", "Sync"),
        ("n", "checkin", "Check In"),
    ]

    CSS = """
    #button-container {
        layout: horizontal;
        content-align: right top;
        dock: bottom;
        width: 100%;
        height: 4;
    }

    #main-container {
        height: 100%;
    }

    #tables-container {
        width: 50%;
        height: 100%;
    }

    #inventory-table {
        height: 50%;
    }

    #checkin-table {
        height: 50%;
    }

    .table-label {
        background: $boost;
        color: $text;
        text-align: center;
    }

    TextArea {
        width: 50%;
        height: 100%;
        background: $surface;
    }

    DataTable {
        background: $surface;
    }

    Button {
        margin-left: 1;
        height: 3;
    }
    """

    current_provider = reactive("All")

    def __init__(self):
        super().__init__()
        self.details_view = TextArea(read_only=True)
        self.provider_sync = ProviderSync()
        self.checkin_button = Button("Check In", id="checkin", variant="error")
        self.raw_inventory = []
        self.filtered_inventory = []
        self.inventory_table = InventoryTable(show_id=True)
        self.checkin_table = InventoryTable(show_id=False)  # Initialize with hidden ID column
        self.checkin_hosts = []

    def on_mount(self):
        """Set the header title and sub-title."""
        self.title = "Broker"
        self.sub_title = "0.7.0"
        self.details_view.language = "yaml"
        self.inventory_table = self.get_inventory_table()

    def compose(self):
        """Create child widgets for the app."""
        yield Header()
        with Horizontal(id="main-container"):
            with Vertical(id="tables-container"):
                with Container(id="inventory-table"):
                    yield Static("Local Inventory", classes="table-label")
                    yield self.get_inventory_table()
                with Container(id="checkin-table"):
                    yield Static("Hosts to checkin", classes="table-label")
                    yield self.checkin_table
            yield self.details_view
        with Container(id="button-container"):
            yield self.provider_sync
            yield self.checkin_button

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "sync":
            if self.provider_sync.value == "All":
                self.notify("Syncing all providers", title="Sync Triggered")
                for provider in self.provider_sync.providers[1:]:
                    asyncio.create_task(self.action_sync(provider))  # noqa: RUF006
            else:
                asyncio.create_task(self.action_sync())  # noqa: RUF006
        elif event.button.id == "checkin":
            self.action_checkin()

    @work(exclusive=True)
    async def _sync_command(self, provider):
        returncode, stdout, stderr = await self.run_command(f"broker inventory --sync {provider}")
        return returncode, stdout, stderr

    async def action_sync(self, provider=None):
        """Handle sync command."""
        provider = provider or self.provider_sync.value
        self.notify(f"Starting sync for {provider}", title="Sync Triggered")
        self._sync_command(provider)

    def on_worker_state_changed(self, event):
        """Handle worker state changes."""
        if event.worker.name == "_sync_command" and event.state == WorkerState.SUCCESS:
            returncode, stdout, stderr = event.worker.result
            if returncode == 0:
                self.notify(
                    f"Successfully synced provider: {self.provider_sync.value}",
                    title="Success",
                    severity="information",
                )
                self.update_inventory()
            else:
                self.call_after_refresh(lambda: self.sync_error("Sync Error", stderr.decode()))
        elif event.worker.name == "_sync_command" and event.state == WorkerState.ERROR:
            self.call_after_refresh(lambda: self.sync_error("Sync Error", str(event.worker.error)))

    def sync_error(self, title, message):
        """Display sync error modal."""
        error_modal = ErrorModal(title, message)
        self.push_screen(error_modal)

    async def run_command(self, command):
        """Run a system command asynchronously and return the result."""
        process = await asyncio.create_subprocess_shell(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout, stderr

    def update_inventory(self):
        """Update the inventory data table with the latest data."""
        self.raw_inventory = helpers.load_inventory()
        self.filter_inventory()
        self.inventory_table.inventory_data = self.filtered_inventory
        self.refresh()

    def action_checkin(self):
        """Handle checkin command."""
        # Use self.checkin_hosts as the source for check-in
        checkin_names = [host.get("name") for host in self.checkin_hosts]
        self.notify(
            f"Checking in {len(checkin_names)} hosts\n{checkin_names}",
            title="Checkin Triggered",
            severity="warning",
        )
        # Command execution will be added here

    def filter_inventory(self):
        """Filter inventory based on selected provider."""
        if self.current_provider == "All":
            self.filtered_inventory = self.raw_inventory
        else:
            self.filtered_inventory = [
                host
                for host in self.raw_inventory
                if host.get("_broker_provider") == self.current_provider
            ]

    def get_inventory_table(self):
        """Display the current inventory in a data table."""
        self.raw_inventory = helpers.load_inventory()
        self.filter_inventory()
        self.inventory_table.inventory_data = self.filtered_inventory
        return self.inventory_table

    def on_provider_sync_selection_changed(self, message):
        """Handle provider selection changes."""
        self.current_provider = message.value
        self.filter_inventory()
        self.inventory_table.inventory_data = self.filtered_inventory
        self.refresh()

    def on_data_table_row_highlighted(self, event):
        """Handle row highlight in the inventory table."""
        if not event.row_key.value:
            return
        if not event.row_key.value.isdigit():
            self.details_view.text = "No host selected."
            return

        # Get the correct data source based on which table triggered the event
        if event.data_table == self.inventory_table:
            self.row_data = self.filtered_inventory[int(event.row_key.value)]
        else:  # checkin table
            self.row_data = self.checkin_hosts[int(event.row_key.value)]

        self.details_view.text = helpers.yaml_format(self.row_data)

    def on_data_table_row_selected(self, event):
        """Handle row selection in both tables."""
        if not event.row_key.value or not event.row_key.value.isdigit():
            return

        row_index = int(event.row_key.value)

        if event.data_table == self.checkin_table:
            # Remove selected host from check-in table
            if row_index < len(self.checkin_hosts):
                host_data = self.checkin_hosts[row_index]
                self.checkin_hosts.remove(host_data)
                self.checkin_table.inventory_data = self.checkin_hosts.copy()
                self.refresh()
        elif event.data_table == self.inventory_table:
            # Add selected host from inventory table to check-in table
            if row_index < len(self.filtered_inventory):
                host_data = self.filtered_inventory[row_index]
                if host_data not in self.checkin_hosts:
                    self.checkin_hosts.append(host_data)
                    self.checkin_table.inventory_data = self.checkin_hosts.copy()
                    self.refresh()

    def add_to_checkin_table(self, host_data):
        """Add selected host to the check-in table."""
        if host_data not in self.checkin_hosts:
            self.checkin_hosts.append(host_data)
            self.checkin_table.inventory_data = self.checkin_hosts.copy()
            self.refresh()

    def remove_from_checkin_table(self, host_data):
        """Remove selected host from the check-in table."""
        if host_data in self.checkin_hosts:
            self.checkin_hosts.remove(host_data)
            self.checkin_table.inventory_data = self.checkin_hosts.copy()
            self.refresh()


class ErrorModal(ModalScreen):
    """Modal screen to display error messages."""

    CSS = """
    ErrorModal {
        align: center middle;
    }

    #error-modal {
        align-horizontal: center;
        background: $surface;
        padding: 1;
        width: 75%;
        height: 75%;
        border: solid red;
        layout: vertical;
    }

    #error-message-container {
        height: 100%;
        width: 100%;
    }

    #dismiss {
        dock: bottom;
        margin-top: 2;
    }

    .error-title {
        text-align: center;
        margin-bottom: 1;
    }
    """

    def __init__(self, title, message):
        super().__init__()
        self.title_text = title
        self.error_message = message

    def compose(self):
        """Create child widgets for the error modal."""
        with Container(id="error-modal"):
            yield Static(self.title_text, classes="error-title")
            with ScrollableContainer(id="error-message-container"):
                yield TextArea(self.error_message, classes="error-message", read_only=True)
            yield Button("Dismiss", id="dismiss", variant="error")

    def on_button_pressed(self, event):
        """Dismiss the error modal."""
        if event.button.id == "dismiss":
            self.dismiss()


def main():
    """Run the Broker TUI app."""
    app = BrokerTUI()
    app.run()


if __name__ == "__main__":
    main()
