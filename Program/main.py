#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, simpledialog
from task import task_data   
from datetime import datetime, date
import json
import os

TASKS_FILE = "tasks.json"


class TaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Master")
        self.geometry("1920x1080")
        self.tasks = []
        self.create_widgets()
        self.load_tasks()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    def create_widgets(self):
        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

        self.remove_button = tk.Button(self, text="Remove Task", command=self.remove_completed_tasks)
        self.remove_button.pack(pady=10)

        self.task_listbox = tk.Listbox(self, width=60)
        self.task_listbox.pack(pady=10)

        self.complete_button = tk.Button(self, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(pady=10)


    # Save tasks function #

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2, default=str)

    def on_close(self):
        self.save_tasks()
        self.destroy()


    #Loading task function #

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [task_data.from_dict(d) for d in data]
                self.refresh_tasks()


    # Add task function #

    def add_task(self):
        title = simpledialog.askstring("Task Title", "Enter task title:")
        if not title:
            return
        priority = simpledialog.askinteger("Priority", "Enter priority (1-5):", minvalue=1, maxvalue=5)
        deadline_str = simpledialog.askstring("Deadline", "Enter deadline (YYYY-MM-DD):")
        has_description_bool = messagebox.askyesno("Task Description", "Do you want to add a description?")
        description_str = ""
        if has_description_bool:
            description_str = simpledialog.askstring("Description", "Enter task description:") 
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except Exception:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
            return
        task = task_data(title, priority, deadline, False, has_description_bool, description_str)
        self.tasks.append(task)
        self.refresh_tasks()

     # Remove task function #

    def remove_completed_tasks(self):
        index = self.task_listbox.curselection()
        if not index:
            return
        del self.tasks[index[0]]
        self.refresh_tasks()

    
     # Refresh function #     
    def refresh_tasks(self):
        self.tasks.sort(key=lambda t: (t.completed, t.priority, t.description, t.deadline if t.deadline else datetime.date.max ))
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task.completed else "✗"
            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
            display = f"[{status}] {task.title} (Priority: {task.priority} Deadline: {deadline_str}) Description: {task.description}"
            self.task_listbox.insert(tk.END, display)

    # Task completion check box function #
    def complete_task(self):
        index = self.task_listbox.curselection()
        if not index:
            return
        task = self.tasks[index[0]]
        task.completed = not task.completed
        self.refresh_tasks()

if __name__ == "__main__":
    app = TaskApp()
    app.mainloop()