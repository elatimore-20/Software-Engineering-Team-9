import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
import threading
import time

class Task:
    def __init__(self, description, date_time):
        self.description = description
        self.date_time = date_time
        self.completed = False

class TaskMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Monitor App")

        self.tasks = []

        self.create_main_menu()

        self.reminder_thread = threading.Thread(target=self.check_reminders)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()

    def create_main_menu(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.pack_forget()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(padx=20, pady=20)

        btn_add_task = tk.Button(self.current_frame, text="Add Task", command=self.show_add_task_screen)
        btn_add_task.pack(pady=10)

        btn_delete_task = tk.Button(self.current_frame, text="Delete Task", command=self.show_delete_task_screen)
        btn_delete_task.pack(pady=10)

        btn_display_tasks = tk.Button(self.current_frame, text="Display Tasks", command=self.show_check_tasks_screen)
        btn_display_tasks.pack(pady=10)

        btn_mark_complete = tk.Button(self.current_frame, text="Mark as Complete", command=self.show_mark_complete_screen)
        btn_mark_complete.pack(pady=10)

        btn_exit = tk.Button(self.current_frame, text="Exit Task Monitor", command=self.root.quit)
        btn_exit.pack(pady=10)

    def show_add_task_screen(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.pack_forget()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(padx=20, pady=20)

        lbl_title = tk.Label(self.current_frame, text="Add Task", font=("Helvetica", 16))
        lbl_title.pack(pady=10)

        lbl_task = tk.Label(self.current_frame, text="Task:")
        lbl_task.pack(pady=5)
        self.entry_task = tk.Entry(self.current_frame, width=50)
        self.entry_task.pack(pady=5)

        lbl_date = tk.Label(self.current_frame, text="Date:")
        lbl_date.pack(pady=5)
        self.entry_date = tk.Entry(self.current_frame, width=20)
        self.entry_date.pack(pady=5)

        lbl_time = tk.Label(self.current_frame, text="Time:")
        lbl_time.pack(pady=5)
        self.entry_time = tk.Entry(self.current_frame, width=10)
        self.entry_time.pack(pady=5)

        self.am_pm_var = tk.StringVar(value="AM")
        am_radio = tk.Radiobutton(self.current_frame, text="AM", variable=self.am_pm_var, value="AM")
        am_radio.pack(side=tk.LEFT, padx=10)
        pm_radio = tk.Radiobutton(self.current_frame, text="PM", variable=self.am_pm_var, value="PM")
        pm_radio.pack(side=tk.LEFT, padx=10)

        btn_add = tk.Button(self.current_frame, text="Add Task", command=self.add_task)
        btn_add.pack(pady=10)

        btn_back = tk.Button(self.current_frame, text="Back to Menu", command=self.create_main_menu)
        btn_back.pack(pady=10)

    def add_task(self):
        description = self.entry_task.get()
        date_str = self.entry_date.get()
        time_str = self.entry_time.get()
        am_pm = self.am_pm_var.get()

        try:
            date_time_str = f"{date_str} {time_str} {am_pm}"
            date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %I:%M %p")
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format. Please use YYYY-MM-DD HH:MM AM/PM.")
            return

        task = Task(description, date_time)
        self.tasks.append(task)

        messagebox.showinfo("Success", "Task added successfully.")

        self.entry_task.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        self.entry_time.delete(0, tk.END)

    def show_delete_task_screen(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.pack_forget()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(padx=20, pady=20)

        lbl_title = tk.Label(self.current_frame, text="Delete Task", font=("Helvetica", 16))
        lbl_title.pack(pady=10)

        self.listbox_tasks = tk.Listbox(self.current_frame, width=70)
        self.listbox_tasks.pack(pady=10)

        for task in self.tasks:
            self.listbox_tasks.insert(tk.END, task.description)

        btn_delete = tk.Button(self.current_frame, text="Delete Selected Task", command=self.delete_task)
        btn_delete.pack(pady=10)

        btn_back = tk.Button(self.current_frame, text="Back to Menu", command=self.create_main_menu)
        btn_back.pack(pady=10)

    def delete_task(self):
        selected_index = self.listbox_tasks.curselection()

        if not selected_index:
            return

        task_index = selected_index[0]
        task = self.tasks[task_index]

        confirmed = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{task.description}'?")

        if confirmed:
            self.tasks.pop(task_index)
            self.update_listbox()

    def show_check_tasks_screen(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.pack_forget()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(padx=20, pady=20)

        lbl_title = tk.Label(self.current_frame, text="Tasks", font=("Helvetica", 16))
        lbl_title.pack(pady=10)

        self.listbox_tasks = tk.Listbox(self.current_frame, width=70)
        self.listbox_tasks.pack(pady=10)

        for task in self.tasks:
            task_info = f"{task.description} - {task.date_time.strftime('%Y-%m-%d %H:%M')} - {'Completed' if task.completed else 'Pending'}"
            self.listbox_tasks.insert(tk.END, task_info)

        btn_back = tk.Button(self.current_frame, text="Back to Menu", command=self.create_main_menu)
        btn_back.pack(pady=10)

    def show_mark_complete_screen(self):
        if hasattr(self, 'current_frame'):
            self.current_frame.pack_forget()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(padx=20, pady=20)

        lbl_title = tk.Label(self.current_frame, text="Mark Complete", font=("Helvetica", 16))
        lbl_title.pack(pady=10)

        self.listbox_tasks = tk.Listbox(self.current_frame, width=70)
        self.listbox_tasks.pack(pady=10)

        for task in self.tasks:
            self.listbox_tasks.insert(tk.END, task.description)

        btn_mark_complete = tk.Button(self.current_frame, text="Mark Selected Task as Complete", command=self.mark_task_complete)
        btn_mark_complete.pack(pady=10)

        btn_back = tk.Button(self.current_frame, text="Back to Menu", command=self.create_main_menu)
        btn_back.pack(pady=10)

    def mark_task_complete(self):
        selected_index = self.listbox_tasks.curselection()

        if not selected_index:
            return

        task_index = selected_index[0]
        task = self.tasks[task_index]

        task.completed = True
        self.update_listbox()

    def update_listbox(self):
        if hasattr(self, 'listbox_tasks'):
            self.listbox_tasks.delete(0, tk.END)

            for task in self.tasks:
                self.listbox_tasks.insert(tk.END, task.description)

    def check_reminders(self):
        while True:
            current_time = datetime.datetime.now()

            for task in self.tasks:
                if not task.completed:
                    time_difference = task.date_time - current_time

                    if datetime.timedelta(hours=24) <= time_difference < datetime.timedelta(hours=25):
                        messagebox.showinfo("Reminder", f"Reminder: 24 hours until '{task.description}'.")

                    elif datetime.timedelta(hours=0) <= time_difference < datetime.timedelta(hours=1):
                        messagebox.showinfo("Reminder", f"Reminder: It's time for '{task.description}'.")

            time.sleep(60)

root = tk.Tk()
app = TaskMonitorApp(root)
root.mainloop()