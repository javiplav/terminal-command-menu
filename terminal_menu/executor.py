"""Command execution module with shell integration."""

import os
import sys
import subprocess
import shlex
import re
from typing import Optional, Tuple, Dict
from pathlib import Path

from .settings import Settings


class CommandExecutor:
    """Handles command execution in the user's shell environment."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.shell = self._detect_shell()
        self._aliases_cache = None
    
    def _detect_shell(self) -> str:
        """Detect the user's shell."""
        shell_setting = self.settings.get('shell_type')
        if shell_setting:
            return shell_setting
        
        # Get from environment
        shell = os.environ.get('SHELL', '/bin/bash')
        return shell
    
    def _load_shell_aliases(self) -> Dict[str, str]:
        """Load aliases from the user's shell configuration."""
        if self._aliases_cache is not None:
            return self._aliases_cache
        
        aliases = {}
        shell_name = os.path.basename(self.shell)
        
        try:
            if 'zsh' in shell_name:
                # Get aliases from zsh - need to source .zshrc first
                result = subprocess.run(
                    ['zsh', '-i', '-c', 'source ~/.zshrc 2>/dev/null; alias'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    env=os.environ.copy()
                )

                if result.returncode == 0:
                    aliases = self._parse_alias_output(result.stdout)
            
            elif 'bash' in shell_name:
                # Get aliases from bash
                result = subprocess.run(
                    ['bash', '-i', '-c', 'source ~/.bashrc 2>/dev/null; alias'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    env=os.environ.copy()
                )
                if result.returncode == 0:
                    aliases = self._parse_alias_output(result.stdout)
        
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            # If we can't load aliases, fall back to empty dict
            pass
        
        self._aliases_cache = aliases
        return aliases
    
    def _parse_alias_output(self, alias_output: str) -> Dict[str, str]:
        """Parse the output of the 'alias' command."""
        aliases = {}
        
        for line in alias_output.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Parse lines like: alias k='kubectl'
            # or: alias ll='ls -la'
            # Handle both quoted and unquoted values
            if '=' in line:
                # Split on first =
                parts = line.split('=', 1)
                if len(parts) == 2:
                    alias_name = parts[0].strip()
                    alias_value = parts[1].strip()
                    
                    # Remove 'alias ' prefix if present
                    if alias_name.startswith('alias '):
                        alias_name = alias_name[6:].strip()
                    
                    # Remove quotes from value
                    if alias_value.startswith(("'", '"')) and alias_value.endswith(("'", '"')):
                        alias_value = alias_value[1:-1]
                    
                    if alias_name and alias_value:
                        aliases[alias_name] = alias_value
        return aliases
    
    def prepare_command_for_execution(self, command: str) -> str:
        """Prepare command for execution by expanding shell aliases."""
        command = command.strip()
        if not command:
            return command
        
        # Load shell aliases
        aliases = self._load_shell_aliases()
        
        # Split command into parts
        parts = command.split()
        if not parts:
            return command
        
        first_word = parts[0]
        
        # Check if the first word is an alias
        if first_word in aliases:
            alias_expansion = aliases[first_word]
            # Replace the first word with the alias expansion
            expanded_parts = alias_expansion.split() + parts[1:]
            return ' '.join(expanded_parts)
        
        return command
    
    def execute_command_in_shell(self, command: str, cwd: Optional[str] = None) -> int:
        """Execute command in the user's shell and return exit code."""
        prepared_command = self.prepare_command_for_execution(command)
        
        # Record the execution in statistics
        self.settings.record_execution(prepared_command)
        
        # Use the same working directory as the current process
        if cwd is None:
            cwd = os.getcwd()
        
        try:
            # Execute in the user's shell
            process = subprocess.run(
                prepared_command,
                shell=True,
                cwd=cwd,
                executable=self.shell,
                env=os.environ.copy()
            )
            
            return process.returncode
            
        except Exception as e:
            print(f"Error executing command '{prepared_command}': {e}")
            return 1
    

    
    def can_execute_command(self, command: str) -> Tuple[bool, str]:
        """Check if a command can be executed safely."""
        command = command.strip()
        
        if not command:
            return False, "Empty command"
        
        # Check for potentially dangerous commands
        dangerous_patterns = [
            'rm -rf /',
            'rm -rf *',
            'sudo rm -rf',
            'mkfs.',
            'dd if=',
            '> /dev/',
            'chmod -R 777 /',
            'chown -R',
        ]
        
        command_lower = command.lower()
        for pattern in dangerous_patterns:
            if pattern in command_lower:
                return False, f"Potentially dangerous command detected: {pattern}"
        
        return True, "Command is safe to execute"
    
    def get_command_preview(self, command: str) -> str:
        """Get a preview of what the command will do."""
        # For certain commands, we can provide helpful previews
        parts = command.split()
        if not parts:
            return "Empty command"
        
        first_word = parts[0]
        
        previews = {
            'cd': f"Change directory to: {' '.join(parts[1:]) if len(parts) > 1 else '~'}",
            'ls': f"List contents of: {' '.join(parts[1:]) if len(parts) > 1 else 'current directory'}",
            'git': f"Git operation: {' '.join(parts[1:])}",
            'docker': f"Docker operation: {' '.join(parts[1:])}",
            'kubectl': f"Kubernetes operation: {' '.join(parts[1:])}",
            'npm': f"NPM operation: {' '.join(parts[1:])}",
            'yarn': f"Yarn operation: {' '.join(parts[1:])}",
            'pip': f"Pip operation: {' '.join(parts[1:])}",
        }
        
        return previews.get(first_word, f"Execute: {command}")


def execute_command_and_exit(command: str) -> None:
    """Execute a command and exit the application properly.
    
    This function is designed to be called from the main application
    to execute a selected command and then exit cleanly.
    """
    settings = Settings()
    executor = CommandExecutor(settings)
    
    # Check if command can be executed safely
    can_execute, reason = executor.can_execute_command(command)
    if not can_execute:
        print(f"Cannot execute command: {reason}")
        sys.exit(1)
    
    # Show what we're about to execute
    print(f"Executing: {command}")
    
    # Execute the command
    exit_code = executor.execute_command_in_shell(command)
    
    # Exit with the same code as the executed command
    sys.exit(exit_code)
