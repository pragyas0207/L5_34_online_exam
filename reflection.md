# Lab 5 Reflection

> **Provisional answers:** The original lab handout and its four reflection questions were not present in this repository. The README refers to a separate handout, so the answers below address the four reflection topics specified for this project and may need to be matched to the handout wording later.

## 1. What did I learn from using Pylint, Flake8, and Bandit?

Each tool looks for a different kind of problem. Pylint reported code quality issues such as missing docstrings, non-snake-case names, and a mutable default argument. Flake8 reported formatting problems. Bandit found security concerns, including the hard-coded password, MD5 use, and the shell command built in `lockScreen`.

After the changes, the Pylint score went from 5.65/10 to 10.00/10, and Flake8 went from four findings to none. Bandit went from four findings, including two High severity findings, to two Low severity subprocess warnings. The remaining warnings relate to using `subprocess`; the SSH helper now validates the hostname and runs an argument list without a shell. I also changed bonus selection to `secrets.choice`.

## 2. How is static code analysis different from testing?

Static analysis examines source code without running the application. It can point out patterns such as unsafe shell use, weak hashing, naming problems, and formatting issues. Testing runs code with selected inputs and checks the results. For example, the `unittest` suite checked answer scoring, grade boundaries, averages, ties, empty topper results, and that importing the module does not run the demo. Both methods are useful: analysis finds suspicious code patterns, while tests check observed behavior for the cases they cover.

## 3. Why do command injection and weak hashing matter?

The original `lockScreen` built a shell command by joining the SSH host with the command text. If the host value contained shell syntax, it could cause commands beyond the intended screen lock to run. The updated function validates the host and passes arguments to `subprocess.run` without invoking a shell, which removes that shell interpretation path.

MD5 is not suitable when a hash must provide security because it is no longer considered collision resistant. In this program, answers are known text and do not need password storage, so the updated grader compares normalized answers directly instead of hashing them. The hard-coded demo password was also removed.

## 4. How do code quality improvements help maintainability and reliability?

Clear names, docstrings, and type hints make each function's purpose and inputs easier to understand. Removing global result state and the mutable default argument makes grading calls independent. `topper()` now handles an empty result set safely, and the `if __name__ == "__main__":` guard allows the module to be imported without running the demonstration. These changes make the program easier to reuse and reason about. The ten unit tests passed after the changes, and the demo retained the baseline student scores, average, and topper.
