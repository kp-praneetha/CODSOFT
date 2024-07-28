import json
import os
from datetime import datetime

class Task:
    """Represents a single task with title, description, due date, and due time."""
    def __init__(self, title, description, due_date, due_time):
        self.title = title.lower()  # Make titles case-insensitive
        self.description = description
        self.due_date = due_date
        self.due_time = due_time
        self.completed = False

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}', '{self.due_date}', '{self.due_time}')"

class ToDoList:
    """Manages a list of tasks."""
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        """Adds a new task to the list."""
        self.tasks.append(task)

    def remove_task(self, task_title):
        """Removes a task by title."""
        self.tasks = [task for task in self.tasks if task.title != task_title.lower()]
        self.save_to_file("tasks.json")  # Save changes immediately

    def clear_tasks(self):
        """Removes all tasks from the list."""
        self.tasks = []
        self.save_to_file("tasks.json")  # Save changes immediately

    def update_task(self, task_title, new_title=None, new_description=None, new_due_date=None, new_due_time=None):
        """Updates a task by title."""
        for task in self.tasks:
            if task.title == task_title.lower():
                if new_title:
                    task.title = new_title.lower()
                if new_description:
                    task.description = new_description
                if new_due_date:
                    task.due_date = new_due_date
                if new_due_time:
                    task.due_time = new_due_time
                self.save_to_file("tasks.json")  # Save changes immediately
                break

    def save_to_file(self, filename):
        """Saves the task list to a file."""
        tasks_json = []
        for task in self.tasks:
            tasks_json.append({
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date,
                'due_time': task.due_time,
                'completed': task.completed
            })
        with open(filename, 'w') as f:
            json.dump(tasks_json, f)

    def load_from_file(self, filename):
        """Loads the task list from a file."""
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                tasks_json = json.load(f)
                self.tasks = []
                for task_json in tasks_json:
                    due_time = task_json.get('due_time', '12:00 PM')  # Default time if due_time is missing
                    task = Task(task_json['title'], task_json['description'], task_json['due_date'], due_time)
                    task.completed = task_json['completed']
                    self.tasks.append(task)

    def is_duplicate_title(self, title):
        """Checks for duplicate task titles."""
        return any(task.title == title.lower() for task in self.tasks)

def validate_date_time(date_text, time_text):
    try:
        due_date_time = f"{date_text} {time_text}"
        due_date = datetime.strptime(due_date_time, '%d-%m-%Y %I:%M %p')
        if due_date < datetime.now():
            print("Invalid due date: The date and time have already passed.")
            return False
        return due_date
    except ValueError:
        print("Invalid date/time format. Please use dd-mm-yyyy for date and HH:MM AM/PM for time.")
        return False

def display_time_left(due_date):
    now = datetime.now()
    time_left = due_date - now
    days_left = time_left.days
    hours_left = time_left.seconds // 3600
    print(f"Time left for the task: {days_left} days and {hours_left} hours")

def display_tasks(todo_list, display_details=False, task_index=None):
    if todo_list.tasks:
        if display_details and task_index is not None:
            task = todo_list.tasks[task_index]
            print(f"\nTask {task_index + 1}:")
            print(f"Title       : {task.title}")
            print(f"Description : {task.description}")
            print(f"Due Date    : {task.due_date}")
            print(f"Due Time    : {task.due_time}")
            due_date_time = f"{task.due_date} {task.due_time}"
            due_date = datetime.strptime(due_date_time, '%d-%m-%Y %I:%M %p')
            display_time_left(due_date)
        else:
            print("\nCurrent tasks:")
            for i, task in enumerate(todo_list.tasks):
                print(f"{i + 1}. {task.title}")
            print(f"Total tasks: {len(todo_list.tasks)}")
    else:
        print("The to-do list is empty. Please add a task first.")

def main():
    todo_list = ToDoList()

    filename = "tasks.json"
    if os.path.exists(filename):
        todo_list.load_from_file(filename)

    while True:
        print("\nTo-Do List App")
        print("1. Create a new task")
        print("2. Update a task")
        print("3. Remove a task")
        print("4. View tasks")
        print("5. Clear all tasks")
        print("6. Save tasks")
        print("7. Load tasks")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            while True:
                title = input("Enter task title: ")
                if todo_list.is_duplicate_title(title):
                    print("Duplicate task title. Please enter another title.")
                else:
                    break
            description = input("Enter task description: ")
            while True:
                due_date = input("Enter task due date (dd-mm-yyyy): ")
                due_time = input("Enter task due time (HH:MM): ")
                am_pm = input("Enter AM or PM: ").strip().upper()
                if am_pm not in ['AM', 'PM']:
                    print("Invalid input. Please enter either AM or PM.")
                    continue
                due_time = f"{due_time} {am_pm}"
                due_date_validated = validate_date_time(due_date, due_time)
                if due_date_validated:
                    display_time_left(due_date_validated)
                    task = Task(title, description, due_date_validated.strftime('%d-%m-%Y'), due_date_validated.strftime('%I:%M %p'))
                    todo_list.add_task(task)
                    print("Task added.")
                    print(f"Total tasks: {len(todo_list.tasks)}")
                    break
                else:
                    print("Invalid date or time. Please enter again.")
        elif choice in ['2', '3', '4', '6']:
            if not todo_list.tasks:
                print("The to-do list is empty. Please add a task first.")
            else:
                display_tasks(todo_list)
                if choice == '2':
                    task_num = int(input("Enter the number of the task to update: ")) - 1
                    if 0 <= task_num < len(todo_list.tasks):
                        task_title = todo_list.tasks[task_num].title
                        display_tasks(todo_list, display_details=True, task_index=task_num)
                        while True:
                            print("What do you want to update?")
                            print("1. Title")
                            print("2. Description")
                            print("3. Due Date")
                            print("4. Due Time")
                            update_choice = input("Enter your choice: ")

                            if update_choice == '1':
                                new_title = input("Enter new title: ")
                                if todo_list.is_duplicate_title(new_title):
                                    print("Duplicate task title. Please enter another title.")
                                else:
                                    todo_list.update_task(task_title, new_title=new_title)
                                    print("Task updated.")
                                break
                            elif update_choice == '2':
                                new_description = input("Enter new description: ")
                                todo_list.update_task(task_title, new_description=new_description)
                                print("Task updated.")
                                break
                            elif update_choice == '3':
                                new_due_date = input("Enter new due date (dd-mm-yyyy): ")
                                current_due_time = todo_list.tasks[task_num].due_time
                                if validate_date_time(new_due_date, current_due_time):
                                    todo_list.update_task(task_title, new_due_date=new_due_date)
                                    print("Task updated.")
                                else:
                                    print("Invalid input. Please enter a valid date.")
                                    break
                            elif update_choice == '4':
                                new_due_time = input("Enter new due time (HH:MM): ")
                                am_pm = input("Enter AM or PM: ").strip().upper()
                                if am_pm not in ['AM', 'PM']:
                                    print("Invalid input. Please enter either AM or PM.")
                                    break
                                new_due_time = f"{new_due_time} {am_pm}"
                                current_due_date = todo_list.tasks[task_num].due_date
                                if validate_date_time(current_due_date, new_due_time):
                                    todo_list.update_task(task_title, new_due_time=new_due_time)
                                    print("Task updated.")
                                else:
                                    print("Invalid input. Please enter a valid time.")
                                    break
                            else:
                                print("Invalid choice. Please enter a valid option.")
                                break
                    else:
                        print("Invalid task number.")
                elif choice == '3':
                    task_num = int(input("Enter the number of the task to remove: ")) - 1
                    if 0 <= task_num < len(todo_list.tasks):
                        task_title = todo_list.tasks[task_num].title
                        todo_list.remove_task(task_title)
                        print("Task removed.")
                        print(f"Total tasks: {len(todo_list.tasks)}")
                    else:
                        print("Invalid task number.")
                elif choice == '4':
                    task_num = int(input("Enter the number of the task to view details: ")) - 1
                    if 0 <= task_num < len(todo_list.tasks):
                        display_tasks(todo_list, display_details=True, task_index=task_num)
                    else:
                        print("Invalid task number.")
                elif choice == '6':
                    todo_list.save_to_file(filename)
                    print("Tasks saved.")

        elif choice == '5':
            if todo_list.tasks:
                confirm_clear = input("Are you sure you want to clear all tasks? (yes/no): ").lower()
                if confirm_clear == 'yes':
                    todo_list.clear_tasks()
                    print("All tasks cleared.")
            else:
                print("The to-do list is already empty.")
        
        elif choice == '7':
            if os.path.exists(filename):
                todo_list.load_from_file(filename)
                print("Tasks loaded.")
            else:
                print("No saved tasks found.")

        elif choice == '8':
            todo_list.save_to_file(filename)
            print("Tasks saved. Exiting the application.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
