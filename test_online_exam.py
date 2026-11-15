"""Unit tests for the online examination demo."""

import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import online_exam


class GradeStudentTests(unittest.TestCase):
    """Tests for individual exam scoring."""

    def test_correct_answers_receive_full_score(self) -> None:
        responses = {
            0: "4",
            1: "def",
            2: "Central Processing Unit",
            3: "tuple",
        }
        self.assertEqual(online_exam.grade_student("Asha", responses), 4)

    def test_incorrect_answer_loses_only_its_mark(self) -> None:
        responses = {
            0: "4",
            1: "def",
            2: "Wrong answer",
            3: "tuple",
        }
        self.assertEqual(online_exam.grade_student("Asha", responses), 3)

    def test_missing_answer_is_marked_incorrect(self) -> None:
        responses = {0: "4", 1: "def", 3: "tuple"}
        self.assertEqual(online_exam.grade_student("Asha", responses), 3)

    def test_empty_responses_receive_zero(self) -> None:
        self.assertEqual(online_exam.grade_student("Asha", {}), 0)

    def test_multiple_students_are_graded_independently(self) -> None:
        first_score = online_exam.grade_student("Asha", {0: "4"})
        second_score = online_exam.grade_student("Ben", {1: "def", 2: "CPU"})

        self.assertEqual(first_score, 1)
        self.assertEqual(second_score, 1)


class GradeAndClassResultsTests(unittest.TestCase):
    """Tests for grade bands and class-level calculations."""

    def test_grade_boundaries_at_90_60_and_below_60_percent(self) -> None:
        # Ten questions make the requested percentage boundaries exact.
        with patch.object(online_exam, "QUESTIONS", [
            {"q": "Question", "answer": "answer"} for _ in range(10)
        ]):
            self.assertEqual(online_exam.get_grade(9), "A")
            self.assertEqual(online_exam.get_grade(6), "B")
            self.assertEqual(online_exam.get_grade(5), "C")

    def test_class_average_is_calculated_correctly(self) -> None:
        results = {"Asha": 4, "Ben": 2, "Chen": 3}
        self.assertEqual(online_exam.class_average(results), 3.0)

    def test_tied_top_scores_choose_first_student_consistently(self) -> None:
        results = {"Asha": 4, "Ben": 4, "Chen": 2}
        self.assertEqual(online_exam.topper(results), "Asha")

    def test_topper_with_no_students_returns_none(self) -> None:
        self.assertIsNone(online_exam.topper({}))


class ImportBehaviorTests(unittest.TestCase):
    """Tests that importing the module has no demo side effects."""

    def test_import_does_not_run_demonstration(self) -> None:
        result = subprocess.run(
            [sys.executable, "-c", "import online_exam"],
            capture_output=True,
            text=True,
            check=True,
            cwd=Path(online_exam.__file__).parent,
        )
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
