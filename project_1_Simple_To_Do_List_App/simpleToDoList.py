"""A simple command-line to-do Python application."""
from abc import ABC, abstractmethod
import json
import os
import sys


class OpenApp(ABC):
    """This class ensures the user's tasks are taken in."""

    @abstractmethod
    def menu(self):
        """Displays the main menu."""
        pass

    def menu_functions(self, user_input):
        """Manages the application's functions."""
        pass

    def load_tasks(self):
        """Loads tasks from a file."""
        pass


class App(OpenApp):
    """Main application class for the To-Do app."""

    def __init__(self):
        """Initializes the task manager and loads tasks."""
        self.tasks = self.load_tasks()
        self.task_manager = TaskManager(self.tasks)

    def menu(self):
        """Displays the main menu and prompts for user input."""
        print("**************************")
        print("* To-Do_Python_App       *")
        print("*                        *")
        print("* 1. Add Task            *")
        print("* 2. Delete Task         *")
        print("* 3. View Tasks          *")
        print("* 4. Mark Task Complete  *")
        print("* 5. Save Task           *")
        print("* 6. Exit                *")
        print("**************************")

        user_input = int(input("Enter Option: "))
        self.menu_functions(user_input)

    def load_tasks(self):
        """
        Reads tasks from the To_Do_List.json file and returns them as a list.
        """
        filename = 'To_Do_List.json'

        if not os.path.exists(filename):
            print("Warning: To_Do_List.json not found. Starting with an empty list.")
            return []

        with open('To_Do_List.json', 'r') as json_file:
            try:
                tasks_as_dicts = json.load(json_file)
                tasks_as_objects = [Task(d['description']) for d in tasks_as_dicts]
                return tasks_as_objects
            except json.JSONDecodeError:
                print("Warning: File is empty or corrupt. Starting with an empty list.")
                return []

    def menu_functions(self, user_input):
        """This function manages all the application's functions."""
        start_function = self.task_manager

        # Add task
        if user_input == 1:
            user_task_entry = input("Enter task: ")
            specific_task = Task(user_task_entry)
            start_function.add_task(specific_task)

        # Delete task
        elif user_input == 2:
            start_function.list_tasks()
            task_to_delete = int(input("Enter Task Number: "))
            start_function.delete_task(task_to_delete)

        # View task
        elif user_input == 3:
            start_function.list_tasks()

        # Mark task as complete
        elif user_input == 4:
            user_input_task_number = int(input("Enter Task Number: "))
            start_function.mark_as_complete(user_input_task_number)

        # Save task
        elif user_input == 5:
            start_function.data_persistence()

        # Exit
        elif user_input == 6:
            print("Ending App. Saving Tasks...")
            start_function.data_persistence()
            sys.exit()

        self.menu()


class TaskManagerInterface(ABC):
    """
    This class ensures the "TaskManager" class implements all important functions.
    """

    @abstractmethod
    def add_task(self, task_obj):
        """This function adds a task to the list."""
        pass

    @abstractmethod
    def list_tasks(self):
        """This function lists tasks from the list."""
        pass

    @abstractmethod
    def mark_as_complete(self, task_number):
        """This function marks tasks as complete."""
        pass

    @abstractmethod
    def delete_task(self, task_number):
        """This function deletes specific tasks from the list."""
        pass

    @abstractmethod
    def data_persistence(self):
        """This function puts the task list into a .json file."""
        pass


class TaskManager(TaskManagerInterface):
    """Main functionalities of the To-Do Application."""

    def __init__(self, tasks):
        """Initializes task list."""
        self.task_list = tasks

    def add_task(self, task_obj):
        """Adds a task to the task list."""
        self.task_list.append(task_obj)

    def list_tasks(self):
        """Lists all tasks in the list."""
        print()
        for i, task in enumerate(self.task_list):
            specific_task = task.to_dict()
            print(f"Task {i}: {specific_task['description']} | Status: {specific_task['status']}")
        print()

    def mark_as_complete(self, task_number):
        """Marks a specific task as complete."""
        try:
            self.task_list[task_number].mark_complete()
        except IndexError:
            print("Warning: Invalid Task Number!")

    def delete_task(self, task_number):
        """Deletes a specific task from the list."""
        try:
            del self.task_list[task_number]
        except IndexError:
            print("Warning: Invalid Task Number!")

    def data_persistence(self):
        """Stores the tasks collected in a .json file."""
        with open('To_Do_List.json', 'w') as json_file:
            list_of_dicts = [task.to_dict() for task in self.task_list]
            json.dump(list_of_dicts, json_file, indent=5)


class Task:
    """Task class: Handles the class variables."""

    def __init__(self, description):
        """Initializes description and status."""
        self._description = description
        self._status = 'Incomplete'

    def to_dict(self):
        """Returns description and status as a dictionary."""
        return {"description": self._description, "status": self._status}

    def mark_complete(self):
        """
        Changes the status to 'Complete' if it's currently 'Incomplete'.
        """
        if self._status == "Incomplete":
            self._status = 'Complete'
        else:
            print("Message: Task is already Completed!")


if __name__ == "__main__":
    """This section is a demonstration of the to-do list's functionality."""
    start = App()
    start.menu()
