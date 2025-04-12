import click

from dataclasses import dataclass

from ..sdk import *
from .config import *
from .cache import *
from ..web import *

@dataclass
class GlobalState:
    _instance = None
    _organization: Organization = None 

    @classmethod
    def current(cls) -> 'GlobalState':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def user_id(self) -> str:
        '''Return the current user id.'''
        return get_aliyun_account_id() or fetch_user_id()

    @property
    def organization(self) -> Organization:
        '''Return the working on organization.'''
        if self._organization:
            return self._organization

        self._organization = get_cached_organization(True)

        if self._organization is None:
            raise click.exceptions.Exit(1)
        
        return self._organization

    @property
    def organization_id(self) -> str:
        '''Return the working on organization's id.'''
        return self.organization.id

    def save_organization(self):
        '''Save the working organization's changes to local cache.'''
        save_cached_organization(self.organization)

    def get_all_projects(self, reload: bool = False, reload_project_set: bool = False) -> List[Project]:
        '''Get all the projects under the working organization.'''
        all_projects = self.organization.projects

        if reload:
            # Fetch builtin projects
            all_projects = ProjectListAPI.run(self.organization_id)

            # Fetch the user's following projects
            for p in get_following_projects():
                if p not in all_projects:
                    all_projects.append(p)

            if reload_project_set:
                # Fetch from the user's project sets
                for p in self.get_all_projects_by_web():
                    if p not in all_projects:
                        all_projects.append(p)

            i, total = 1, len(all_projects)
            result_projects = []

            for p in all_projects:
                click.echo(f'Fetching {i}/{total}')
                i += 1

                click.echo(f'Fetching project details: {p.identifier}')
                project = ProjectDetailAPI.run(self.organization_id, p.identifier)

                click.echo(f'Fetching project members')
                members = MemberListAPI.run(self.organization_id, p.identifier)
                if members:
                    project.members = members

                click.echo(f'Fetching project workflow statuses')
                for category in list(Category):
                    statuses = WorkFlowStatusAPI.run(self.organization_id, p.identifier, category.value)
                    if statuses:
                        project.save_statuses_for(category.value, statuses)

                click.echo(f'Fetching project workitem\'s types and fields')
                for category in list(Category):
                    types = WorkItemTypeAPI.run(self.organization_id, p.identifier, category.value)

                    for t in types:
                        t.fields = WorkItemFieldAPI.run(self.organization_id, p.identifier, t.identifier)

                    project.save_workitemtypes_for(category.value, types)

                result_projects.append(project)
                click.secho(f'Reloaded project {project.name}\n', fg='green', bold=True)

            all_projects = result_projects
            self.organization.projects = all_projects
            self.save_organization()

        return all_projects

    def get_all_projects_by_web(self) -> List[Project]:
        ticket = get_login_ticket()

        if ticket:
            data = fetch_user_info(ticket)

            if data:
                if data.get('tenantId') != self.organization_id:
                    click.echo('Not a matching organization, you should switch your organization to prefer one and try again.')
                    click.echo(f'{data}')
                    return
            else:
                click.echo(f'Login ticket may get expired: {ticket}')
                ticket = None

        if ticket is None:
            click.echo('Opening chrome browser to get a access ticket of aliyun...')
            ticket = request_aliyun_login_ticket()

            if ticket:
                save_login_ticket(ticket)

        if not ticket:
            return
        
        all_projects = []
        all_project_sets = fetch_project_sets(ticket) or []

        if len(all_project_sets) > 0:
            for projectset in all_project_sets:
                id = projectset.get('identifier')
                name = projectset.get('name')
                click.echo(f'Fetching project set {name} ({id})')
                all_projects.extend(fetch_projects(id, ticket))
        else:
            click.echo('No project set found')
        
        return all_projects

    def get_matching_members(self, user) -> List[Member]:
        results = []

        for project in self.organization.projects:
            for member in project.members:
                if member.identifier == user or member.realName == user:
                    results.append(member)
        
        return results

    def get_matching_member_name(self, user) -> str:
        members = self.get_matching_members(user)
        return members[0].realName if len(members) > 0 else user

    def get_matching_status(self, name) -> List[Status]:
        results = []

        for project in self.organization.projects:
            for _, statuses in project.statuses.items():
                for status in statuses:
                    if status.name == name:
                        results.append(status)
        
        return results

    def get_matching_status_ids(self, keywords) -> List[str]:
        if not keywords:
            return []

        results = []
        names = keywords.split(',')

        for project in self.organization.projects:
            for _, statuses in project.statuses.items():
                for status in statuses:
                    if status.name in names:
                        results.append(status)
        
        return list(map(lambda x: x.identifier, results))
    
    def get_matching_field_name(self, project_id: str, category_id: str, field_id: str) -> str:
        for project in self.organization.projects:
            if project.identifier != project_id:
                continue

            for category, workitemtypes in project.workitemtypes.items():
                if category != category_id:
                    continue

                for workitemtype in workitemtypes:
                    for field in workitemtype.fields:
                        if field.identifier == field_id:
                            return field.name
        
        return None

    def get_matching_field_id(self, project_id: str, category_id: str, field_name: str) -> str:
        for project in self.organization.projects:
            if project.identifier != project_id:
                continue

            for category, workitemtypes in project.workitemtypes.items():
                if category != category_id:
                    continue

                for workitemtype in workitemtypes:
                    for field in workitemtype.fields:
                        if field.name == field_name:
                            return field.identifier
        
        return None


# BEGIN - Functions

def list_workitem_by(category: Category, assigned_to: Optional[str], statuses: Optional[str] = None, not_in_statuses: Optional[str] = None):
    '''List workitem by conditions.'''

    group = ConditionGroup()

    if assigned_to:
        user_id = next(map(lambda x: x.identifier, GlobalState.current().get_matching_members(assigned_to)))
    else:
        user_id = GlobalState.current().user_id

    if user_id:
        group.add(Condition.assigned_to(user_id))

    statuses = GlobalState.current().get_matching_status_ids(statuses)
    not_in_statuses = GlobalState.current().get_matching_status_ids(not_in_statuses)

    if statuses and len(statuses) > 0:
        group.add(Condition.status_contains(statuses))

    if not_in_statuses and len(not_in_statuses) > 0:
        group.add(Condition.status_not_contains(not_in_statuses))

    for project in GlobalState.current().get_all_projects():
        workitems = WorkItemListAPI.run(GlobalState.current().organization_id, project.identifier, category.value, group.dict)
        yield project, workitems

# END - Functions