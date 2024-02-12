import os

def get_paths_to_config(directory, file1, file2):
    current_directory = os.getcwd()

    config_dir = os.path.join(current_directory, directory)
    if file1:
        credentials_path = os.path.join(config_dir, file1)
    elif file2:
        token_path = os.path.join(config_dir, file2)

    return credentials_path, token_path