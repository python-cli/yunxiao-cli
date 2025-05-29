import os
import os.path
from typing import Optional

def get_current_working_git_repo() -> Optional[str]:
    """Get the current working git repository path.
    
    Checks the current directory and its parent directories until a .git folder is found.
    
    Returns:
        Optional[str]: The path to the git repository if found, otherwise None.
    """
    path = os.getcwd()
    
    # Check if the current directory is a git repository
    if os.path.isdir(os.path.join(path, '.git')):
        return path
    
    # If not, check parent directories
    parent = path
    while parent != os.path.dirname(parent):  # Stop at root directory
        parent = os.path.dirname(parent)
        if os.path.isdir(os.path.join(parent, '.git')):
            return parent
    
    return None