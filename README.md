# Mouse Macro Builder

Mouse Macro Builder is a small desktop automation tool that lets you **build and play back mouse macros** from a simple GUI. Users create a sequence of events (mouse button down/up, right click down/up, and waits), preview click positions with an on-screen marker, and then run the macro to reproduce repetitive tasks.

Built as a school/simulation assignment and packaged for convenient use.

## Features

- **GUI-based macro editor** (Tkinter)
- Add events to a macro:
  - Left Click Down / Up
  - Right Click Down / Up
  - Wait (delay)
- **Editable event parameters** (X, Y, Duration) via an “Edit Event Parameters” dialog
- **On-screen click preview** (“ghost marker”)
  - Displays a semi-transparent red square at the selected coordinates
- **Playback** in a background thread (keeps UI responsive)
- **Repeat mode** (optional): loop the event list until stopped
- **Emergency stop hotkey:** press **A + S** to stop playback immediately

## How It Works

1. Use the **Add Events** buttons to create macro steps.
2. For each step, set:
   - `X` and `Y` screen coordinates
   - `Duration` (used for wait timing; stored for each event)
3. A semi-transparent red marker appears at the chosen coordinates to preview click location.
4. Click **Play Events** to execute the macro in order.
5. Enable **Repeat Events** to loop continuously until you stop it with **A + S**.

## Requirements

- Python 3.x
- Dependencies:
  - `pyautogui`
  - `keyboard`

> Note: On some systems, global hotkeys and mouse automation may require admin privileges or accessibility permissions.

## Run Locally

```bash
python MouseMacroBuilder.py
