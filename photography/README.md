# `photography`: When you don't have drawing or painting skills
This module offers classes that contain functions for digital photography

## Table of Contents
1. [Classes and Methods](#classes-and-methods)  
    1.1. [Transfer](#transfer)
2. [Driver Code Sample](#driver-code-sample)  
3. [Unit Tests](#unit-tests)

## Classes and Methods
This module contains the following classes and methods:

### Transfer
- `__init__(input_dir)`
    - Requires an input path to a directory where photo and/or video files are stored
- `import_config()`
    - Imports configuration settings
- `get_file_list(input_dir, input_ext)`
    - Returns a list of files in `input_dir` that have an file extension matching `input_ext`
- `build_file_list()`
    - Builds file lists for photo and video files
- `confirm_transfer()`
    - Confirms with the user whether to proceed with the transfer or not
- `get_file_mod_dates(input_list)`
    - Requires a list of files
    - Returns a list of 'last modified' dates for a list of files
- `run_transfer()`
    - Sets up and performs file transfer
- `run_robocopy(input_date, input_path)`
    - Requires a date and a path
    - Runs robocopy for files on a specified date and sends them to a specifed location

## Driver Code Sample
Sample driver code can be found at the end of the file in the `STANDALONE SCRIPT` section.

## Unit Tests
Unit tests in progress!