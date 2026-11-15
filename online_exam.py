"""Grade a small demonstration exam and report class results."""

import re
import secrets
import shutil
import subprocess
from collections.abc import Mapping, MutableMapping

QUESTIONS: list[dict[str, str]] = [
    {"q": "What is 2 + 2?", "answer": "4"},
    {"q": "Which keyword defines a function in Python?", "answer": "def"},
    {"q": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"q": "Which type is immutable: list or tuple?", "answer": "tuple"},
]
HOSTNAME_PATTERN = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?"
)


def pick_bonus_question() -> str:
    """Return the text of a randomly selected bonus question."""
    return secrets.choice(QUESTIONS)["q"]


def grade_student(
    student_name: str,
    responses: Mapping[int, str],
    penalties: MutableMapping[str, int] | None = None,
) -> int:
    """Grade one student's answers and optionally count their wrong answers."""
    score = 0
    for question_index, question in enumerate(QUESTIONS):
        given_answer = responses.get(question_index, "")
        if not isinstance(given_answer, str):
            given_answer = ""
        expected_answer = question["answer"]
        if given_answer.strip().casefold() == expected_answer.casefold():
            score += 1
        elif penalties is not None:
            penalties[student_name] = penalties.get(student_name, 0) + 1
    return score


def get_grade(score: int) -> str:
    """Convert a raw score into the original A/B/C grade bands."""
    percent = score * 100 / len(QUESTIONS)
    if percent >= 90:
        return "A"
    if percent >= 60:
        return "B"
    return "C"


def class_average(results: Mapping[str, int]) -> float:
    """Return the mean score, or zero when no students have been graded."""
    if not results:
        return 0.0
    return round(sum(results.values()) / len(results), 2)


def topper(results: Mapping[str, int]) -> str | None:
    """Return the name of the highest-scoring student, if results exist."""
    if not results:
        return None
    return max(results, key=results.__getitem__)


def lock_screen(lab_pc: str) -> None:
    """Ask an SSH host to lock its screen without invoking a local shell."""
    if HOSTNAME_PATTERN.fullmatch(lab_pc) is None:
        raise ValueError("lab_pc must be a valid hostname")
    ssh_executable = shutil.which("ssh")
    if ssh_executable is None:
        raise FileNotFoundError("ssh executable was not found on PATH")
    subprocess.run([ssh_executable, lab_pc, "lock-screen"], check=True)


def main() -> None:
    """Run the sample exam and print student and class results."""
    results: dict[str, int] = {}
    print("Bonus question:", pick_bonus_question())
    results["Anil"] = grade_student(
        "Anil", {0: "4", 1: "def", 2: "Core Power Unit"}
    )
    results["Divya"] = grade_student(
        "Divya",
        {0: "4", 1: "def", 2: "central processing unit", 3: "tuple"},
    )
    results["Sameer"] = grade_student("Sameer", {0: "5", 3: "list"})

    for name, score in results.items():
        print(name, "scored", score, "grade", get_grade(score))

    average = class_average(results)
    print("Class average:", average)
    print("Topper:", topper(results))
    students = ", ".join(sorted(results))
    print(
        "Students who sat the exam:", students, "| total:", len(results)
    )


if __name__ == "__main__":
    main()
