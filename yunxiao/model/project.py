from .base import *
from .member import Member
from .status import Status
from .workitemtype import WorkItemType

class Project(ModelBase):
    '''
    {
        'categoryIdentifier': 'Project',
        'creator': '1234567890',
        'customCode': 'ABC',
        'description': '',
        'gmtCreate': 1728538669000,
        'icon': 'https://img.alicdn.com/imgextra/i3/xxxxxxxx.png',
        'identifier': 'ffffffff',
        'name': 'NAME',
        'scope': 'private'
    }
    {
        'category': None,
        'categoryIdentifier': 'Project',
        'creator': '1234567890',
        'customCode': 'ABCD',
        'description': '',
        'gmtCreate': 1734185008000,
        'gmtModified': 1738839913000,
        'hasSuperiorSpace': True,
        'icon': 'https://img.alicdn.com/imgextra/i2/xxx.png',
        'iconBig': 'https://img.alicdn.com/imgextra/i1/xxx.png',
        'iconGroup': '{"small":"https://img.alicdn.com/imgextra/i2/xxx.png","big":"https://img.alicdn.com/imgextra/i1/xxx.png"}',
        'iconSmall': 'https://img.alicdn.com/imgextra/i2/xxx.png',
        'id': None,
        'identifier': 'ffffffff',
        'identifierPath': 'ffffffff',
        'logicalStatus': 'NORMAL',
        'modifier': '1234567890',
        'name': 'NAME',
        'organizationIdentifier': 'ffffffff',
        'parentIdentifier': None,
        'scope': 'public',
        'statusIdentifier': 'ffffffff',
        'statusStageIdentifier': '9',
        'subType': None,
        'typeIdentifier': 'AgileProject'
    }
    '''

    def __init__(self, **kwargs: Any) -> None:
        members: List[Member] = kwargs.pop("members", [])
        statuses: Dict[str, List[Status]] = kwargs.pop("statuses", {})
        workitemtypes: Dict[str, List[WorkItemType]] = kwargs.pop("workitemtypes", {})
        super().__init__(**kwargs)
        self._members: List[Member] = []
        self.members = members  # Use the setter to ensure binding
        self._statuses: Dict[str, List[Status]] = {}
        self.statuses = statuses  # Use the setter to ensure binding
        self._workitemtypes: Dict[str, List[WorkItemType]] = {}
        self.workitemtypes = workitemtypes  # Use the setter to ensure binding

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Project):
            return False
        return self.identifier == other.identifier

    @property
    def members(self) -> List[Member]:
        """Return a copy of the members list to prevent direct modification."""
        return self._members.copy()

    @members.setter
    def members(self, value: List[Member]) -> None:
        """Bind members to this project when set."""
        self._members = value

    @property
    def statuses(self) -> Dict[str, List[Status]]:
        """Return a copy of the statuses list to prevent direct modification."""
        return self._statuses.copy()

    @statuses.setter
    def statuses(self, value: Dict[str, List[Status]]) -> None:
        """Bind statuses to this project when set."""
        self._statuses = value

    def statuses_for(self, category: str) -> List[Status]:
        """Get the list of statuses for a specific work item category."""
        return self.statuses.get(category, [])

    def save_statuses_for(self, category: str, value: List[Status]) -> None:
        """Save the list of statuses for a specific work item category."""
        self._statuses[category] = value

    @property
    def workitemtypes(self) -> Dict[str, List[WorkItemType]]:
        """Return a copy of the workitem types list to prevent direct modification."""
        return self._workitemtypes.copy()

    @workitemtypes.setter
    def workitemtypes(self, value: Dict[str, List[WorkItemType]]) -> None:
        """Bind workitem types to this project when set."""
        self._workitemtypes = value

    def workitemtypes_for(self, category: str) -> List[WorkItemType]:
        """Get the list of workitem types for a specific work item category."""
        return self.workitemtypes.get(category, [])

    def save_workitemtypes_for(self, category: str, value: List[WorkItemType]) -> None:
        """Save the list of workitem types for a specific work item category."""
        self._workitemtypes[category] = value
