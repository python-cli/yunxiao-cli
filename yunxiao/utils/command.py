from typing import Optional, List, Any
from dataclasses import dataclass
from os.path import exists, dirname, basename
import sys
import importlib
from abc import ABC, abstractmethod
from click import Parameter

class CommandBase(ABC):
    '''All the custom commands\' base class.'''

    @classmethod
    def name(cls) -> str:
        return ''

    @classmethod
    def help(cls) -> str:
        return ''
    
    @classmethod
    def arguments(cls) -> List[Parameter]:
        return []
    
    @classmethod
    def options(cls) -> List[Parameter]:
        return []

    @abstractmethod
    def run(self, **kwargs):
        """Run the command logic."""
        pass

class CommandCenter:
    '''Manage commands for dispatching.'''

    def __init__(self, commands: List[CommandBase.__subclasses__]):
        self.commands = commands

    @property
    def is_valid(self):
        return len(self.commands) > 0

    @staticmethod
    def register(path: str) -> Optional[CommandBase.__subclasses__]:
        dirpath = dirname(path)
        filename = basename(path)

        if not exists(dirpath):
            return None

        if not filename.endswith('.py'):
            return None

        module_name = filename.replace('.py', '')
        is_new_path = False

        if dirpath not in sys.path:
            sys.path.append(dirpath)
            is_new_path = True

        # Dynamically import the specified module using its filename and directory path
        module = importlib.import_module(module_name, dirpath)
        # Retrieve the Command class from the dynamically imported module
        command = getattr(module, 'Command')

        if is_new_path:
            sys.path.remove(dirpath)

        return command

    def run(self, items: List[str], **kwargs):
        for item in items:
            if exists(item):
                cmd_cls = CommandBase.register(item)

                if cmd_cls:
                    print(f'Runing command: {item}')
                    cmd_cls(**kwargs).run()
                else:
                    print('Didn\'t find a class named Command in the module')
            else:
                print(f'Invalid plugin: {item}')
