import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_absolute_path, directory))

        valid_target_dir = os.path.commonpath([working_dir_absolute_path, target_dir]) == working_dir_absolute_path

        if not valid_target_dir:
            return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'    Error: {directory} is not a directory'

        recorded_dir_items = []
        for item in os.listdir(target_dir):
            path_to_file = os.path.join(target_dir, item)
            recorded_dir_items.append(f'  - {item}: file_size={os.path.getsize(path_to_file)} bytes, is_dir={os.path.isdir(path_to_file)}')

        return "\n".join(recorded_dir_items)
    except Exception as e:
        return f"Error: Some generic error occured in get_files_info.  {repr(e)}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
