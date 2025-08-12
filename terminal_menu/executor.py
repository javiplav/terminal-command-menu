"""Command execution module with shell integration."""

import os
import sys
import subprocess
import shlex
from typing import Optional, Tuple
from pathlib import Path

from .settings import Settings


class CommandExecutor:
    """Handles command execution in the user's shell environment."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.shell = self._detect_shell()
    
    def _detect_shell(self) -> str:
        """Detect the user's shell."""
        shell_setting = self.settings.get('shell_type')
        if shell_setting:
            return shell_setting
        
        # Get from environment
        shell = os.environ.get('SHELL', '/bin/bash')
        return shell
    
    def prepare_command_for_execution(self, command: str) -> str:
        """Prepare command for execution in the current shell context."""
        command = command.strip()
        
        # Handle common aliases by expanding them to full commands
        # This ensures commands work even when aliases aren't available in subprocess
        
        # Kubectl aliases
        if command.startswith('k '):
            command = command.replace('k ', 'kubectl ', 1)
        elif command == 'k':
            command = 'kubectl'
        
        # Git aliases (common ones)
        elif command.startswith('gco '):
            command = command.replace('gco ', 'git checkout ', 1)
        elif command == 'gco':
            command = 'git checkout'
        elif command.startswith('gst'):
            command = command.replace('gst', 'git status', 1)
        elif command.startswith('gaa'):
            command = command.replace('gaa', 'git add --all', 1)
        elif command.startswith('gcm '):
            command = command.replace('gcm ', 'git commit -m ', 1)
        elif command.startswith('gp'):
            command = command.replace('gp', 'git push', 1)
        elif command.startswith('gl'):
            command = command.replace('gl', 'git pull', 1)
        
        # List aliases
        elif command == 'll':
            command = 'ls -la'
        elif command == 'la':
            command = 'ls -la'
        
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
