from .base import *
from .project import Project

class Organization(ModelBase):
    '''
    {
      "isOrgAdmin": false,
      "name": "XXX公司",
      "id": "ffffffff"
    }
    '''

    def __init__(self, **kwargs: Any) -> None:
        projects: List[Project] = kwargs.pop("projects", [])
        super().__init__(**kwargs)
        self._projects: List[Project] = []
        self.projects = projects  # Use the setter to ensure binding

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Organization):
            return False
        return self.id == other.id

    @property
    def projects(self) -> List[Project]:
        """Return a copy of the projects list to prevent direct modification."""
        return self._projects.copy()

    @projects.setter
    def projects(self, value: List[Project]) -> None:
        """Bind projects to this organization when set."""
        self._projects = []
        for project in value:
            self.add_project(project)

    def add_project(self, project: Project) -> None:
        """Add a project to the organization and set its parent."""
        if project not in self._projects:
            self._projects.append(project)
