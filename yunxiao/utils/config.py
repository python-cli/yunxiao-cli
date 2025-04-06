from os import makedirs, chmod
from os.path import join, exists, expanduser
from typing import Tuple, List, Dict, Optional, Any, Union
import yaml
from textwrap import dedent

from ..model import Project
from .command import CommandCenter, CommandBase

_config = None

def get_config_root() -> str:
    _root = expanduser('~/.config/yunxiao-cli')
    exists(_root) or makedirs(_root, exist_ok=True)  # type: ignore[func-returns-value]
    return _root

def _get_config_file() -> str:
    return join(get_config_root(), 'config.yaml')

def _load_config() -> dict:
    global _config

    if _config is not None:
        return _config

    config_file = _get_config_file()

    if not exists(config_file):
        content = dedent('''
        # User Credential
        # https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair
        CREDENTIAL:
            access_key_id: 
            access_key_secret:

            # Open page https://myaccount.console.aliyun.com/overview and copy the value of "账号ID"
            aliyun_account_id:

        TEAM:
            endpoint: devops.cn-hangzhou.aliyuncs.com
            organization: 

            # Following projects
            projects:
                - id: 
                  name: 
      
        COMMAND:
            - # /path/to/code.py
        ''')

        with open(config_file, 'w') as file:
            file.write(content)
        
        chmod(config_file, 0o600)  # u=rw,g=,o=

    with open(config_file) as file:
        _config = yaml.load(file, Loader=yaml.FullLoader)

    return _config

def get_credential() -> Tuple[str, str]:
    config = _load_config()
    access_key_id = config.get('CREDENTIAL', {}).get('access_key_id')
    access_key_secret = config.get('CREDENTIAL', {}).get('access_key_secret')

    return access_key_id, access_key_secret

def get_aliyun_account_id() -> str:
    return _load_config().get('CREDENTIAL', {}).get('aliyun_account_id')

def get_prefer_organization() -> str:
    return _load_config().get('TEAM', {}).get('organization')

def get_endpoint() -> str:
    return _load_config().get('TEAM', {}).get('endpoint')

def get_following_projects() -> List[Project]:
    data = [{
        'customCode': '',
        'identifier': x.get('id'),
        'name': x.get('name'),
    } for x in _load_config().get('TEAM', {}).get('projects')]

    return [Project(**x) for x in data]

def get_user_commands() -> List[CommandBase.__subclasses__]:
    result = []
    for path in _load_config().get('COMMAND', []):
        cmd_cls = CommandCenter.register(path)
        if cmd_cls:
            result.append(cmd_cls)
    return result
