import click

from dataclasses import dataclass

from .sdk import *
from .utils.output import *
from .utils.config import *
from .utils.cache import *
from .utils.notification import *
from .utils.date import *
from .web import *

# BEGIN - Global State Singleton

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

    def get_all_projects(self, reload: bool = False) -> List[Project]:
        '''Get all the projects under the working organization.'''
        all_projects = self.organization.projects

        if reload:
            # Fetch builtin projects
            all_projects = ProjectListAPI.run(self.organization_id)

            # Fetch the user's following projects
            for p in get_following_projects():
                if p not in all_projects:
                    all_projects.append(p)

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

        if ticket is None:
            ticket = request_aliyun_login_ticket()

            if ticket:
                save_login_ticket(ticket)

        if not ticket:
            return
        
        all_projects = []

        for projectset in fetch_project_sets(ticket):
            id = projectset.get('identifier')
            name = projectset.get('name')
            click.echo(f'Fetching project set {name} ({id})')
            all_projects.extend(fetch_projects(id, ticket))
        
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

# END - Global State Singleton

# BEGIN - Functions

def _list_workitem_by(category: Category, assigned_to: Optional[str], statuses: Optional[str]):
    '''List workitem by conditions.'''

    group = ConditionGroup()

    if assigned_to:
        user_id = next(map(lambda x: x.identifier, GlobalState.current().get_matching_members(assigned_to)))
    else:
        user_id = GlobalState.current().user_id

    if user_id:
        group.add(Condition.assigned_to(user_id))

    statuses = GlobalState.current().get_matching_status_ids(statuses)

    if statuses and len(statuses) > 0:
        group.add(Condition.status(statuses))

    for project in GlobalState.current().get_all_projects():
        workitems = WorkItemListAPI.run(GlobalState.current().organization_id, project.identifier, category.value, group.dict)
        yield project, workitems

# END - Functions

@click.group()
def cli():
    """CLI tool for managing yunxiao projects"""
    pass

@cli.group(invoke_without_command=True)
@click.pass_context
def organization(ctx):
    """Project management commands"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(organization_list)

@organization.command(name='list')
def organization_list():
    """List all the organizations"""
    organizations = OrganizationListAPI.run()
    [save_cached_organization(org) for org in organizations]
    show_table_organization(organizations)

@cli.group(invoke_without_command=True)
@click.pass_context
def project(ctx):
    """Project management commands"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(project_list_builtin)

@project.command(name='list')
def project_list_builtin():
    """List the builtin projects"""
    projects = ProjectListAPI.run(GlobalState.current().organization_id)
    show_table_project(projects)

@project.command(name='all')
@click.option('--reload', '-r', is_flag=True, default=False, help='Force reload the following projects or not.')
def project_list_all(reload):
    """List the builtin and following projects."""
    projects = GlobalState.current().get_all_projects(reload)
    show_table_project(projects)

@project.command(name='field')
def project_fields_all():
    """List the builtin and following projects."""
    for project in GlobalState.current().get_all_projects():
        click.echo(f'Project: {project.name}')
        for category, workitemtypes in project.workitemtypes.items():
            click.echo(f'\tCategory: {category}')
            for workitemtype in workitemtypes:
                click.echo(f'\t\tType: {workitemtype.name}')
                # for field in workitemtype.fields:
                #     click.echo(f'\t\t\tField: {field.name}')
                click.echo(f'\t\tFields: {", ".join(sorted(map(lambda x: x.name, workitemtype.fields)))}')
        else:
            click.echo()

@project.command(name='info')
@click.argument('id', type=click.STRING, required=True)
def workitem_info(id):
    """Get project details"""
    project = ProjectDetailAPI.run(GlobalState.current().organization_id, id)
    show_table_project([project])

@project.command(name='status')
@click.option('--project', type=click.STRING, help='Project ID')
@click.option('--category', type=click.Choice([c.value for c in Category]), required=True, help='Category name')
def project_status(project, category):
    """List the project's statuses."""
    if project:
        all_projects = [ProjectDetailAPI.run(GlobalState.current().organization_id, project)]
    else: 
        all_projects = GlobalState.current().get_all_projects()

    for project in all_projects:
        statuses = WorkFlowStatusAPI.run(GlobalState.current().organization_id, project.identifier, category)
        if statuses:
            project.statuses = statuses
            GlobalState.current().save_organization()
            show_content('Project: ', project.name)
            show_table_project_status(statuses)

@project.command(name='member')
@click.option('--project', type=click.STRING, help='Project ID')
def member_list(project):
    """List all members under the project"""
    if project:
        all_projects = [ProjectDetailAPI.run(GlobalState.current().organization_id, project)]
    else:
        all_projects = GlobalState.current().get_all_projects()

    for project in all_projects:
        members = MemberListAPI.run(GlobalState.current().organization_id, project.identifier)
        if members:
            project.members = members
            GlobalState.current().save_organization()
            show_content('Project: ', project.name)
            show_table_member(members)

@cli.group(invoke_without_command=True)
@click.pass_context
def workitem(ctx):
    """Workitem management commands"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(workitem_task_list)

@workitem.command(name='task')
@click.option('--assigned-to', type=click.STRING, help='User ID/Name')
@click.option('--statuses', type=click.STRING, help='Workitem statuses, use comma as separator')
def workitem_task_list(assigned_to, statuses):
    """List task workitems with filters"""
    for project, workitems in _list_workitem_by(Category.Task, assigned_to, statuses):
        if workitems:
            show_content('Project: ' , project.name)
            show_table_workitem(workitems)

@workitem.command(name='bug')
@click.option('--assigned-to', type=click.STRING, help='User ID/Name')
@click.option('--statuses', type=click.STRING, help='Workitem statuses, use comma as separator')
def workitem_bug_list(assigned_to, statuses):
    """List bug workitems with filters"""
    for project, workitems in _list_workitem_by(Category.Bug, assigned_to, statuses):
        if workitems:
            show_content('Project: ' , project.name)
            show_table_workitem(workitems)

@workitem.command(name='reminder')
@click.option('--statuses', type=click.STRING, help='Workitem statuses, use comma as separator')
def workitem_bug_list(statuses):
    """Remind the watching workitems."""
    content = ''

    for project, workitems in _list_workitem_by(Category.Task, None, statuses):
        if workitems:
            content += project.name + ':\n'
            
            for item in workitems:
                print(format_timestamp(int(item.modifier)))
                breakpoint()
                content += '\t' + item.subject + '\n'
            else:
                content += '\n'

    for project, workitems in _list_workitem_by(Category.Bug, None, statuses):
        if workitems:
            content += project.name + ':\n'

            for item in workitems:
                content += '\t' + item.subject + '\n'
            else:
                content += '\n'

    show_dialog('Reminder', content.strip())

@workitem.command(name='info')
@click.argument('id', type=click.STRING, required=True)
def workitem_info(id):
    """Get workitems details"""

    org = GlobalState.current().organization_id
    # Get the basic info of work item w/o custom fields
    workitem = WorkItemDetailAPI.run(org, id)
    # Get the basic info of work item with custom fields
    workitem = WorkItemDetailAPI.run(org, workitem.identifier)

    show_panel_workitem(workitem)

@cli.command(name='test')
def test_entry():
    """Test"""
    pass

if __name__ == '__main__':
    cli()
