#!/usr/bin/env python3

# Importing argument parser module
import argparse
# Importing path module
from pathlib import Path
# Importing subprocess module
import subprocess, os
# imporing shutil module
import shutil

# Custom help formatter class to remove the metavar from the option strings
class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            return super()._format_action_invocation(action)
        
        # Join the option strings without adding a metavar
        return ', '.join(action.option_strings)
    
    # Preversing the description formatting
    def _fill_text(self, text, width, indent):
        return ''.join([indent + line for line in text.splitlines(True)])

# Defining the DotnetBuildProject class to create dotnet projects
class DotnetProjectBuilderLibrary:
    # Constructor to initialize the project name and framework
    def __init__(self, project_name, solution_name, framework="net6.0", use_top_level_statements=False):
        # Initializing the project name
        self.project_name = project_name
        # Initializing the solution name
        self.solution_name = solution_name
        # Initializing the framework. Default is net6.0
        self.framework = framework
        # Initializing the use top level statements
        self.use_top_level_statements = use_top_level_statements
        # Initializing the project path
        self.__project_path = Path.joinpath(Path.cwd(), self.project_name)
        # Initializing the class library string
        self.__class_library_string = "classlib"
        # Initializing the unit test string
        self.__unit_test_string = "xunit"
        # Initializing the console app string
        self.__console_app_string = "console"
        # Initializing the solution string
        self.__solution_string = "sln"
        # Initializing the class library project name
        self.__class_library_name = f"{self.project_name[2:]}Lib"
        # Initializing the unit test project name
        self.__unit_test_name = f"{self.project_name[2:]}UnitTests"
        # Initializing the console app project name
        self.__console_app_name = f"{self.project_name[2:]}ConsoleApp"
    
    # Building the project directory
    def __build_project_directory(self):
        # Creating the directory path
        directory_path = Path(self.__project_path)
        # Checking if the directory exists
        if directory_path.exists():
            # Removing the directory even if exists or it's not empty
            shutil.rmtree(directory_path, ignore_errors=True)
        # Creating the directory
        directory_path.mkdir()
        
    # Defining method to check the output
    def __check_output(self, command_output, message_required):
        # Checking the output and returning the message required
        return message_required if (command_output[:len(message_required)] == message_required) else command_output
    
    # Defining method to rename the required files
    def __rename_files(self, required_file_name, new_file_name):
        # Checking if the required file exists and is a file
        if Path(required_file_name).is_file():
            # Renaming the file
            Path(required_file_name).rename(Path(required_file_name).with_name(new_file_name))
            # Printing the message
            print(f"Renamed the file {required_file_name} to {new_file_name}")
    
    # Defining method to update the contents of the file
    def __update_file_contents(self, required_file, old_text, new_text):
        # Reading the contents of the file
        with open(required_file, 'r') as file:
            # Reading the contents of the file
            file_contents = file.read()
        # Replacing the contents of the file
        file_contents = file_contents.replace(old_text, new_text)
        # Writing the contents to the file
        with open(required_file, 'w') as file:
            # Writing the contents to the file
            file.write(file_contents)
            # Printing the message
            print(f"Updated the contents of the file from {old_text} to {new_text}")
        
    
    # Method to create the class library project
    def create_class_library_project(self):
        # Creating the class library project
        output = subprocess.run(["dotnet", "new", self.__class_library_string, "-n", self.__class_library_name, "-f", self.framework], cwd=self.__project_path, capture_output=True, text=True)
        # Creating a message
        message_required = 'The template "Class Library" was created successfully.'
        # Displaying the output
        print(self.__check_output(output.stdout, message_required))
        # Fetching the name of the required file
        required_file = Path.joinpath(self.__project_path, self.__class_library_name, "Class1.cs").as_posix()
        # Updating the contents of the file
        self.__update_file_contents(required_file, "Class1", self.__class_library_name)
        # Renaming the required file
        self.__rename_files(required_file, f"{self.__class_library_name}.cs")
        
    # Method to create the unit test project
    def create_unit_test_project(self):
        # Creating the unit test project
        output = subprocess.run(["dotnet", "new", self.__unit_test_string, "-n", self.__unit_test_name, "-f", self.framework], cwd=self.__project_path, capture_output=True, text=True)
        # Creating a message
        message_required = 'The template "xUnit Test Project" was created successfully.'
        # Displaying the output
        print(self.__check_output(output.stdout, message_required))
        # Fetching the name of the required file
        required_file = Path.joinpath(self.__project_path, self.__unit_test_name, "UnitTest1.cs").as_posix()
        # Updating the contents of the file
        self.__update_file_contents(required_file, "UnitTest1", self.__unit_test_name)
        # Renaming the required file
        self.__rename_files(required_file, f"{self.__unit_test_name}.cs")
        
    # Method to create the console app project
    def create_console_app_project(self):
        # Creating the console app project
        output = subprocess.run(["dotnet", "new", self.__console_app_string, "-n", self.__console_app_name, "-f", self.framework, '--use-program-main', self.use_top_level_statements], cwd=self.__project_path, capture_output=True, text=True)
        # Creating a message
        message_required = 'The template "Console App" was created successfully.'
        # Displaying the output
        print(self.__check_output(output.stdout, message_required))
    
    # Method to add projects to the solution
    def add_projects(self, project_name):
        # Adding the class library project to the solution
        result = subprocess.run(["dotnet", self.__solution_string, self.solution_name, "add", Path.joinpath(self.__project_path, project_name)], cwd=Path.cwd(), capture_output=True, text=True)
        # Displaying the output
        print(result.stdout.strip())
    
    # Method to add reference to projects
    def add_reference(self, project_name, reference_project_name):
        # Adding the reference to the project
        result = subprocess.run(["dotnet", "add", project_name, "reference", reference_project_name], cwd=Path.cwd(), capture_output=True, text=True)
        # Displaying the output
        print(result.stdout.strip())
    
    # Method to create the dotnet projects
    def create_projects(self):
        # Building required directory
        self.__build_project_directory()
        # Creating the class library project
        self.create_class_library_project()
        # Adding the class library project to the solution
        self.add_projects(self.__class_library_name)
        # Creating the unit test project
        self.create_unit_test_project()
        # Adding reference to the unit test project
        self.add_reference(
            project_name=Path.joinpath(self.__project_path, self.__unit_test_name, f"{self.__unit_test_name}.csproj"), 
            reference_project_name=Path.joinpath(self.__project_path, self.__class_library_name, f"{self.__class_library_name}.csproj"))
        # Adding the unit test project to the solution
        self.add_projects(self.__unit_test_name)
        # Creating the console app project
        self.create_console_app_project()
        # Adding reference to the console app project
        self.add_reference(
            project_name=Path.joinpath(self.__project_path, self.__console_app_name, f"{self.__console_app_name}.csproj"),
            reference_project_name=Path.joinpath(self.__project_path, self.__class_library_name, f"{self.__class_library_name}.csproj"))
        # Adding the console app project to the solution
        self.add_projects(self.__console_app_name)

def main():
    # Specifying the dotnet installation path
    # DOTNET_ROOT=$HOME/.dotnet
    # PATH=$PATH:$DOTNET_ROOT:$DOTNET_ROOT/tools
    # Dotnet location string
    dotnet_location = ".dotnet"
    # Specifying the dotnet path
    dotnet_path = Path.joinpath(Path(os.environ['HOME']), dotnet_location)
    # Specifying the dotnet tools path
    dotnet_tools_path = Path.joinpath(dotnet_path, 'tools')
    # Adding the dotnet path to the PATH environment variable
    os.environ['PATH'] = os.environ['PATH'] + ':' + str(dotnet_path) + ':' + str(dotnet_tools_path)
    # Extracting the installed dotnet versions
    dotnet_versions = subprocess.run(["dotnet", "--list-sdks"], capture_output=True, text=True)
    # creating empty list to store the versions available
    versions_available = []
    # Extract the versions available from the output and store in the list
    dotnet_list = dotnet_versions.stdout.split('\n')
    # Iterating through the list and extracting the versions
    for each in dotnet_list:
        # Adding the versions to the list
        versions_available = versions_available + [ f'net{each[:3]}']
        
    
    # Initializing parser
    argument_parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
    # Adding description for this script
    description = r"""
    This script is used as a template to create dotnet projects (tailored to my own preference) which can be used for solving leet code challenges.
    
    This script will create a new directory with the name of the project. Inside this directory, the following projects are created:
        1. Class Library
           This project will contain all the classes and methods to solve the leet code challenges.
        2. Unit Test Project
           This project will contain all the unit tests for the classes and methods in the class library. This project will add a reference to the class library project directly.
        3. Console App
           This project will contain the main method to run the code. This project will add a reference to the class library project directly. This project can be used to run the code for adhoc testing.
    """
    
    # Adding description to the parser
    argument_parser.description = description
    # Adding project name argument to the parser
    argument_parser.add_argument("-n", "--name", help="name of the project", required=True, metavar='')
    # Adding solution name argument to the parser
    argument_parser.add_argument("-s", "--solution", help="name of the solution", required=True, metavar='')
    # Adding framework argument to the parser
    argument_parser.add_argument("-f", "--framework", help="framework to use for the project", default="net6.0", metavar='', choices=versions_available[:-1])
    # Adding use-program-main argument to the parser
    argument_parser.add_argument("--use-program-main", help="use top level statements in the project", default="true", metavar='', choices=["true", "false"])
    # Getting the arguments
    args = argument_parser.parse_args()
    # Getting the arguments as dictionary
    args_dict = vars(args)
    # Getting the project name
    project_name = args_dict["name"]
    # Getting the solution name
    solution_name = args_dict["solution"]
    # Getting the framework
    framework = args_dict["framework"]
    # Getting the top level statements flag
    use_top_level_statements = args_dict["use_program_main"]
    
    # Creating an instance of the DotnetProjectBuilderLibrary class
    dotnet_project_builder = DotnetProjectBuilderLibrary(project_name, solution_name, framework, use_top_level_statements)
    # Creating the dotnet projects
    dotnet_project_builder.create_projects()
    
        
if __name__ == "__main__":
    main()