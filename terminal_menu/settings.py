"""Settings management for the terminal command menu."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class Settings:
    """Manages application settings with persistence."""
    
    DEFAULT_SETTINGS = {
        'max_commands': 100,
        'confirm_execution': True,
        'sort_method': 'frequency',  # frequency, recency, alphabetical
        'show_categories': True,
        'auto_refresh': True,
        'shell_type': None,  # auto-detect if None
        'excluded_patterns': [
            'ls',
            'cd',
            'pwd',
            'clear',
            'exit'
        ],
        'category_filters': [],  # Empty means show all categories
        'theme': 'dark',
    }
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize settings with optional custom config directory."""
        if config_dir is None:
            # Use XDG config directory or fallback to home
            xdg_config = os.environ.get('XDG_CONFIG_HOME')
            if xdg_config:
                config_dir = Path(xdg_config) / 'terminal-command-menu'
            else:
                config_dir = Path.home() / '.config' / 'terminal-command-menu'
        
        self.config_dir = config_dir
        self.config_file = config_dir / 'settings.json'
        self.stats_file = config_dir / 'stats.json'
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Load settings
        self._settings = self.load_settings()
        self._stats = self.load_stats()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or return defaults."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded_settings = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                settings = self.DEFAULT_SETTINGS.copy()
                settings.update(loaded_settings)
                return settings
            
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading settings: {e}. Using defaults.")
        
        return self.DEFAULT_SETTINGS.copy()
    
    def save_settings(self) -> None:
        """Save current settings to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except IOError as e:
            print(f"Error saving settings: {e}")
    
    def load_stats(self) -> Dict[str, Any]:
        """Load usage statistics from file."""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading stats: {e}")
        
        return {
            'command_executions': {},  # command -> count
            'session_count': 0,
            'total_executions': 0,
            'last_used': {},  # command -> timestamp
        }
    
    def save_stats(self) -> None:
        """Save usage statistics to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self._stats, f, indent=2)
        except IOError as e:
            print(f"Error saving stats: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a setting value and save."""
        self._settings[key] = value
        self.save_settings()
    
    def update(self, settings: Dict[str, Any]) -> None:
        """Update multiple settings at once."""
        self._settings.update(settings)
        self.save_settings()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self._settings = self.DEFAULT_SETTINGS.copy()
        self.save_settings()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return self._stats.copy()
    
    def record_execution(self, command: str) -> None:
        """Record a command execution in statistics."""
        # Update execution count
        self._stats['command_executions'][command] = \
            self._stats['command_executions'].get(command, 0) + 1
        
        # Update totals
        self._stats['total_executions'] = \
            self._stats.get('total_executions', 0) + 1
        
        # Update last used timestamp
        import time
        self._stats['last_used'][command] = time.time()
        
        self.save_stats()
    
    def increment_session_count(self) -> None:
        """Increment the session counter."""
        self._stats['session_count'] = self._stats.get('session_count', 0) + 1
        self.save_stats()
    
    def get_excluded_patterns(self) -> list:
        """Get list of command patterns to exclude."""
        return self._settings.get('excluded_patterns', [])
    
    def add_excluded_pattern(self, pattern: str) -> None:
        """Add a pattern to the exclusion list."""
        excluded = self.get_excluded_patterns()
        if pattern not in excluded:
            excluded.append(pattern)
            self.set('excluded_patterns', excluded)
    
    def remove_excluded_pattern(self, pattern: str) -> None:
        """Remove a pattern from the exclusion list."""
        excluded = self.get_excluded_patterns()
        if pattern in excluded:
            excluded.remove(pattern)
            self.set('excluded_patterns', excluded)
    
    def should_exclude_command(self, command: str) -> bool:
        """Check if a command should be excluded based on patterns."""
        excluded_patterns = self.get_excluded_patterns()
        first_word = command.split()[0] if command.split() else ""
        
        return any(
            pattern in command or pattern == first_word
            for pattern in excluded_patterns
        )
    
    def get_category_filters(self) -> list:
        """Get list of categories to show (empty = show all)."""
        return self._settings.get('category_filters', [])
    
    def set_category_filters(self, categories: list) -> None:
        """Set which categories to show."""
        self.set('category_filters', categories)
    
    def should_show_category(self, category: str) -> bool:
        """Check if a category should be shown."""
        filters = self.get_category_filters()
        return not filters or category in filters
