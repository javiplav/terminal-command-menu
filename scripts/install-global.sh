#!/bin/bash
# Global installation script for Terminal Command Menu
# This creates system-wide commands that don't require virtual environment activation

set -e

INSTALL_DIR="$HOME/.local/bin"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🚀 Installing Terminal Command Menu globally..."

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Create wrapper scripts that handle virtual environment automatically
cat > "$INSTALL_DIR/terminal-menu" << EOF
#!/bin/bash
# Terminal Command Menu - Global wrapper script
cd "$PROJECT_DIR"
source venv/bin/activate
exec python -m terminal_menu.main "\$@"
EOF

cat > "$INSTALL_DIR/cmd-menu" << EOF
#!/bin/bash
# Terminal Command Menu - Alternative wrapper script
cd "$PROJECT_DIR"
source venv/bin/activate
exec python -m terminal_menu.main "\$@"
EOF

cat > "$INSTALL_DIR/tcm" << EOF
#!/bin/bash
# Terminal Command Menu - Short wrapper script
cd "$PROJECT_DIR"
source venv/bin/activate
exec python -m terminal_menu.main "\$@"
EOF

# Make scripts executable
chmod +x "$INSTALL_DIR/terminal-menu"
chmod +x "$INSTALL_DIR/cmd-menu"
chmod +x "$INSTALL_DIR/tcm"

echo "✅ Installed wrapper scripts to $INSTALL_DIR"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "⚠️  Add ~/.local/bin to your PATH by adding this to your shell profile:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "For zsh, add to ~/.zshrc:"
    echo "   echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc"
    echo ""
else
    echo "✅ ~/.local/bin is already in your PATH"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "You can now use these commands from anywhere:"
echo "  terminal-menu    # Main command"
echo "  cmd-menu         # Alternative"
echo "  tcm              # Short alias"
echo ""
echo "No need to activate virtual environments - the scripts handle it automatically!"
EOF
