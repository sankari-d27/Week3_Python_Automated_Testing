
"""Student Records Management System."""

import json
from pathlib import Path


class StudentNotFoundError(Exception):
    """Student record does not exist."""


class DuplicateStudentError(Exception):
    """Student ID already exists."""


class StudentManager:

    def __init__(self, storage_file=None):
        self.storage_file = Path(storage_file) if storage_file else None
        self.students = {}

    @staticmethod
    def _validate_student(student_id, name, marks):
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Invalid student ID.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid student name.")

        if isinstance(marks, bool) or not isinstance(marks, (int, float)):
            raise ValueError("Marks must be numeric.")

        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")

    @staticmethod
    def calculate_grade(marks):
        if isinstance(marks, bool) or not isinstance(marks, (int, float)):
            raise ValueError("Marks must be numeric.")

        if not 0 <= marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")

        if marks >= 90:
            return "A"
        if marks >= 75:
            return "B"
        if marks >= 60:
            return "C"
        if marks >= 40:
            return "D"
        return "F"

    def add_student(self, student_id, name, marks):
        self._validate_student(student_id, name, marks)

        student_id = student_id.strip()

        if student_id in self.students:
            raise DuplicateStudentError(
                f"Student {student_id} already exists."
            )

        student = {
            "id": student_id,
            "name": name.strip(),
            "marks": marks,
            "grade": self.calculate_grade(marks),
        }

        self.students[student_id] = student
        return student.copy()

    def get_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError(
                f"Student {student_id} was not found."
            )

        return self.students[student_id].copy()

    def update_student(self, student_id, name=None, marks=None):
        student = self.get_student(student_id)

        new_name = student["name"] if name is None else name
        new_marks = student["marks"] if marks is None else marks

        self._validate_student(student_id, new_name, new_marks)

        updated_student = {
            "id": student_id,
            "name": new_name.strip(),
            "marks": new_marks,
            "grade": self.calculate_grade(new_marks),
        }

        self.students[student_id] = updated_student
        return updated_student.copy()

    def delete_student(self, student_id):
        self.get_student(student_id)
        del self.students[student_id]
        return True

    def search_student(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Search name cannot be empty.")

        query = name.strip().casefold()

        return [
            student.copy()
            for student in self.students.values()
            if query in student["name"].casefold()
        ]

    def calculate_average(self):
        if not self.students:
            return 0.0

        total = sum(
            student["marks"] for student in self.students.values()
        )

        return total / len(self.students)

    def save_to_file(self):
        if self.storage_file is None:
            raise ValueError("No storage file configured.")

        self.storage_file.parent.mkdir(
            parents=True, exist_ok=True
        )

        with self.storage_file.open("w", encoding="utf-8") as file:
            json.dump(list(self.students.values()), file, indent=4)

    def load_from_file(self):
        if self.storage_file is None:
            raise ValueError("No storage file configured.")

        if not self.storage_file.exists():
            self.students = {}
            return

        with self.storage_file.open("r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError("Invalid student data format.")

        loaded = {}

        for record in records:
            if not isinstance(record, dict):
                raise ValueError("Invalid student record.")

            if set(record) != {"id", "name", "marks", "grade"}:
                raise ValueError("Invalid student record fields.")

            student_id = record["id"]
            name = record["name"]
            marks = record["marks"]

            self._validate_student(student_id, name, marks)

            if student_id != student_id.strip():
                raise ValueError("Invalid student ID.")

            if name != name.strip():
                raise ValueError("Invalid student name.")

            if student_id in loaded:
                raise ValueError("Duplicate student ID.")

            grade = self.calculate_grade(marks)

            if record["grade"] != grade:
                raise ValueError("Incorrect stored grade.")

            loaded[student_id] = {
                "id": student_id,
                "name": name,
                "marks": marks,
                "grade": grade,
            }

        self.students = loaded
