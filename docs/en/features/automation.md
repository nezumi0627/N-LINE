# Automation (Experimental)

## Overview
This is an experimental feature that emulates user input into LINE's chat screen. 
It uses the UI Automation API to find specific classes (`AutoSuggestTextArea`) and directly send text to them.

## Status
- **Last Updated**: 2025-12-11
- **Version**: v0.1.0 (Alpha)
- **State**: Experimental (May be unstable)

## Feature Details

### 1. Type Text (AutoSuggestTextArea)
- **Description**: Automatically detects the chat input field (text box) and enters any string.
- **Technology**: Uses the `SendKeys` method without using the clipboard, so it is less likely to interfere with other tasks.
- **Target**: Recursively searches for elements with the ClassName `AutoSuggestTextArea`.

### 2. Send 'Enter' Key
- **Description**: Programmatically sends an `Enter` key press event to the input field.
- **Purpose**: Used to send messages without clicking the send button.

## Usage

1. Open the talk screen with the person you want to send a message to in LINE.
2. Select the **"Automation"** tab.
3. Enter the text you want to send in the text box.
4. Click **"Type Text"** -> Text enters the input field.
5. Click **"Send 'Enter' Key"** -> Message is sent.

## Notes
- If the class name (`AutoSuggestTextArea`) changes due to a LINE version update, this feature will stop working.
- In that case, you need to find the new class name using the **UI Inspector**.

## Changelog

| Version | Date | Description |
|:---|:---|:---|
| v0.1.0 | 2025-12-11 | Initial release. Implementation of basic text sending functionality. |
