import tkinter as tk
from tkinter import ttk
import sv_ttk
from pynput import keyboard
import threading
from clipthread.db import DatabaseHandler
import pyperclip


class TableWindow:
    def __init__(self):
        self.uuid_to_complete = {}

        # Initialize database
        self.db = DatabaseHandler()
        self.db.create_table()

        # create main windows
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry('300x200+100+100')
        
        # Flag to track window visibility
        self.is_visible = True

        # Apply modern theme
        sv_ttk.set_theme("dark")  # or "light" for light theme
        
        # Configure styles
        self.style = ttk.Style()
        
        # Style for the main frame
        self.style.configure('Main.TFrame', background='#2b2b2b')
        
        # Style for the Treeview
        self.style.configure("Treeview",
                           background="#2b2b2b",
                           foreground="white",
                           fieldbackground="#2b2b2b",
                           rowheight=25)
        
        # Style for Treeview headings
        self.style.configure("Treeview.Heading",
                           background="#404040",
                           foreground="white",
                           relief="flat")
        self.style.map("Treeview.Heading",
                      background=[('active', '#404040')])
        
        # Style for buttons
        self.style.configure("Accent.TButton",
                           padding=10)
        
        # Create main container with padding and styled
        self.container = ttk.Frame(self.root, style='Main.TFrame')
        self.container.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Container and table setup
        self.container = ttk.Frame(self.root)
        self.container.pack(fill='both', expand=True, padx=2, pady=2)
        
        table_frame = ttk.Frame(self.container)
        table_frame.pack(fill='both', expand=True)
        
        self.tree = ttk.Treeview(table_frame, 
                                columns=('UUID', 'Value'),
                                show='headings',
                                selectmode='browse')
        
        self.tree.heading('UUID', text='UUID')
        self.tree.heading('Value', text='Value')
        
        self.tree.column('UUID', width=50, stretch=True)
        self.tree.column('Value', width=200, stretch=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', 
                                command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add control buttons
        button_frame = ttk.Frame(self.container)
        button_frame.pack(fill='x', pady=5)
        ttk.Button(
            button_frame,
            text="Clear",
            style="Accent.TButton",
            command=self.clear_data).pack(side='right', padx=5)
        
        self.tree.bind('<ButtonRelease-1>', self.on_click)
        
        # Configure window resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Set up hotkey listener in a separate thread
        self.setup_hotkey()
        self.refresh_data()

        # overwrite the default close behavior to hide the window instead
        self.root.protocol("WM_DELETE_WINDOW", self.toggle_window)

    def toggle_window(self):
        if self.is_visible:
            self.root.withdraw()  # Hide window
        else:
            self.root.deiconify()  # Show window
        self.is_visible = not self.is_visible

    def setup_hotkey(self):
        def on_press(key):
            try:
                # Check for Ctrl + Alt + [
                if key == keyboard.KeyCode.from_char('['):
                    if keyboard.Key.ctrl.value in self.current_keys and keyboard.Key.alt.value in self.current_keys:
                        # Use after() to safely interact with tkinter from another thread
                        self.root.after(0, self.toggle_window)

                # Check for Ctrl + C
                if key == keyboard.KeyCode.from_char('c'):
                    if keyboard.Key.ctrl.value in self.current_keys:
                        # Get the clipboard content
                        clipboard_content = pyperclip.paste()
                        # print(f"Clipboard content: {clipboard_content}")

                        # insert the clipboard content into the database
                        self.db.insert(clipboard_content)
                        self.refresh_data()


            except AttributeError:
                print(f"Unknown key: {key}")

        def on_release(key):
            try:
                if key.value in self.current_keys:
                    self.current_keys.remove(key.value)
            except AttributeError:
                pass

        # Set to keep track of currently pressed keys
        self.current_keys = set()

        def for_canonical(f):
            return lambda k: f(listener.canonical(k))

        def on_press_with_tracking(key):
            try:
                self.current_keys.add(key.value)
            except AttributeError:
                pass
            on_press(key)

        # Start keyboard listener in a separate thread
        listener = keyboard.Listener(
            on_press=for_canonical(on_press_with_tracking),
            on_release=for_canonical(on_release))
        listener.daemon = True
        listener.start()

    def on_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item)['values']
        print(f"Clicked row with values: {values}")

        # copy the value to the clipboard
        self.db.get(values[0])
        pyperclip.copy(self.uuid_to_complete[values[0]])

    def clear_data(self):
        """Clear all rows from the database and refresh the display"""
        self.db.clear()
        self.refresh_data()

    def truncate_text(self, text, limit=25):
        """Truncate text if longer than limit and add ellipsis"""
        return (text[:limit] + '...') if len(text) > limit else text

    def refresh_data(self):
        """Refresh the table data from database"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Load data from database
        rows = self.db.read_rows()
        for row in rows:
            self.uuid_to_complete[row[0]] = row[1]

            truncated_row = list(row)
            truncated_row[1] = self.truncate_text(str(row[1]))
            self.tree.insert('', 'end', values=truncated_row)
    
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = TableWindow()
    app.run()