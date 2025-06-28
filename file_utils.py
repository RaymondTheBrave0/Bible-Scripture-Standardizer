import os
import shutil

def get_docx_files(directory: str):
    """
    Returns a list of all .docx files in the given directory.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"The provided path is not a directory: {directory}")
    
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.docx')]

def create_backup(file_path: str) -> (bool, str):
    """
    Creates a backup of the given file.
    Returns a tuple (success: bool, backup_path: str).
    """
    try:
        backup_path = f"{file_path}.bak"
        shutil.copy(file_path, backup_path)
        return True, backup_path
    except Exception as e:
        return False, str(e)