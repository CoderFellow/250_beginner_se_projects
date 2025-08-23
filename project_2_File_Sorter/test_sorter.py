"""
Project 2 - B: Testing Core FileSorter.py functionalities
Project Description: This script tests all the core
functionalities of FileSorter.py.
"""

import shutil
import os
import unittest
from FileSorter import FileSorterApp  # Assumed file name is FileSorter.py

class MyTest(unittest.TestCase):
    """
    This class verifies all core functionalities of the FileSorter.py app.
    """

    TEST_DIRECTORY = "temp_test_directory"

    def setUp(self):
        """
        This function:
        1. checks if the TEST_DIRECTORY exists. If proven
        true then it removes the directory. Following up, it then
        creates another new directory with the constant TEST_DIRECTORY.
        Then sets a dictionary to serve as files to create. The key
        being the name of the file, and the content being what is
        written inside. This dictionary is then iterated upon
        using python's read and write in-built functionalities to
        create the file_name (key) and write content (value).
        Towards the end an object reserved and used for this testing
        file is created.

        args:
            none

        returns:
            none
        """
        if os.path.exists(self.TEST_DIRECTORY):
            shutil.rmtree(self.TEST_DIRECTORY)
        os.makedirs(self.TEST_DIRECTORY)

        files_to_create = {
            "file.txt": "This is a text file.",
            "Photo.jpg": "This is a jpeg file.",
            "no_extension_file": "this file has no extension."
        }
        
        for file_name, content in files_to_create.items():
            file_path = os.path.join(self.TEST_DIRECTORY, file_name)
            with open(file_path, 'w') as f:
                f.write(content)
                
        self.app = FileSorterApp(self.TEST_DIRECTORY)

    def tearDown(self):
        """
        This function simply checks if the TEST_DIRECTORY exists, then
        deletes it if it does.
        """
        if os.path.exists(self.TEST_DIRECTORY):
            shutil.rmtree(self.TEST_DIRECTORY)
    
    def test_note_all_extensions(self):
        """
        This function runs the notes_all_extensions function
        in the FileSorter.py file here as a test, establishes an expected
        set of file extensions, then uses a method from unittest class
        to check if the expected extensions in this very function
        is equal to the extensions in the previous FileSorter.py
        initilized list 'extensions.'

        args:
            none

        returns:
            none
        """
        # The single-pass approach now handles this within the main function call
        self.app.iterate_through_all_files()
        
        expected_extensions = {'.txt', '.jpg', ''}
        self.assertEqual(self.app.extensions, expected_extensions)
    
    def test_create_subdirectories(self):
        """
        This app calls two functions (note_all_extensions and
        create_subdirectories_for_specific_functions) to set up the
        necessary conditions for the following test. A set of
        expected extensions is created. This test is then iterated
        upon in a for loop, where the directories are tested
        upon if they exist.

        args:
            none

        returns:
            none
        """
        # The single-pass approach now handles this within the main function call
        self.app.iterate_through_all_files()

        expected_directories = {
            os.path.join(self.TEST_DIRECTORY, '.txt'),
            os.path.join(self.TEST_DIRECTORY, '.jpg'),
            os.path.join(self.TEST_DIRECTORY, '')
        }

        for directory in expected_directories:
            self.assertTrue(os.path.isdir(directory), f"Directory {directory} does not exist.")

    def test_move_files_to_subdirectory(self):
        """
        This function serves to test the function from the app that
        creates a specfici directory for each specific file extension.
        """
        # Calling the full function to perform the move operation
        self.app.iterate_through_all_files()
        
        expected_locations = {
            'file.txt': os.path.join(self.TEST_DIRECTORY, '.txt', 'file.txt'),
            'Photo.jpg': os.path.join(self.TEST_DIRECTORY, '.jpg', 'Photo.jpg'),
            'no_extension_file': os.path.join(self.TEST_DIRECTORY, '', 'no_extension_file')
        }

        for file_name, destination in expected_locations.items():
            self.assertTrue(os.path.exists(destination))
            self.assertTrue(os.path.isfile(destination))

    def test_no_extension_file_moves_correctly(self):
        """
        Explicitly tests that a file with no extension is moved to the correct
        directory (the directory with an empty string as its name).
        This is the new test requested by the instructor.
        """
        # Calling the full function to perform the move operation
        self.app.iterate_through_all_files()
        
        # Define the expected paths for the no-extension file
        no_extension_file_source = os.path.join(self.TEST_DIRECTORY, 'no_extension_file')
        no_extension_file_destination = os.path.join(self.TEST_DIRECTORY, '', 'no_extension_file')
        
        # Assert that the original file no longer exists
        self.assertFalse(os.path.exists(no_extension_file_source), "Original no-extension file still exists.")
        
        # Assert that the file now exists in the correct destination directory
        self.assertTrue(os.path.exists(no_extension_file_destination), "No-extension file was not moved to the correct directory.")


if __name__ == "__main__":
    """ main function"""
    unittest.main()
