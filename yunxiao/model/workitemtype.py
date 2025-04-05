from .base import *
from .workitemfield import WorkItemField

class WorkItemType(ModelBase):
    '''
    工作项类型

    {
      "systemDefault": true,
      "identifier": "xxxxxxxx",
      "creator": "AK-ADMIN",
      "enable": false,
      "addUser": "AK-ADMIN",
      "name": "任务",
      "description": "",
      "nameEn": "Task",
      "gmtAdd": 1728538669000,
      "categoryIdentifier": "Task",
      "gmtCreate": 1616584627000,
      "defaultType": false
    }
    '''

    def __init__(self, **kwargs: Any) -> None:
        fields: List[WorkItemField] = kwargs.pop("fields", [])
        super().__init__(**kwargs)
        self._fields: List[WorkItemField] = []
        self.fields = fields  # Use the setter to ensure binding

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WorkItemType):
            return False
        return self.identifier == other.identifier

    @property
    def fields(self) -> List[WorkItemField]:
        """Return a copy of the fields to prevent direct modification."""
        return self._fields.copy()

    @fields.setter
    def fields(self, value: List[WorkItemField]) -> None:
        """Bind fields to this project when set."""
        self._fields = value
