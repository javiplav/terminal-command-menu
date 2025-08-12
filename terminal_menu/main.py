"""Main entry point for the terminal command menu application."""

import sys
import os
import argparse
from typing import Optional

import click

from .tui import run_tui
from .executor import execute_command_and_exit
from .history_parser import ShellHistoryParser
from .settings import Settings


@click.command()
@click.option('--shell', type=click.Choice(['zsh', 'bash', 'fish']), 
              help='Specify shell type (auto-detected if not provided)')
@click.option('--max-commands', type=int, default=100,
              help='Maximum number of commands to display')
@click.option('--no-confirm', is_flag=True,
              help='Skip confirmation before executing commands')
@click.option('--stats', is_flag=True,
              help='Show statistics and exit')
@click.option('--refresh', is_flag=True,
              help='Refresh history cache and exit')
@click.option('--config', is_flag=True,
              help='Show configuration path and exit')
@click.version_option(version='1.0.0', prog_name='Terminal Command Menu')
def main(shell: Optional[str], max_commands: int, no_confirm: bool, 
         stats: bool, refresh: bool, config: bool) -> None:
    """Terminal Command Menu - A developer productivity tool for frequently used commands.
    
    This tool displays a searchable, interactive menu of your most frequently 
    used terminal commands, sorted by usage frequency.
    """
    
    # Initialize settings
    settings = Settings()
    
    # Handle info commands
    if config:
        print(f"Configuration directory: {settings.config_dir}")
        print(f"Settings file: {settings.config_file}")
        print(f"Statistics file: {settings.stats_file}")
        return
    
    if stats:
        show_statistics(settings)
        return
    
    if refresh:
        refresh_history_cache()
        print("History cache refreshed!")
        return
    
    # Update settings from command line options
    if shell:
        settings.set('shell_type', shell)
    
    if max_commands != 100:  # Only update if different from default
        settings.set('max_commands', max_commands)
    
    if no_confirm:
        settings.set('confirm_execution', False)
    
    # Increment session count
    settings.increment_session_count()
    
    try:
        # Run the TUI and get the selected command
        selected_command = run_tui()
        
        if selected_command:
            # Execute the selected command
            execute_command_and_exit(selected_command)
        else:
            # User cancelled or quit
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def show_statistics(settings: Settings) -> None:
    """Display usage statistics."""
    parser = ShellHistoryParser()
    commands = parser.parse_history()
    stats = parser.get_statistics(commands)
    app_stats = settings.get_stats()
    
    print("📊 TERMINAL COMMAND MENU STATISTICS")
    print("=" * 50)
    
    # History statistics
    print(f"Total commands in history: {stats['total_commands']}")
    print(f"Unique commands: {stats['unique_commands']}")
    
    # Category breakdown
    print("\n📁 COMMAND CATEGORIES:")
    category_breakdown = stats.get('category_breakdown', {})
    for category, count in sorted(category_breakdown.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count}")
    
    # Top commands
    print(f"\n🔥 TOP {min(10, len(stats['top_commands']))} COMMANDS:")
    for i, cmd in enumerate(stats['top_commands'][:10], 1):
        print(f"  {i:2d}. [{cmd.category}] {cmd.text} ({cmd.count}x)")
    
    # App usage statistics
    print(f"\n📱 APP USAGE:")
    print(f"Sessions started: {app_stats.get('session_count', 0)}")
    print(f"Commands executed via app: {app_stats.get('total_executions', 0)}")
    
    # Most executed via app
    command_executions = app_stats.get('command_executions', {})
    if command_executions:
        print(f"\n⚡ MOST EXECUTED VIA APP:")
        sorted_executions = sorted(command_executions.items(), key=lambda x: x[1], reverse=True)
        for i, (cmd, count) in enumerate(sorted_executions[:5], 1):
            print(f"  {i}. {cmd} ({count}x)")


def refresh_history_cache() -> None:
    """Refresh the history cache."""
    # For now, this is a placeholder since we don't cache history
    # In the future, we could implement caching for performance
    parser = ShellHistoryParser()
    commands = parser.parse_history()
    print(f"Parsed {len(commands)} unique commands from history")


if __name__ == '__main__':
    main()
