# 🧪 Testing Guide

## Navigation After Search - Fixed!

### The Issue You Reported
When searching for commands (e.g., "runat"), the arrow keys stopped working to navigate between the filtered results, making it impossible to select the 2nd command.

### How to Test the Fix

#### **1. Test Basic Search Navigation:**
```bash
# Launch the app
terminal-menu --fast

# Steps:
1. Press '/' to enter search mode
2. Type "runat" (or any search term that matches multiple commands)
3. Press 'Down Arrow' or 'Esc' to focus the command list
4. Use ↑/↓ arrow keys to navigate between filtered results
5. Press Enter to execute a command

# Expected Result: Arrow keys should now work properly!
```

#### **2. Test Search Workflow:**
```bash
# Full workflow test:
1. Launch: terminal-menu
2. Search: Press '/' and type part of a command
3. Navigate: Use arrows to move between results
4. Clear: Press 'Esc' to clear search and return to full list
5. Search Again: Press '/' and search for something else
6. Navigate: Arrows should work on new filtered results

# Expected: Navigation works at every step
```

#### **3. Test Edge Cases:**
```bash
# Edge case testing:
1. Search for something with only 1 result
   - Arrow keys should not cause errors
2. Search for something with no results
   - Should show "No commands found"
3. Clear search (empty search term)
   - Should return to full command list with working navigation
```

#### **4. Test Focus Transfer:**
```bash
# Focus behavior testing:
1. Start in search box (press '/')
2. Type a search term
3. Press 'Down Arrow' to move to command list
4. Use arrows to navigate - should work!
5. Press '/' again to return to search
6. Clear search and try navigation again
```

### What Was Fixed

#### **🔧 Technical Fixes Applied:**

1. **Table Refresh Issue:**
   ```python
   # Before: Table wasn't properly refreshed after clear()
   self.clear()
   # Add rows...
   
   # After: Forced widget refresh
   self.clear()
   # Add rows...
   self.refresh()  # Ensures proper table rebuild
   ```

2. **Cursor Positioning:**
   ```python
   # Before: Immediate cursor positioning (didn't work)
   self.move_cursor(row=0)
   
   # After: Delayed cursor positioning after table rebuild
   self.call_after_refresh(self._reset_cursor_position)
   ```

3. **Focus Management:**
   ```python
   # Enhanced focus transfer between search and command list
   # Added bounds checking for cursor position
   # Improved robustness of action_select_command
   ```

#### **🎯 Root Cause:**
When filtering commands, the DataTable widget needs time to rebuild its internal structure after `clear()` and `add_row()` operations. The cursor positioning and navigation were happening before the table was fully ready, causing the arrow keys to not respond properly.

### Additional Testing Commands

#### **Test Performance & Navigation Together:**
```bash
# Test fast mode with navigation
terminal-menu --fast
# Search and navigate - should be both fast AND functional

# Test with confirmation disabled  
terminal-menu --fast --no-confirm
# Search, navigate, execute - maximum speed workflow
```

#### **Test Standalone Version:**
```bash
# The standalone version should also work correctly
./terminal-menu-standalone
# Same search and navigation tests apply
```

### Expected Behavior After Fix

✅ **Search works:** Type to filter commands  
✅ **Navigation works:** Arrow keys move between filtered results  
✅ **Focus works:** Smooth transition between search box and command list  
✅ **Selection works:** Enter executes the highlighted command  
✅ **Clear works:** Empty search returns to full list with working navigation  
✅ **Performance:** Fast mode still provides optimized execution  

### If You Still Experience Issues

If the navigation still doesn't work after this fix:

1. **Clear the app config:**
   ```bash
   rm -rf ~/.config/terminal-command-menu/
   ```

2. **Reinstall the standalone version:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/javiplav/terminal-command-menu/main/install.sh | bash
   ```

3. **Test with minimal history:**
   Create a small test history to isolate the issue.

4. **Report the issue:**
   Include details about:
   - Your terminal emulator (iTerm2, Terminal.app, etc.)
   - Shell type (zsh, bash)
   - Number of commands in history
   - Exact steps to reproduce

### 🎉 You Should Now Be Able To:

- ✅ Search for "runat" and see filtered results
- ✅ Use ↑/↓ arrow keys to navigate between the results  
- ✅ Select the 2nd command (or any command) with arrows
- ✅ Press Enter to execute the selected command
- ✅ Enjoy a smooth, fast command selection workflow!

**The navigation bug has been fixed - your workflow should now be seamless!** 🚀
