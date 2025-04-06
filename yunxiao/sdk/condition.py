from typing import Dict, List, Union

class Condition:
    def __init__(self, dict) -> None:
        self._dict = dict

    @classmethod
    def assigned_to(cls, value: str) -> 'Condition':
        """Initialize a condition for assigned_to field"""
        return cls({
            "fieldIdentifier": "assignedTo",
            "operator": "CONTAINS",
            "value": [value],
            "toValue": None,
            "className": "user",
            "format": "list"
        })

    @classmethod
    def status_contains(cls, value: Union[str, List[str]]) -> 'Condition':
        """Initialize a condition for status field"""
        return cls({
            "fieldIdentifier": "status",
            "operator": "CONTAINS",
            "value": [value] if isinstance(value, str) else value,
            "toValue": None,
            "className": "status",
            "format": "list"
        })

    @classmethod
    def status_not_contains(cls, value: Union[str, List[str]]) -> 'Condition':
        """Initialize a condition for status field"""
        return cls({
            "fieldIdentifier": "status",
            "operator": "NOT_CONTAINS",
            "value": [value] if isinstance(value, str) else value,
            "toValue": None,
            "className": "status",
            "format": "list"
        })

    @property
    def dict(self) -> Dict:
        return self._dict

class ConditionGroup:
    def __init__(self) -> None:
        self._conditions = []

    def add(self, condition: Condition) -> None:
        self._conditions.append(condition)

    @property
    def dict(self) -> Dict:
        return {
            "conditionGroups": [
                list(map(lambda x: x.dict, self._conditions))
            ]
        }
