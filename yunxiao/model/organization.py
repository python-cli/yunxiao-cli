from .base import *
from .project import Project
from .repository import Repository

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
        repositories: List[Repository] = kwargs.pop("repositories", [])
        breakpoint()
        super().__init__(**kwargs)
        self._projects: List[Project] = []
        self.projects = projects  # Use the setter to ensure binding
        self._repositories: List[Repository] = []
        self.repositories = repositories  # Use the setter to ensure binding

    def __setstate__(self, state):
        """Handle object deserialization from cache"""
        self.__dict__.update(state)
        if not hasattr(self, '_repositories'):
            self._repositories = []
        if not hasattr(self, '_projects'):
            self._projects = []

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

    @property
    def repositories(self) -> List[Repository]:
        """Return a copy of the repositories list to prevent direct modification."""
        return self._repositories.copy()

    @repositories.setter
    def repositories(self, value: List[Repository]) -> None:
        """Bind repositories to this organization when set."""
        self._repositories = []
        for repository in value:
            self.add_repository(repository)

    def add_repository(self, repository: Repository) -> None:
        """Add a repository to the organization and set its parent."""
        if repository not in self._repositories:
            self._repositories.append(repository)
