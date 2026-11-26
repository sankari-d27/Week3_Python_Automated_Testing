
# Student Records Management System

## Project Description

This project is developed for Week 3: Writing Automated
Tests for Python Applications.

It is a Python-based application for managing student
records with automated testing using pytest.

## Features

- Add student records.
- Update student information.
- Delete student records.
- Search students by name.
- Calculate grades.
- Calculate class averages.
- Save and load records using JSON.
- Validate inputs and handle exceptions.

## Technologies Used

- Python 3.9 or later
- pytest
- JSON
- pathlib

## Installation

1. Install Python 3.9 or later.
2. Open the project directory.
3. Install the required dependency:

   pip install -r requirements.txt

## Running the Tests

Execute the following command from the project root:

   python -m pytest -v

## Running Tests with Coverage

Install pytest-cov:

   pip install pytest-cov

Run:

   python -m pytest --cov=student_management --cov-report=term-missing

## Using the Application

Example:

   from student_management import StudentManager

   manager = StudentManager()

   manager.add_student("S001", "Alice", 95)

   print(manager.get_student("S001"))

   print(manager.calculate_average())

## Test Structure

- test_student_management.py:
  Unit tests for individual functions.

- test_integration.py:
  Integration tests for combined operations
  and JSON persistence.

## Expected Outcome

All automated tests should pass successfully.

## Author

Week 3 Python Automated Testing Assignment
