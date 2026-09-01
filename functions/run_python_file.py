import os
import sys
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))

        valid_target_file = os.path.commonpath([working_dir_absolute_path, target_file]) == working_dir_absolute_path

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        process_result = subprocess.run(command, capture_output=True, cwd=working_dir_absolute_path, text=True, timeout=30)

        output_text = ""
        if process_result.returncode != 0:
            output_text += f"Process exited with code {process_result.returncode}\n"
        elif not process_result.stdout and not process_result.stderr:
            output_text += f"No output processed\n"

        if process_result.stdout:
            output_text += f"STDOUT: {process_result.stdout}\n"
        elif process_result.stderr:
            output_text += f"STDERR: {process_result.stderr}\n"

        return output_text

    except Exception as e:
        return f"Error: executing Python file: {repr(e)}"
