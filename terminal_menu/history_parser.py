"""Shell history parser for different shell types."""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import Counter
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Command:
    """Represents a shell command with metadata."""
    text: str
    count: int
    category: str = "Other"
    last_used: Optional[datetime] = None


class ShellHistoryParser:
    """Parses shell history files from different shells."""
    
    def __init__(self):
        self.home = Path.home()
        self.command_categories = {
            'git': ['git', 'gco', 'gst', 'gaa', 'gcm', 'gp', 'gl', 'gh'],
            'docker': ['docker', 'docker-compose', 'podman'],
            'kubernetes': ['kubectl', 'k', 'helm', 'kustomize'],
            'npm': ['npm', 'yarn', 'pnpm', 'node'],
            'python': ['python', 'pip', 'conda', 'poetry', 'pytest'],
            'system': ['ls', 'cd', 'pwd', 'mkdir', 'rm', 'cp', 'mv', 'find', 'grep'],
            'editor': ['vim', 'nvim', 'code', 'nano', 'emacs'],
        }
    
    def detect_shell(self) -> str:
        """Detect the current shell type."""
        shell = os.environ.get('SHELL', '')
        if 'zsh' in shell:
            return 'zsh'
        elif 'bash' in shell:
            return 'bash'
        elif 'fish' in shell:
            return 'fish'
        else:
            # Try to detect based on available history files
            if (self.home / '.zsh_history').exists():
                return 'zsh'
            elif (self.home / '.bash_history').exists():
                return 'bash'
            elif (self.home / '.local/share/fish/fish_history').exists():
                return 'fish'
            else:
                return 'bash'  # Default fallback
    
    def get_history_file_path(self, shell_type: str) -> Optional[Path]:
        """Get the history file path for the given shell type."""
        paths = {
            'zsh': self.home / '.zsh_history',
            'bash': self.home / '.bash_history',
            'fish': self.home / '.local/share/fish/fish_history',
        }
        
        path = paths.get(shell_type)
        return path if path and path.exists() else None
    
    def parse_zsh_history(self, file_path: Path) -> List[str]:
        """Parse zsh history file."""
        commands = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Zsh history format: ": timestamp:duration;command"
                    if line.startswith(':'):
                        # Extract command part after the semicolon
                        parts = line.split(';', 1)
                        if len(parts) > 1:
                            commands.append(parts[1].strip())
                    else:
                        # Simple command line
                        commands.append(line)
        except Exception as e:
            print(f"Error reading zsh history: {e}")
        
        return commands
    
    def parse_bash_history(self, file_path: Path) -> List[str]:
        """Parse bash history file."""
        commands = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        commands.append(line)
        except Exception as e:
            print(f"Error reading bash history: {e}")
        
        return commands
    
    def parse_fish_history(self, file_path: Path) -> List[str]:
        """Parse fish history file."""
        commands = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                current_cmd = ""
                for line in f:
                    line = line.strip()
                    if line.startswith('- cmd:'):
                        if current_cmd:
                            commands.append(current_cmd)
                        current_cmd = line[6:].strip()  # Remove '- cmd:'
                    elif line.startswith('  when:') or line.startswith('- when:'):
                        if current_cmd:
                            commands.append(current_cmd)
                            current_cmd = ""
                
                if current_cmd:
                    commands.append(current_cmd)
        except Exception as e:
            print(f"Error reading fish history: {e}")
        
        return commands
    
    def categorize_command(self, command: str) -> str:
        """Categorize a command based on its first word."""
        first_word = command.split()[0] if command.split() else ""
        
        for category, keywords in self.command_categories.items():
            if first_word in keywords:
                return category.title()
        
        return "Other"
    
    def clean_command(self, command: str) -> str:
        """Clean and normalize a command."""
        # Remove leading/trailing whitespace
        command = command.strip()
        
        # Remove common prefixes like 'sudo '
        if command.startswith('sudo '):
            command = command[5:]
        
        # Collapse multiple spaces
        command = re.sub(r'\s+', ' ', command)
        
        return command
    
    def parse_history(self, shell_type: Optional[str] = None) -> List[Command]:
        """Parse shell history and return list of Command objects."""
        if shell_type is None:
            shell_type = self.detect_shell()
        
        history_file = self.get_history_file_path(shell_type)
        if not history_file:
            print(f"No history file found for {shell_type}")
            return []
        
        print(f"Parsing {shell_type} history from {history_file}")
        
        # Parse based on shell type
        if shell_type == 'zsh':
            raw_commands = self.parse_zsh_history(history_file)
        elif shell_type == 'bash':
            raw_commands = self.parse_bash_history(history_file)
        elif shell_type == 'fish':
            raw_commands = self.parse_fish_history(history_file)
        else:
            print(f"Unsupported shell type: {shell_type}")
            return []
        
        # Clean and deduplicate commands
        cleaned_commands = []
        for cmd in raw_commands:
            cleaned = self.clean_command(cmd)
            if cleaned and len(cleaned) > 1:  # Skip empty or single character commands
                cleaned_commands.append(cleaned)
        
        # Count frequencies
        command_counts = Counter(cleaned_commands)
        
        # Create Command objects
        commands = []
        for cmd_text, count in command_counts.items():
            category = self.categorize_command(cmd_text)
            commands.append(Command(
                text=cmd_text,
                count=count,
                category=category
            ))
        
        # Sort by frequency (descending)
        commands.sort(key=lambda x: x.count, reverse=True)
        
        return commands
    
    def get_statistics(self, commands: List[Command]) -> Dict[str, any]:
        """Get statistics about the command history."""
        total_commands = sum(cmd.count for cmd in commands)
        unique_commands = len(commands)
        
        # Category breakdown
        category_counts = {}
        for cmd in commands:
            category_counts[cmd.category] = category_counts.get(cmd.category, 0) + cmd.count
        
        return {
            'total_commands': total_commands,
            'unique_commands': unique_commands,
            'category_breakdown': category_counts,
            'top_commands': commands[:10]  # Top 10 most frequent
        }
