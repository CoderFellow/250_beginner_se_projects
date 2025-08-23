"""
Project 2 - A: FileSorter.py
Project Description: A simple python script that takes in a user's directory 
and organizes everything in a systematic way.
"""

import shutil
import os
import unittest

class FileSorterApp:
    """This class houses all the app's core functionalities"""

    def __init__(self, target_directory):
        """
        Initializes the FileSorterApp with a target directory.
        
        args:
            target_directory (str): The path to the directory to be sorted.
        """
        self.target_directory = target_directory
        self.extensions = set()
        self.files_to_move = {}  # A dictionary to store file paths and their extensions

    def iterate_through_all_files(self):
        """
        This is the main function that coordinates the sorting process.
        It now uses a single-pass traversal to prevent the runaway loop bug.
        
        The process is as follows:
        1. It gets a list of all files in the directory and their extensions.
        2. It creates the necessary subdirectories for each unique extension.
        3. It moves the files into their respective subdirectories.
        """
        self._get_all_files_and_extensions()
        self._create_subdirectories_for_specific_extensions()
        self._move_files_to_their_respective_subdirectories()

    def _get_all_files_and_extensions(self):
        """
        Helper function to perform a single traversal of the directory.
        It populates the `self.extensions` set and `self.files_to_move` dictionary.
        This fixes the `os.walk` bug by listing all files before any file system changes are made.
        """
        for root, subdirs, files in os.walk(self.target_directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                # Skip any files that are already inside a sorted subdirectory
                if root != self.target_directory:
                    continue
                
                # Get the extension and add it to the set
                extension = os.path.splitext(file_name)[1]
                self.extensions.add(extension)
                
                # Store the file path and its extension for later use
                self.files_to_move[file_path] = extension

    def _create_subdirectories_for_specific_extensions(self):
        """
        This function creates a subdirectory for each respective extension.
        It uses the `self.extensions` set populated by the single-pass traversal.
        """
        for extension in self.extensions:
            os.makedirs(os.path.join(self.target_directory, extension), exist_ok=True)

    def _move_files_to_their_respective_subdirectories(self):
        """
        This function moves all files into their respective subdirectories.
        It uses the `self.files_to_move` dictionary populated during the single pass.
        """
        for source_path, extension in self.files_to_move.items():
            file_name = os.path.basename(source_path)
            destination_directory = os.path.join(self.target_directory, extension)
            shutil.move(source_path, destination_directory)
            print(f"Moved {file_name} to '{destination_directory}'.")


if __name__ == "__main__":
    """
    main function:
    """
    target_path = input("Enter directory: ")
    
    app = FileSorterApp(target_path)
    
    app.iterate_through_all_files()
