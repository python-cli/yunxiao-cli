from os import makedirs, chmod
from os.path import join, exists, expanduser
from typing import Tuple, List, Dict, Optional, Any, Union
import yaml
from textwrap import dedent

# from .plugin import DoPlugin, ListPlugin, InfoPlugin

_root = expanduser('~/.config/yunxiao-cli')
exists(_root) or makedirs(_root, exist_ok=True)  # type: ignore[func-returns-value]

_config = None
_config_file = join(_root, 'config.yaml')

def _load_config() -> dict:
    global _config

    if _config is not None:
        return _config

    if not exists(_config_file):
        content = dedent('''
        # User Credential
        # https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair
        CREDENTIAL:
            access_key_id: 
            access_key_secret: 

        TEAM:
            endpoint: devops.cn-hangzhou.aliyuncs.com
            organization: 
            project: 
        ''')

        with open(_config_file, 'w') as file:
            file.write(content)
        
        chmod(_config_file, 0o600)  # u=rw,g=,o=

    with open(_config_file) as file:
        _config = yaml.load(file, Loader=yaml.FullLoader)

    return _config

def get_config_file() -> str:
    return _config_file

def get_credential() -> Tuple[str, str]:
    config = _load_config()
    access_key_id = config.get('CREDENTIAL', {}).get('access_key_id')
    access_key_secret = config.get('CREDENTIAL', {}).get('access_key_secret')

    return access_key_id, access_key_secret

def get_organization() -> str:
    return _load_config().get('TEAM', {}).get('organization')

def get_project() -> str:
    return _load_config().get('TEAM', {}).get('project')

def get_endpoint() -> str:
    return _load_config().get('TEAM', {}).get('endpoint')
