from .base import *
from .member import Member
from .status import Status

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
    '''

    def __init__(self, **kwargs: Any) -> None:
        members: List[Member] = kwargs.pop("members", [])
        statuses: Dict[str, List[Status]] = kwargs.pop("statuses", {})
        super().__init__(**kwargs)
        self._members: List[Member] = []
        self.members = members  # Use the setter to ensure binding
        self._statuses: Dict[str, List[Status]] = {}
        self.statuses = statuses  # Use the setter to ensure binding

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
