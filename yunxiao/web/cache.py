from os.path import join
from typing import Tuple, List, Dict, Optional, Any, Union

from ..utils.config import get_config_root

_credential_file = join(get_config_root(), 'credential')

def get_login_ticket() -> Optional[str]:
    try:
        with open(_credential_file, 'r') as f:
            return f.read()
    except (FileNotFoundError, IOError):
        return None

def save_login_ticket(value: str):
    try:
        with open(_credential_file, 'w') as f:
            f.write(value)
    except IOError:
        print("Error saving the login ticket.")
