from abc import ABC
from typing import Any, List, Dict, Optional

class ModelBase(ABC):

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _format_value(self, value: Any, indent: int = 0) -> str:
        if isinstance(value, dict):
            items = []
            for k, v in sorted(value.items()):
                items.append(f"{'  ' * (indent + 1)}{k}={self._format_value(v, indent + 1)}")
            return "{\n" + "\n".join(items) + f"\n{'  ' * indent}}}"
        elif isinstance(value, (list, tuple)):
            items = []
            for v in value:
                items.append(f"{'  ' * (indent + 1)}{self._format_value(v, indent + 1)}")
            return "[\n" + "\n".join(items) + f"\n{'  ' * indent}]"
        elif isinstance(value, ModelBase):
            return value.__class__.__name__ + "(\n" + "\n".join(
                f"{'  ' * (indent + 1)}{k}={self._format_value(v, indent + 1)}"
                for k, v in sorted(value.__dict__.items())
            ) + f"\n{'  ' * indent})"
        return str(value)

    def __repr__(self):
        items = []
        for key, value in sorted(self.__dict__.items()):
            items.append(f"  {key}={self._format_value(value, 1)}")
        return f"{self.__class__.__name__}(\n" + "\n".join(items) + "\n)"
