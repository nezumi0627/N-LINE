# Visual Style Injection (QSS)

## Overview
This feature allows you to forcefully change the appearance (UI design) of the LINE desktop app using **Qt Stylesheets (QSS)**. 
With CSS-like syntax, you can freely customize background colors, fonts, borders, button designs, and more.

## Status
- **Last Updated**: 2025-12-14
- **Version**: v0.2.0 (Released as an independent tab)
- **State**: Experimental (May be disabled by LINE version updates)

## How it Works
When starting LINE (an app built with the Qt framework), it injects the `-stylesheet` standard debug option and restarts it. 
This overwrites the app's internal default styles with an external file.

## Usage

### 1. Style Selection and Editing
When you open the **"Styles (QSS)"** tab, a file operation panel appears on the left and a simple editor on the right.

1. **Open File**: Select an existing `.qss` file using the "Browse File..." button.
2. **Edit**: The content is loaded into the editor on the right. You can edit colors and properties in real-time and save them with "Save Changes".

### 2. Deployment
Places the edited style in a location that is easy for LINE to load.

* **"Deploy to LINE Folder"**: Copies the currently selected file to LINE's local configuration folder (`AppData\Local\LINE`). 
* This simplifies path specifications and makes management easier.

### 3. Application (Inject & Relaunch)
1. When ready, click the **"Apply & Relaunch LINE"** button.
2. The LINE app will close once and restart while loading the specified stylesheet.

## Useful Features
* **Simple Editor**: Allows for minor color adjustments and other edits directly in the app without needing a separate text editor.
* **Automatic Path Resolution**: Automatically searches LINE's folders and completes the full path even if only the file name is entered.

## Notes
- **Restart**: This feature involves restarting the app. Do not execute it during calls or other important activities.
- **Reverting**: To revert to the default appearance, restart LINE from its normal shortcut or run "Launch LINE" from the N-LINE dashboard (it starts without arguments).
- **Identifying Class Names**: To find out which elements to apply styles to, use the **UI Inspector (Spy Mode)** to investigate `ClassName`.

## Changelog

| Version | Date | Description |
|:---|:---|:---|
| v0.2.1 | 2025-12-14 | Separated from Window Mods and created a dedicated tab. |
| v0.2.0 | 2025-12-14 | Initial implementation as part of Mods. |
