# Dotnet-Leetcode-Template

### About:
This repository contains automation script that helps me to create required DotNet projects in specified directory preference.

### Description:
This script is used as a template to create DotNet projects (tailored to my own preference) which can be used for solving Leet code challenges directly.

This script will create a new directory with the name of the project. Inside this directory, the following projects are created:
1. **Class Library** </br>
    This project will contain all the classes and methods to solve the Leet code challenges.

2. **Unit Test Project** </br>
    This project will contain all the unit tests for the classes and methods in the class library. This project will add a reference to the class library project directly.

3. **Console App** </br>
    This project will contain the main method to run the code. This project will add a reference to the class library project directly. This project can be used to run the code for adhoc testing.

### Prerequisites

This package requires the .NET SDK to be installed.

##### Install .NET
1. Visit the [official .NET download page](https://dotnet.microsoft.com/download).
2. Follow the instructions for your operating system.
3. Verify the installation by running:
   ```bash
   dotnet --version
   ```

### Command:

```
dotnet-project.py [-h] -n  -s  [-f] [--use-program-main]
```

### Usage: 

```
options:
  -h, --help          show this help message and exit
  -n, --name          name of the project
  -s, --solution      name of the solution
  -f, --framework     framework to use for the project
  --use-program-main  use top level statements in the project
```

