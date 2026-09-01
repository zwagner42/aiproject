import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))

        valid_target_file = os.path.commonpath([working_dir_absolute_path, target_file]) == working_dir_absolute_path

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        _ = os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, mode='w') as file:
            _ = file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: Some generic error occured in write_file.  {repr(e)}"
