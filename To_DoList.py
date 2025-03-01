
import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime
from PIL import Image, ImageTk  # Requires Pillow library

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("1000x700")  # Increased window size
        self.root.minsize(800, 600)     # Increased minimum size
        
        # Colors - Navy blue theme
        self.primary_color = "#1a237e"  # Dark navy blue
        self.secondary_color = "#303f9f"  # Medium navy blue
        self.bg_color = "#e8eaf6"  # Light indigo/blue background
        self.accent_color = "#c5cae9"  # Very light indigo
        self.text_color = "#ffffff"  # White text for dark backgrounds
        self.dark_text = "#263238"  # Dark text for light backgrounds
        
        # Set up background image
        self.setup_background()
            
        # Font styles
        self.header_font = ("Arial", 24, "bold")
        self.normal_font = ("Arial", 12)
        self.list_font = ("Arial", 14)
        
        self.create_header()
        self.create_task_frame()
        self.create_button_row()  # Buttons in a row
        self.create_status_bar()
        
        # Load saved tasks at startup
        self.load_tasks()
        
    def setup_background(self):
        # Initialize main_frame to root as default
        self.main_frame = self.root
        self.root.configure(bg=self.bg_color)
        
        # Try various file extensions
        possible_paths = [
            'blue.jpeg',
            # 'myimage.avif',
            # 'myimage.png',
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blue.jpeg'),
            # os.path.join(os.path.dirname(os.path.abspath(__file__)), 'myimage.avif'),
            # os.path.join(os.path.dirname(os.path.abspath(__file__)), 'myimage.png')
        ]
        
        # Try each possible path
        for bg_image_path in possible_paths:
            try:
                print(f"Trying to load image from: {bg_image_path}")
                if os.path.exists(bg_image_path):
                    original_image = Image.open(bg_image_path)
                    print(f"Successfully loaded image from: {bg_image_path}")
                    
                    # Resize image to fit the window
                    width, height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
                    resized_image = original_image.resize((width, height), Image.LANCZOS)
                    
                    # Convert PIL image to Tkinter PhotoImage
                    self.bg_image = ImageTk.PhotoImage(resized_image)
                    
                    # Create a label with the image
                    background_label = tk.Label(self.root, image=self.bg_image)
                    background_label.place(x=0, y=0, relwidth=1, relheight=1)
                    
                    # Set this label as the main container
                    self.main_frame = background_label
                    
                    # Stop searching after finding a valid image
                    return
                
            except Exception as e:
                print(f"Failed to load image from {bg_image_path}: {e}")
        
        # If we get here, all attempts failed
        print("Could not load background image from any path, using default background")
        self.main_frame = self.root
        self.root.configure(bg=self.bg_color)
        
    def create_header(self):
        # Header frame
        header_frame = tk.Frame(self.main_frame, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X)
        
        # App title
        title_label = tk.Label(
            header_frame, 
            text="Task Manager", 
            font=self.header_font,
            bg=self.primary_color,
            fg=self.text_color,
            pady=15
        )
        title_label.pack()
        
        # Current date
        date_str = datetime.now().strftime("%A, %B %d, %Y")
        date_label = tk.Label(
            header_frame,
            text=date_str,
            font=("Arial", 10),
            bg=self.primary_color,
            fg=self.text_color
        )
        date_label.place(relx=1.0, rely=1.0, x=-10, y=-5, anchor="se")
        
    def create_task_frame(self):
        # Main content frame
        content_frame = tk.Frame(self.main_frame, bg=self.bg_color)  # Fixed: Empty bg value
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        content_bg = tk.Frame(content_frame, bg=self.accent_color)
        # Semi-transparent overlay for better readability
        content_bg.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Task input area
        input_frame = tk.Frame(content_frame, bg=self.bg_color)  # Fixed: Empty bg value
        input_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            input_frame, 
            text="New Task:", 
            font=self.normal_font, 
            bg=self.bg_color,  # Fixed: Empty bg value
            fg=self.dark_text
        ).pack(side=tk.LEFT, padx=5)
        
        self.task_entry = tk.Entry(
            input_frame, 
            font=self.normal_font,
            bd=1,
            relief=tk.SOLID
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        # Styled Add button
        add_btn = tk.Button(
            input_frame, 
            text="Add Task",
            command=self.add_task,
            font=self.normal_font,
            bg=self.primary_color,
            fg=self.text_color,
            relief=tk.RAISED,
            padx=15,
            pady=5,
            activebackground=self.secondary_color,
            activeforeground=self.text_color
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Separator
        separator = tk.Frame(content_frame, height=2, bg=self.secondary_color)
        separator.pack(fill=tk.X, pady=10)
        
        # Task list with scrollbar in a frame
        list_frame = tk.Frame(content_frame, bg=self.bg_color)  # Fixed: Empty bg value
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a frame with white semi-transparent background for the list
        list_bg = tk.Frame(list_frame, bg='white')
        list_bg.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame, bg=self.secondary_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Task list
        self.task_list = tk.Listbox(
            list_frame,
            font=self.list_font,
            bg='white',
            fg=self.dark_text,
            bd=0,
            relief=tk.FLAT,
            selectbackground=self.secondary_color,
            selectforeground=self.text_color,
            activestyle="none",
            highlightthickness=0
        )
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Connect scrollbar and listbox
        self.task_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_list.yview)
        
    def create_button_row(self):
        # Create a frame for buttons in a row
        button_frame = tk.Frame(self.main_frame, bg=self.bg_color, height=60)  # Fixed: Empty bg value
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Define buttons to create
        buttons = [
            ("Remove Selected", self.remove_task),
            ("Mark as Complete", self.mark_complete),
            ("Clear All Tasks", self.clear_tasks),
            ("Save Tasks", self.save_tasks),
            ("Load Tasks", self.load_tasks)
        ]
        
        # Create and place buttons in a row
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=self.normal_font,
                bg=self.primary_color,
                fg=self.text_color,
                bd=0,
                relief=tk.RAISED,
                padx=15,
                pady=10,
                highlightthickness=0,
                activebackground=self.secondary_color,
                activeforeground=self.text_color,
                cursor="hand2",
                command=command
            )
            btn.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    
    def create_status_bar(self):
        # Status bar at the bottom
        status_frame = tk.Frame(self.main_frame, bg=self.primary_color, height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg=self.primary_color,
            fg=self.text_color,
            font=("Arial", 10),
            anchor="w",
            padx=10,
            pady=5
        )
        status_label.pack(side=tk.LEFT)
        
        # Task counter
        self.counter_var = tk.StringVar()
        self.counter_var.set("Tasks: 0")
        
        counter_label = tk.Label(
            status_frame,
            textvariable=self.counter_var,
            bg=self.primary_color,
            fg=self.text_color,
            font=("Arial", 10),
            anchor="e",
            padx=10,
            pady=5
        )
        counter_label.pack(side=tk.RIGHT)
    
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            # Add timestamp
            timestamp = datetime.now().strftime("%H:%M")
            task_with_time = f"[{timestamp}] {task}"
            
            self.task_list.insert(tk.END, task_with_time)
            self.task_entry.delete(0, tk.END)
            self.update_status(f"Task added: {task}")
            self.update_counter()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")
    
    def remove_task(self):
        try:
            selected_index = self.task_list.curselection()[0]
            task = self.task_list.get(selected_index)
            self.task_list.delete(selected_index)
            self.update_status(f"Task removed: {task}")
            self.update_counter()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove.")
    
    def mark_complete(self):
        try:
            selected_index = self.task_list.curselection()[0]
            task = self.task_list.get(selected_index)
            if not task.startswith("✓ "):
                self.task_list.delete(selected_index)
                self.task_list.insert(selected_index, f"✓ {task}")
                self.update_status(f"Task completed: {task}")
            else:
                # Unmark if already marked
                self.task_list.delete(selected_index)
                self.task_list.insert(selected_index, task[2:])
                self.update_status(f"Task unmarked: {task[2:]}")
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as complete.")
    
    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.task_list.delete(0, tk.END)
            self.update_status("All tasks cleared")
            self.update_counter()
    
    def save_tasks(self):
        tasks = self.task_list.get(0, tk.END)
        if not tasks:
            messagebox.showinfo("Info", "No tasks to save")
            return
            
        with open("tasks.txt", "w") as file:
            for task in tasks:
                file.write(f"{task}\n")
        
        self.update_status(f"Tasks saved to tasks.txt ({len(tasks)} tasks)")
        messagebox.showinfo("Success", f"{len(tasks)} tasks saved successfully")
    
    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                tasks = file.readlines()
                
            # Clear current list
            self.task_list.delete(0, tk.END)
            
            # Add tasks from file
            for task in tasks:
                self.task_list.insert(tk.END, task.strip())
                
            self.update_status(f"Loaded {len(tasks)} tasks from tasks.txt")
            self.update_counter()
            
        except FileNotFoundError:
            self.update_status("No saved tasks found")
    
    def update_status(self, message):
        self.status_var.set(message)
    
    def update_counter(self):
        count = self.task_list.size()
        self.counter_var.set(f"Tasks: {count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()