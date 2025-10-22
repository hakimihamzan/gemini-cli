import os


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(full_path)

    if not full_path.startswith(working_directory) or working_directory not in abs_path:
        raise Exception(
            f'Cannot list "{directory}" as it is outside the permitted working directory'
        )

    files = os.listdir(abs_path)
    print("Result for current directory:")

    for f in files:
        f_path = os.path.join(abs_path, f)

        file_size = os.path.getsize(f_path)

        if os.path.isfile(f_path):
            print(f" - {f}: file_size={file_size} bytes, is_dir=False")
        elif os.path.isdir(f_path):
            print(f" - {f}: file_size={file_size} bytes, is_dir=True")

    print("\n")
