# AutomationManager Module

This module uses UI Automation to interact with the UI elements of the LINE application.

## Overview

`AutomationManager` is a utility class providing only static methods to search for and manipulate UI elements in the LINE application using the UI Automation API.

## Class

### `AutomationManager`

A class providing only static methods. No instantiation is required.

## Methods

### `_get_line_window() -> Optional[auto.WindowControl]`

Retrieves the LINE main window.

**Returns:**
- `Optional[auto.WindowControl]`: The found WindowControl object, or `None` if not found.

**Note:** This method is intended for internal use.

### `type_in_chat(text: str) -> str`

Inputs text into the chat input field.

**Parameters:**
- `text: str`: The text to input.

**Returns:**
- `str`: A message indicating the result of the process.

**Example:**
```python
from n_line.core.automation_manager import AutomationManager

result = AutomationManager.type_in_chat("Hello, World!")
print(result)
```

### `press_send() -> str`

Sends the chat send key (Enter).

Focuses on the input field and sends the Enter key. This method is more reliable than searching for the "Send" button.

**Returns:**
- `str`: A message indicating the result of the process.

## Implementation Details

### Window Searching
Uses `auto.WindowControl()` to search for the window named "LINE".

### Chat Input Field Searching
Searches for an `EditControl` with the class name `AutoSuggestTextArea`. It uses a `searchDepth=15` as the element may be nested deeply.

### Text Input
1. Brings the window to the front.
2. Clicks the input field.
3. Inputs the text using `SendKeys()`.

### Sending
1. Focuses on the input field.
2. Sends the `{Enter}` key.

## Error Handling
All methods implement proper error handling and safely manage exceptions.

## Notes
- LINE must be running.
- A chat window must be open.
- UI Automation must be functioning correctly.

## Related Modules
- `uiautomation`: UI Automation API
- `win32gui`: Win32 GUI API
