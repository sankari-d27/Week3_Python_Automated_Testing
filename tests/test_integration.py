
import json
import pytest

from student_management import StudentManager


def test_save_and_load_students(tmp_path):
    file_path = tmp_path / "students.json"

    manager = StudentManager(file_path)
    manager.add_student("S001", "Alice", 95)
    manager.add_student("S002", "Bob", 75)

    manager.save_to_file()

    new_manager = StudentManager(file_path)
    new_manager.load_from_file()

    assert len(new_manager.students) == 2
    assert new_manager.get_student("S001")["grade"] == "A"
    assert new_manager.get_student("S002")["grade"] == "B"


def test_load_missing_file(tmp_path):
    manager = StudentManager(tmp_path / "missing.json")

    manager.load_from_file()

    assert manager.students == {}


def test_save_creates_parent_directory(tmp_path):
    file_path = tmp_path / "data" / "students.json"
    manager = StudentManager(file_path)

    manager.add_student("S001", "Alice", 90)
    manager.save_to_file()

    assert file_path.exists()


def test_save_without_storage_file():
    manager = StudentManager()

    with pytest.raises(ValueError):
        manager.save_to_file()


def test_load_without_storage_file():
    manager = StudentManager()

    with pytest.raises(ValueError):
        manager.load_from_file()


def test_invalid_json_file(tmp_path):
    file_path = tmp_path / "students.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    manager = StudentManager(file_path)

    with pytest.raises(json.JSONDecodeError):
        manager.load_from_file()


def test_invalid_record_does_not_replace_existing_data(tmp_path):
    file_path = tmp_path / "students.json"

    manager = StudentManager(file_path)
    manager.add_student("S001", "Alice", 80)

    file_path.write_text(
        '[{"id": "S002", "name": "Bob", "marks": 120, "grade": "A"}]',
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        manager.load_from_file()

    assert manager.get_student("S001")["name"] == "Alice"


def test_crud_and_average_work_together():
    manager = StudentManager()

    manager.add_student("S001", "Alice", 80)
    manager.add_student("S002", "Bob", 60)

    manager.update_student("S002", marks=100)

    assert manager.calculate_average() == 90

    manager.delete_student("S001")

    assert manager.calculate_average() == 100
