"""Terminal User Interface for the command menu."""

import os
import subprocess
import sys
from typing import List, Optional, Callable

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Input, Static, DataTable, Button, Label
)
from textual.binding import Binding
from textual.reactive import reactive
from textual.message import Message
from textual import events
from rich.text import Text
from rich.console import Console

from .history_parser import Command, ShellHistoryParser
from .settings import Settings


class CommandList(DataTable):
    """Custom DataTable for displaying commands."""
    
    BINDINGS = [
        Binding("enter", "select_command", "Execute Command"),
        Binding("escape", "app.quit", "Quit"),
        Binding("ctrl+r", "refresh", "Refresh"),
        Binding("ctrl+s", "show_settings", "Settings"),
    ]
    
    def __init__(self, commands: List[Command], **kwargs):
        super().__init__(**kwargs)
        self.commands = commands
        self.filtered_commands = commands.copy()
        self.on_execute: Optional[Callable[[str], None]] = None
        
    def compose(self) -> ComposeResult:
        return super().compose()
    
    def on_mount(self) -> None:
        """Set up the data table."""
        self.add_columns("Category", "Command", "Count")
        self.cursor_type = "row"
        self.zebra_stripes = True
        self.refresh_table()
    
    def refresh_table(self) -> None:
        """Refresh the table with filtered commands."""
        self.clear()
        for cmd in self.filtered_commands:
            category_text = Text(f"[{cmd.category}]", style="bold cyan")
            command_text = Text(cmd.text, style="white")
            count_text = Text(f"({cmd.count}x)", style="bold yellow")
            
            self.add_row(category_text, command_text, count_text, key=cmd.text)
    
    def filter_commands(self, search_term: str) -> None:
        """Filter commands based on search term."""
        if not search_term:
            self.filtered_commands = self.commands.copy()
        else:
            search_lower = search_term.lower()
            self.filtered_commands = [
                cmd for cmd in self.commands
                if search_lower in cmd.text.lower() or search_lower in cmd.category.lower()
            ]
        
        self.refresh_table()
        
        # Reset cursor to top
        if self.filtered_commands:
            self.move_cursor(row=0)
    
    def action_select_command(self) -> None:
        """Execute the selected command."""
        if self.cursor_row < len(self.filtered_commands):
            selected_command = self.filtered_commands[self.cursor_row]
            if self.on_execute:
                self.on_execute(selected_command.text)
    
    def action_refresh(self) -> None:
        """Refresh the command list."""
        self.post_message(self.RefreshRequested())
    
    def action_show_settings(self) -> None:
        """Show settings menu."""
        self.post_message(self.SettingsRequested())
    
    class RefreshRequested(Message):
        """Message sent when refresh is requested."""
        pass
    
    class SettingsRequested(Message):
        """Message sent when settings are requested."""
        pass


class StatsPanel(Static):
    """Panel showing command statistics."""
    
    def __init__(self, stats: dict, **kwargs):
        super().__init__(**kwargs)
        self.stats = stats
    
    def render(self) -> Text:
        """Render the statistics."""
        text = Text()
        text.append("📊 STATISTICS\n", style="bold magenta")
        text.append(f"Total commands: {self.stats.get('total_commands', 0)}\n", style="cyan")
        text.append(f"Unique commands: {self.stats.get('unique_commands', 0)}\n", style="cyan")
        
        # Category breakdown
        text.append("\n📁 CATEGORIES\n", style="bold magenta")
        category_breakdown = self.stats.get('category_breakdown', {})
        for category, count in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True):
            text.append(f"{category}: {count}\n", style="yellow")
        
        return text


class SearchInput(Input):
    """Custom search input with fuzzy search capabilities."""
    
    BINDINGS = [
        Binding("escape", "clear_and_focus_list", "Clear & Focus List"),
        Binding("down", "focus_list", "Focus List"),
        Binding("ctrl+j", "focus_list", "Focus List"),
    ]
    
    def __init__(self, **kwargs):
        super().__init__(placeholder="🔍 Search commands...", **kwargs)
        self.on_search: Optional[Callable[[str], None]] = None
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes for real-time search."""
        if self.on_search:
            self.on_search(event.value)
    
    def action_clear_and_focus_list(self) -> None:
        """Clear search and focus the command list."""
        self.value = ""
        self.post_message(self.FocusListRequested())
    
    def action_focus_list(self) -> None:
        """Focus the command list."""
        self.post_message(self.FocusListRequested())
    
    class FocusListRequested(Message):
        """Message sent when list focus is requested."""
        pass


class ConfirmDialog(Container):
    """Confirmation dialog for command execution."""
    
    def __init__(self, command: str, **kwargs):
        super().__init__(**kwargs)
        self.command = command
        self.can_focus = True
    
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static(f"Execute command: [bold cyan]{self.command}[/]?", id="confirm-text")
            with Horizontal():
                yield Button("Execute", variant="success", id="confirm-yes")
                yield Button("Cancel", variant="error", id="confirm-no")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "confirm-yes":
            self.post_message(self.CommandConfirmed(self.command))
        else:
            self.post_message(self.CommandCancelled())
    
    class CommandConfirmed(Message):
        """Message sent when command execution is confirmed."""
        def __init__(self, command: str):
            super().__init__()
            self.command = command
    
    class CommandCancelled(Message):
        """Message sent when command execution is cancelled."""
        pass


class TerminalCommandMenu(App):
    """Main application for the terminal command menu."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #header {
        dock: top;
        height: 3;
        background: $primary;
        color: $text;
        content-align: center middle;
    }
    
    #main-container {
        height: 1fr;
        background: $surface;
    }
    
    #search-container {
        dock: top;
        height: 3;
        padding: 1;
        background: $panel;
    }
    
    #content-container {
        height: 1fr;
    }
    
    #stats-panel {
        dock: left;
        width: 30;
        padding: 1;
        background: $panel;
        border-right: solid $primary;
    }
    
    #command-list {
        height: 1fr;
        padding: 1;
    }
    
    #confirm-dialog {
        dock: bottom;
        height: 7;
        padding: 1;
        background: $warning;
        border-top: solid $error;
    }
    
    SearchInput {
        width: 1fr;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+r", "refresh_history", "Refresh"),
        Binding("ctrl+s", "toggle_settings", "Settings"),
        Binding("/", "focus_search", "Search"),
    ]
    
    show_confirm_dialog = reactive(False)
    pending_command = reactive("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = ShellHistoryParser()
        self.settings = Settings()
        self.commands: List[Command] = []
        self.stats: dict = {}
        self.command_list: Optional[CommandList] = None
        self.search_input: Optional[SearchInput] = None
        self.confirm_dialog: Optional[ConfirmDialog] = None
        
    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header(show_clock=False, name="Terminal Command Menu", id="header")
        
        with Container(id="main-container"):
            with Container(id="search-container"):
                yield SearchInput(id="search")
            
            with Horizontal(id="content-container"):
                yield StatsPanel(self.stats, id="stats-panel")
                yield CommandList(self.commands, id="command-list")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Load data when the app starts."""
        self.setup_callbacks()
        self.load_history()
    
    def setup_callbacks(self) -> None:
        """Set up callback functions."""
        self.command_list = self.query_one("#command-list", CommandList)
        self.search_input = self.query_one("#search", SearchInput)
        
        # Set up callbacks
        self.command_list.on_execute = self.request_command_execution
        self.search_input.on_search = self.command_list.filter_commands
    
    def load_history(self) -> None:
        """Load shell history and update the UI."""
        self.commands = self.parser.parse_history()
        self.stats = self.parser.get_statistics(self.commands)
        
        # Limit displayed commands based on settings
        max_commands = self.settings.get('max_commands', 100)
        self.commands = self.commands[:max_commands]
        
        # Update UI components
        if hasattr(self, 'command_list') and self.command_list:
            self.command_list.commands = self.commands
            self.command_list.filtered_commands = self.commands.copy()
            self.command_list.refresh_table()
        
        # Update stats panel
        try:
            stats_panel = self.query_one("#stats-panel", StatsPanel)
            stats_panel.stats = self.stats
            stats_panel.refresh()
        except Exception:
            # Stats panel might not be ready yet
            pass
    
    def request_command_execution(self, command: str) -> None:
        """Request confirmation for command execution."""
        if self.settings.get('confirm_execution', True):
            self.pending_command = command
            self.show_confirm_dialog = True
            self.mount_confirm_dialog()
        else:
            self.execute_command(command)
    
    def mount_confirm_dialog(self) -> None:
        """Mount the confirmation dialog."""
        self.confirm_dialog = ConfirmDialog(self.pending_command, id="confirm-dialog")
        self.mount(self.confirm_dialog)
        self.confirm_dialog.focus()
    
    def remove_confirm_dialog(self) -> None:
        """Remove the confirmation dialog."""
        if self.confirm_dialog:
            self.confirm_dialog.remove()
            self.confirm_dialog = None
        self.show_confirm_dialog = False
        self.command_list.focus()
    
    def execute_command(self, command: str) -> None:
        """Execute the selected command."""
        self.exit(result=command)
    
    def action_refresh_history(self) -> None:
        """Refresh the command history."""
        self.load_history()
        self.notify("History refreshed!", title="Success")
    
    def action_focus_search(self) -> None:
        """Focus the search input."""
        self.search_input.focus()
    
    def action_toggle_settings(self) -> None:
        """Toggle settings menu."""
        # For now, just show a notification
        self.notify("Settings menu not implemented yet", title="Info")
    
    # Message handlers
    def on_command_list_refresh_requested(self, message: CommandList.RefreshRequested) -> None:
        """Handle refresh requests from command list."""
        self.action_refresh_history()
    
    def on_command_list_settings_requested(self, message: CommandList.SettingsRequested) -> None:
        """Handle settings requests from command list."""
        self.action_toggle_settings()
    
    def on_search_input_focus_list_requested(self, message: SearchInput.FocusListRequested) -> None:
        """Handle focus list requests from search input."""
        self.command_list.focus()
    
    def on_confirm_dialog_command_confirmed(self, message: ConfirmDialog.CommandConfirmed) -> None:
        """Handle confirmed command execution."""
        self.remove_confirm_dialog()
        self.execute_command(message.command)
    
    def on_confirm_dialog_command_cancelled(self, message: ConfirmDialog.CommandCancelled) -> None:
        """Handle cancelled command execution."""
        self.remove_confirm_dialog()


def run_tui() -> Optional[str]:
    """Run the TUI and return the selected command."""
    app = TerminalCommandMenu()
    return app.run()
