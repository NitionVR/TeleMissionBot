import os
import shutil

def get_paths_to_config(directory, file1=None, file2=None):
    current_directory = os.getcwd()
    config_dir = os.path.join(current_directory, directory)
    credentials_path = None
    token_path = None
    if file1 is not None:
        credentials_path = os.path.join(config_dir, file1)
    elif file2 is not None:
        token_path = os.path.join(config_dir, file2)

    if credentials_path and token_path:
        return credentials_path, token_path
    return credentials_path

def get_file_path_in_cjc_code_clinics(filename):
    """
    Get or create the path to a file within the cjc_code_clinics_9 directory in the user's home directory.

    :param filename: The name of the file.
    :return: The full path to the file within the cjc_code_clinics_9 directory.
    """

    home_directory = os.path.expanduser("~")

    config_path = os.path.join(home_directory, ".config")

    cjc_code_clinics_9_path = os.path.join(config_path, "cjc_code_clinics_9")

    if not os.path.exists(cjc_code_clinics_9_path):
        os.makedirs(cjc_code_clinics_9_path)

    file_path = os.path.join(cjc_code_clinics_9_path, filename)

    return file_path

def move_config_files_to_home():
    credentials_path = os.path.abspath(".config/credentials.json")
    service_account_path = os.path.abspath(".config/service_account.json")

    home_directory = os.path.expanduser("~")

    cjc_code_clinics_9_path = os.path.join(home_directory, ".config/cjc_code_clinics_9")

    if not os.path.exists(cjc_code_clinics_9_path):
        os.makedirs(cjc_code_clinics_9_path)

    credentials_destination_path = os.path.join(cjc_code_clinics_9_path, "credentials.json")
    service_account_destination_path = os.path.join(cjc_code_clinics_9_path,'service_account.json')
    shutil.copy(credentials_path, credentials_destination_path)
    shutil.copy(service_account_path,service_account_destination_path)
    remove_project_config()
    
    return True

def remove_project_config():
    project_config_path = os.path.abspath(".config")

    if os.path.exists(project_config_path):
        shutil.rmtree(project_config_path)
        return True
    else:
        return False