import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file_path):
        return f'Error: File "{file_path}" not found.'

    if not target_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            ["python", target_file_path, *args], timeout=30
        )

        return_code = completed_process.returncode

        if return_code != 0:
            print(f"Process exited with code {return_code}")

        out = None
        if completed_process.stdout is None:
            out = "No output produced."
        else:
            out = completed_process.stdout

        return (
            f"STDOUT: {out}",
            f"STDERR: {completed_process.stderr}",
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"
