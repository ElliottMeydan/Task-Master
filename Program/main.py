#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from task import task_data   
from datetime import datetime, date
import json
import os

TASKS_FILE = "tasks.json"

# UI Design #

def draw_gradient(canvas, width, height, color1, color2):
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    r_ratio = float(r2 - r1) / height
    g_ratio = float(g2 - g1) / height
    b_ratio = float(b2 - b1) / height

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f"#{nr//256:02x}{ng//256:02x}{nb//256:02x}"
        canvas.create_line(0, i, width, i, fill=color)

class buttons(tk.Button):
    def __init__(self, master=None, bg="#4da6ff", active="#3399ff", fg="#ffffff", **kwargs):
        super().__init__(master, bd=0, relief="flat", fg=fg, bg=bg, activebackground=active, **kwargs)
        self._bg = bg
        self._active = active
        self._hover = self._shade(bg, -10)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event=None):
        try:
            self.configure(bg=self._hover)
        except Exception:
            pass

    def _on_leave(self, _event=None):
        try:
            self.configure(bg=self._bg)
        except Exception:
            pass

    @staticmethod
    def _shade(hexcolor, percent):
        hexcolor = hexcolor.lstrip("#")
        r = int(hexcolor[0:2], 16)
        g = int(hexcolor[2:4], 16)
        b = int(hexcolor[4:6], 16)
        def clamp(v): return max(0, min(255, v))
        r = clamp(int(r + (percent / 100.0) * 255))
        g = clamp(int(g + (percent / 100.0) * 255))
        b = clamp(int(b + (percent / 100.0) * 255))
        return f"#{r:02x}{g:02x}{b:02x}"


# Main application class #

class TaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Master")
        width, height = 350, 500
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)

    
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        win_w = self.winfo_width()
        win_h = self.winfo_height()
        x = screen_width - win_w - 12
        y = screen_height - win_h - 48
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        draw_gradient(self.canvas, width, height, "#eaf6ff", "#d9f0ff") 

        self.content = tk.Frame(self.canvas, bg="#ffffff", bd=0, highlightthickness=0)
        self.content.place(relx=0.5, rely=0.5, anchor="center", width=width - 32, height=height - 40)

        header_frame = tk.Frame(self.content, bg="#f0fbff")
        header_frame.pack(fill="x", padx=12, pady=(12, 6))
        title_label = tk.Label(header_frame, text="Task Master", bg="#f0fbff", fg="#0b5fa5",
                               font=("Segoe UI", 16, "bold"))
        title_label.pack(side="left", padx=(8, 0))
        subtitle = tk.Label(header_frame, text="Get those tasks done!", bg="#f0fbff", fg="#3a7fb2",
                            font=("Segoe UI", 9))
        subtitle.pack(side="left", padx=(12, 0))

        btn_frame = tk.Frame(self.content, bg="#ffffff")
        btn_frame.pack(fill="x", padx=12, pady=(6, 6))

        add_btn = buttons(btn_frame, text="＋ Add Task", font=("Segoe UI", 11, "bold"),
                              bg="#4da6ff", active="#3399ff", fg="#ffffff", command=self.add_task)
        add_btn.pack(side="left", expand=True, fill="x", padx=(0, 6), ipady=8)

        complete_btn = buttons(btn_frame, text="✓ Toggle Complete", font=("Segoe UI", 11, "bold"),
                                   bg="#6cc0ff", active="#4db8ff", fg="#ffffff", command=self.complete_task)
        complete_btn.pack(side="left", expand=True, fill="x", padx=(6, 0), ipady=8)

        list_frame = tk.Frame(self.content, bg="#ffffff")
        list_frame.pack(fill="both", expand=True, padx=12, pady=(6, 6))

        self.task_listbox = tk.Listbox(list_frame, bd=0, highlightthickness=0, font=("Segoe UI", 11),
                                       bg="#fbfeff", fg="#133b55", selectbackground="#cfeeff", relief="flat")
        self.task_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        bottom_frame = tk.Frame(self.content, bg="#ffffff")
        bottom_frame.pack(fill="x", padx=12, pady=(6, 12))

        remove_btn = buttons(bottom_frame, text="🗑 Remove Selected", font=("Segoe UI", 10, "bold"),
                                 bg="#ff7b7b", active="#ff5c5c", fg="#ffffff", command=self.remove_completed_tasks)
        remove_btn.pack(side="left", expand=True, fill="x", padx=(0, 6), ipady=8)

        save_btn = buttons(bottom_frame, text="💾 Save", font=("Segoe UI", 10, "bold"),
                               bg="#3dbb8f", active="#2fae7a", fg="#ffffff", command=self.save_tasks)
        save_btn.pack(side="left", expand=True, fill="x", padx=(6, 0), ipady=8)

        self.tasks = []
        self.load_tasks()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

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
        if priority is None:
            return
        has_deadline_bool = messagebox.askyesno("Deadline", "Do you want to add a deadline?")
        has_description_bool = messagebox.askyesno("Task Description", "Do you want to add a description?")
        description_str = ""
        deadline = None
        if has_deadline_bool:
            deadline_str = simpledialog.askstring("Deadline", "Enter deadline (YYYY-MM-DD):")
            if not deadline_str:
                has_deadline_bool = False
                deadline = None
            else:
                try:
                    deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                except Exception:
                    messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
                    return
        if has_description_bool:
            description_str = simpledialog.askstring("Description", "Enter task description:") or ""
        task = task_data(title, priority, has_deadline_bool, deadline, False, has_description_bool, description_str)
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
        self.tasks.sort(key=lambda t: (t.completed, t.priority, t.description, t.deadline))
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