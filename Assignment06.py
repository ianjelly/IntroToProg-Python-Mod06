# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   Ian Basques-Jellison, 8/17/2025, Created Script
#   <Your Name Here>, <Date>, <Activity>
# ------------------------------------------------------------------------------------------ #
import json


# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
# FILE_NAME: str = "Enrollments.csv"
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables and constants
# student_first_name: str = ''  # Holds the first name of a student entered by the user.
# student_last_name: str = ''   # Holds the last name of a student entered by the user.
# course_name: str = ''         # Holds the name of a course entered by the user.
# student_data: dict = {}       # one row of student data
students: list = []             # a table of student data
# file = None                   # Holds a reference to an opened file.
menu_choice: str = ''           # Hold the choice made by the user.


# Processing ------------------------------------------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions for Json files

    ChangeLog: (Who, When, What)
    Ian Basques-Jellison, 8/17/2025, Created Class
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file

        ChangeLog: (Who, When, What)
        Ian Basques-Jellison, 8/17/2025, Created Function

        :return: a table of student data
        """
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("Please check that the file exists " \
                                     "and that it is in a json format.", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error " \
                                     "reading the file.", e)
        finally:
            if file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file

        ChangeLog: (Who, When, What)
        Ian Basques-Jellison, 8/17/2025, Created Function

        :return: None
        """
        try:
            file = open(file_name, "w")
            json.dump(student_data, file, indent=2)

            file.close()
            print("The following data was saved to file!")
            for student in student_data:
                print(f'Student {student["FirstName"]} '
                      f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        except Exception as e:
            if file.closed == False:
                file.close()
            IO.output_error_messages("Error: There was a problem with writing " /
                                     "to the file.\n" /
                                     "Please check that the file is not open " /
                                     "by another program.", e)


# Presentation ----------------------------------------------------------------------- #
class IO:
    """
    A collection of presentation layer functions for user input and output

    ChangeLog: (Who, When, What)
    Ian Basques-Jellison, 8/17/2025, Created Class
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays error messages to the user

        ChangeLog: (Who, When, What)
        Ian Basques-Jellison, 8/17/2025, Created Function

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu to the user

        ChangeLog: (Who, When, What)
        Ian Basques-Jellison, 8/17/2025, Created Function

        :return: None
        """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        Ian Basques-Jellison, 8/17/2025, Created Function

        :return: string with the user's choice
        """
        choice = "0"
        try:
            choice = input("What would you like to do: ")
            if choice not in ("1","2","3","4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing the exception object
                                                   # to avoid the technical message
        return choice

    @staticmethod
    def input_student_data(student_data: list):
        """ This function gets first name, last name, and course from the user

        ChangeLog: (Who, When, What)
        Ian Basques-Jellison, 8/17/2025, Created Function

        :return: str
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")
            student = {"FirstName": student_first_name,
                       "LastName": student_last_name,
                       "CourseName": course_name}
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} " \
                  f"for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(f"{e}", e)
        except Exception as e:
            IO.output_error_messages("Error: There was a problem with " \
                                     "your entered data.", e)
        return student_data

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays all the registered students and their courses

        ChangeLog: (Who, When, What)
        Ian Basques-Jellison, 8/17/2025, Created Function

        :return: None
        """
        # Process the data to create and display a custom message
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} '
                  f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)

# End of function definitions


# ------------------------------------ MAIN BODY ------------------------------------- #
# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    # else:
        # print("Please only choose option 1, 2, or 3")

print("Program Ended")
