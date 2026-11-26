
import pytest

from student_management import (
    StudentManager,
    StudentNotFoundError,
    DuplicateStudentError,
)


@pytest.fixture
def manager():
    return StudentManager()


def test_add_student(manager):
    result = manager.add_student("S001", "Alice", 95)
    assert result["name"] == "Alice"
    assert result["grade"] == "A"


def test_add_student_with_boundary_marks(manager):
    result = manager.add_student("S001", "Alice", 90)
    assert result["grade"] == "A"


def test_add_student_rejects_duplicate_id(manager):
    manager.add_student("S001", "Alice", 80)

    with pytest.raises(DuplicateStudentError):
        manager.add_student("S001", "Bob", 70)


@pytest.mark.parametrize("marks", [-1, 101])
def test_add_student_rejects_invalid_marks(manager, marks):
    with pytest.raises(ValueError):
        manager.add_student("S001", "Alice", marks)


@pytest.mark.parametrize("marks", [None, "90", True])
def test_add_student_rejects_non_numeric_marks(manager, marks):
    with pytest.raises(ValueError):
        manager.add_student("S001", "Alice", marks)


@pytest.mark.parametrize(
    "marks, expected",
    [
        (100, "A"),
        (90, "A"),
        (89, "B"),
        (75, "B"),
        (74, "C"),
        (60, "C"),
        (59, "D"),
        (40, "D"),
        (39, "F"),
        (0, "F"),
    ],
)
def test_grade_calculation(marks, expected):
    assert StudentManager.calculate_grade(marks) == expected


def test_rejects_empty_student_id(manager):
    with pytest.raises(ValueError):
        manager.add_student("", "Alice", 80)


def test_rejects_empty_student_name(manager):
    with pytest.raises(ValueError):
        manager.add_student("S001", " ", 80)


def test_get_student(manager):
    manager.add_student("S001", "Alice", 80)
    assert manager.get_student("S001")["name"] == "Alice"


def test_get_missing_student(manager):
    with pytest.raises(StudentNotFoundError):
        manager.get_student("S999")


def test_update_student(manager):
    manager.add_student("S001", "Alice", 60)

    result = manager.update_student(
        "S001", name="Alice Smith", marks=95
    )

    assert result["name"] == "Alice Smith"
    assert result["marks"] == 95
    assert result["grade"] == "A"


def test_update_only_name(manager):
    manager.add_student("S001", "Alice", 80)
    result = manager.update_student("S001", name="Alice Jones")

    assert result["name"] == "Alice Jones"
    assert result["marks"] == 80


def test_update_missing_student(manager):
    with pytest.raises(StudentNotFoundError):
        manager.update_student("S999", name="Bob")


def test_delete_student(manager):
    manager.add_student("S001", "Alice", 80)
    assert manager.delete_student("S001") is True

    with pytest.raises(StudentNotFoundError):
        manager.get_student("S001")


def test_delete_missing_student(manager):
    with pytest.raises(StudentNotFoundError):
        manager.delete_student("S999")


def test_search_student(manager):
    manager.add_student("S001", "Alice Smith", 80)
    manager.add_student("S002", "Bob", 70)

    results = manager.search_student("alice")

    assert len(results) == 1
    assert results[0]["id"] == "S001"


def test_search_is_case_insensitive(manager):
    manager.add_student("S001", "Alice", 80)
    assert len(manager.search_student("ALICE")) == 1


def test_search_rejects_empty_query(manager):
    with pytest.raises(ValueError):
        manager.search_student(" ")


def test_average_calculation(manager):
    manager.add_student("S001", "Alice", 80)
    manager.add_student("S002", "Bob", 60)

    assert manager.calculate_average() == 70


def test_average_for_empty_records(manager):
    assert manager.calculate_average() == 0.0


def test_returned_student_is_copy(manager):
    manager.add_student("S001", "Alice", 80)
    result = manager.get_student("S001")

    result["name"] = "Changed"

    assert manager.get_student("S001")["name"] == "Alice"
