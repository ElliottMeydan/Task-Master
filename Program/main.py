import tkinter as tk
from tkinter import messagebox, simpledialog
from task import task_data   
from datetime import datetime

class TaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Master")
        self.geometry("500x400")
        self.tasks = []
        self.create_widgets()
    def create_widgets(self):
        self.add_button = tk.Button(self, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=10)

        self.remove_button = tk.Button(self, text="Remove Task", command=self.remove_completed_tasks)
        self.remove_button.pack(pady=10)

        self.task_listbox = tk.Listbox(self, width=60)
        self.task_listbox.pack(pady=10)

        self.complete_button = tk.Button(self, text="Complete Task", command=self.complete_task)
        self.complete_button.pack(pady=10)


    # Add task function #

    def add_task(self):
        title = simpledialog.askstring("Task Title", "Enter task title:")
        if not title:
            return
        priority = simpledialog.askinteger("Priority", "Enter priority (1-5):", minvalue=1, maxvalue=5)
        deadline_str = simpledialog.askstring("Deadline", "Enter deadline (YYYY-MM-DD):")
        try:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except Exception:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
            return
        task = task_data(title, priority, deadline)
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
        self.tasks.sort(key=lambda t: (t.completed, t.priority, t.deadline if t.deadline else datetime.date.max ))
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task.completed else "✗"
            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
            display = f"[{status}] {task.title} (Priority: {task.priority} Deadline: {deadline_str})"
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