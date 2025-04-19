import subprocess
import sys
from typing import List, Tuple

def run_command(command: List[str]) -> Tuple[int, str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return 0, result.stdout
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stderr

def check_code_quality() -> int:
    checks = [
        (["black", "--check", "."], "Code formatting"),
        (["isort", "--check-only", "."], "Import sorting"),
        (["mypy", "."], "Type checking"),
        (["pylint", "core/", "interfaces/", "utils/", "tests/"], "Code linting"),
        (["flake8", "."], "Style checking"),
    ]

    total_errors = 0
    for command, description in checks:
        print(f"\nRunning {description}...")
        exit_code, output = run_command(command)
        if exit_code != 0:
            print(f"❌ {description} failed:")
            print(output)
            total_errors += 1
        else:
            print(f"✅ {description} passed")

    return total_errors

if __name__ == "__main__":
    errors = check_code_quality()
    if errors > 0:
        print(f"\nFound {errors} code quality issues")
        sys.exit(1)
    print("\nAll code quality checks passed!")
    sys.exit(0) 