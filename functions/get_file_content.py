import os

from config import FILE_READ_CHARACTER_LIMIT


def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        working_dir_absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_absolute_path, file_path))

        valid_target_file = os.path.commonpath([working_dir_absolute_path, target_file]) == working_dir_absolute_path

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_contents = ""
        with open(target_file, mode='r') as file:
            file_contents = file.read(FILE_READ_CHARACTER_LIMIT)

            if file.read(1):
                file_contents += f'[...File "{file_path}" truncated at {FILE_READ_CHARACTER_LIMIT} characters]'

        return file_contents

    except Exception as e:
        return f"Error: Some generic error occured in get_file_content.  {repr(e)}"
