from typing import Dict, List, Union

class Condition:

    @staticmethod
    def assigned_to(value: str) -> Dict:
        """AssignTo"""
        return {
            "fieldIdentifier": "assignedTo",
            "operator": "CONTAINS",
            "value": [value],
            "toValue": None,
            "className": "user",
            "format": "list"
        }

    @staticmethod
    def status(value: str) -> Dict:
        """Status"""
        return {
            "fieldIdentifier": "status",
            "operator": "CONTAINS",
            "value": [value],
            "toValue": None,
            "className": "status",
            "format":"list"
        }
