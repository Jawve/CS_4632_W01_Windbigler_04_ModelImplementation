import pyautogui
import tkinter as tk
from tkinter import simpledialog, messagebox, Button, Label, Frame, Toplevel, Checkbutton, IntVar
import threading
import time
import keyboard


class ParameterDialog(tk.Toplevel):
    def __init__(self, parent, x, y, duration, on_update_callback, on_save_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Edit Event Parameters")
        self.geometry("300x250")
        self.resizable(False, False)

        self.on_update_callback = on_update_callback
        self.on_save_callback = on_save_callback

        Label(self, text="X Coordinate:").pack(pady=5)
        self.x_entry = tk.Entry(self)
        self.x_entry.pack(pady=5)
        self.x_entry.insert(0, str(x))

        Label(self, text="Y Coordinate:").pack(pady=5)
        self.y_entry = tk.Entry(self)
        self.y_entry.pack(pady=5)
        self.y_entry.insert(0, str(y))

        Label(self, text="Duration (seconds):").pack(pady=5)
        self.duration_entry = tk.Entry(self)
        self.duration_entry.pack(pady=5)
        self.duration_entry.insert(0, str(duration))

        self.x_entry.bind("<KeyRelease>", self.update_ghost)
        self.y_entry.bind("<KeyRelease>", self.update_ghost)

        Button(self, text="Save and Apply Changes", command=self.save_changes).pack(pady=10)

    def update_ghost(self, event=None):
        try:
            x = int(self.x_entry.get()) if self.x_entry.get() else 0
            y = int(self.y_entry.get()) if self.y_entry.get() else 0
            self.on_update_callback(x, y)
        except ValueError:
            pass

    def save_changes(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            duration = float(self.duration_entry.get())
            self.on_save_callback(x, y, duration)
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values.")


class MouseMacroBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Macro Builder")
        self.root.geometry("900x600")

        self.events = []
        self.ghost_mouse_window = None
        self.repeat_events = IntVar()  # Checkbox state to repeat events

        # Layout
        self.left_frame = Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        self.middle_frame = Frame(self.root)
        self.middle_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Event List
        Label(self.left_frame, text="Event List").pack()
        self.event_listbox = tk.Listbox(self.left_frame, selectmode=tk.SINGLE, width=60, height=25)
        self.event_listbox.pack(fill=tk.BOTH, expand=True)
        self.event_listbox.bind("<<ListboxSelect>>", self.on_event_select)

        Button(self.left_frame, text="Remove Event", command=self.remove_event).pack(pady=10)

        Checkbutton(self.left_frame, text="Repeat Events", variable=self.repeat_events).pack(pady=5)

        # Add Event Buttons
        Label(self.middle_frame, text="Add Events").pack()
        self.function_buttons = ["Click Down", "Click Up", "Right Click Down", "Right Click Up", "Wait"]
        for function in self.function_buttons:
            btn = Button(self.middle_frame, text=function, width=20, command=lambda f=function: self.prompt_event(f))
            btn.pack(pady=5)

        # Playback Buttons
        Button(self.root, text="Play Events", command=lambda: threading.Thread(target=self.play_events).start()).pack(side=tk.BOTTOM, pady=10)

    def prompt_event(self, event_type):
        """
        Prompt the user to input parameters for a new event.
        """
        def update_ghost(x, y, duration=None):
            self.show_ghost_mouse(x, y)

        def finalize_input(x, y, duration):
            event = {'type': event_type.lower().replace(" ", "_"), 'x': x, 'y': y, 'duration': duration}
            self.events.append(event)
            self.event_listbox.insert(tk.END, f"{event_type} - X: {x}, Y: {y}, Duration: {duration}")
            self.show_ghost_mouse(0, 0)  # Reset ghost mouse after confirming

        # Mimic the most recent relevant event's parameters
        x, y, duration = 0, 0, 0
        if "up" in event_type.lower():
            matching_down = "click_down" if "left" in event_type.lower() else "right_click_down"
            for event in reversed(self.events):
                if event['type'] == matching_down:
                    x, y, duration = event['x'], event['y'], event['duration']
                    break

        ParameterDialog(
            self.root,
            x=x,
            y=y,
            duration=duration,
            on_update_callback=update_ghost,
            on_save_callback=finalize_input,
        )

    def on_event_select(self, event):
        """
        Allow the user to edit the parameters of an existing event.
        """
        selected_index = self.event_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            selected_event = self.events[index]

            def update_ghost(x, y, duration=None):
                self.show_ghost_mouse(x, y)

            def save_changes(x, y, duration):
                selected_event['x'] = x
                selected_event['y'] = y
                selected_event['duration'] = duration
                self.event_listbox.delete(index)
                self.event_listbox.insert(index, f"{selected_event['type']} - X: {x}, Y: {y}, Duration: {duration}")

            ParameterDialog(
                self.root,
                x=selected_event['x'],
                y=selected_event['y'],
                duration=selected_event['duration'],
                on_update_callback=update_ghost,
                on_save_callback=save_changes,
            )

    def remove_event(self):
        selected_index = self.event_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.event_listbox.delete(index)
            self.events.pop(index)
            if self.ghost_mouse_window:
                self.ghost_mouse_window.destroy()
            messagebox.showinfo("Remove Event", "Event removed successfully!")

    def show_ghost_mouse(self, x, y):
        """
        Display a ghost marker on the screen to indicate where the event takes place.
        """
        # Close existing ghost marker
        if self.ghost_mouse_window:
            self.ghost_mouse_window.destroy()

        if x != 0 or y != 0:
            # Create a new ghost marker
            self.ghost_mouse_window = Toplevel(self.root)
            self.ghost_mouse_window.overrideredirect(True)
            self.ghost_mouse_window.attributes("-topmost", True)
            self.ghost_mouse_window.attributes("-alpha", 0.5)  # Transparency

            # Set marker size and position
            self.ghost_mouse_window.geometry(f"20x20+{x-10}+{y-10}")
            ghost_label = Label(self.ghost_mouse_window, bg="red")
            ghost_label.pack(fill=tk.BOTH, expand=True)

    def play_events(self):
        if not self.events:
            messagebox.showwarning("Playback", "No recorded events to play back!")
            return

        repeat = self.repeat_events.get()  # Check if repeat is enabled
        stop = False

        while not stop:
            for event in self.events:
                if keyboard.is_pressed("a") and keyboard.is_pressed("s"):
                    stop = True
                    break

                x = event['x']
                y = event['y']
                duration = event['duration']
                event_type = event['type']

                if event_type == 'click_down':
                    pyautogui.mouseDown(x, y, button='left')
                elif event_type == 'click_up':
                    pyautogui.mouseUp(x, y, button='left')
                elif event_type == 'right_click_down':
                    pyautogui.mouseDown(x, y, button='right')
                elif event_type == 'right_click_up':
                    pyautogui.mouseUp(x, y, button='right')
                elif event_type == 'wait':
                    time.sleep(duration)

            if not repeat:
                break

        messagebox.showinfo("Playback Complete", "All events have been executed!")


if __name__ == "__main__":
    root = tk.Tk()
    app = MouseMacroBuilderApp(root)
    root.mainloop()
