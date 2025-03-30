import click

from .sdk import *
from .utils.output import *
from .utils.config import *
from .utils.cache import *

# BEGIN - Helper functions

def get_user_id():
    '''Return the current user id.'''
    return get_aliyun_account_id() or fetch_user_id()

def get_organization() -> Organization:
    org = get_cached_organization(True)

    if org is None:
        click.exceptions.Exit(1)
    
    return org

def get_organization_id() -> Organization:
    return get_organization().id

def get_all_projects(reload: bool = False) -> List[Project]:
    org = get_organization()
    cached_projects = get_cached_projects()

    if cached_projects:
        return cached_projects

    all_projects = ProjectListAPI.run(org.id)
    
    if reload:
        for p in get_following_projects():
            if p not in all_projects:
                click.echo(f'Fetching project details: {p.identifier}')
                project = ProjectDetailAPI.run(org.id, p.identifier)

                click.echo(f'Fetching project members')
                members = MemberListAPI.run(org.id, p.identifier)
                if members:
                    project.members = members

                click.echo(f'Fetching project workflow statuses')
                for category in list(Category):
                    statuses = WorkFlowStatusAPI.run(org.id, p.identifier, category.value)
                    if statuses:
                        project.save_statuses_for(category.value, statuses)

                click.secho(f'Reloaded project {project.name}\n', fg='green', bold=True)
                org.add_project(project)

        synchronize_cache()
        all_projects = org.projects

    return all_projects

# END - Helper functions

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
    save_new_organizations(organizations)
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
    projects = ProjectListAPI.run(get_organization_id())
    show_table_project(projects)

@project.command(name='all')
@click.option('--reload', '-r', is_flag=True, default=False, help='Force reload the following projects.')
def project_list_all(reload):
    """Add the target project to my following list."""
    projects = get_all_projects(reload)
    show_table_project(projects)

@project.command(name='info')
@click.argument('id', type=click.STRING, required=True)
def workitem_info(id):
    """Get project details"""
    project = ProjectDetailAPI.run(get_organization_id(), id)
    show_table_project([project])

@project.command(name='status')
@click.option('--project', type=click.STRING, help='Project ID')
@click.option('--category', type=click.Choice([c.value for c in Category]), required=True, help='Category name')
def project_status(project, category):
    """List the project's status."""
    for project in get_all_projects():
        statuses = WorkFlowStatusAPI.run(get_organization_id(), project.identifier, category)
        if statuses:
            project.statuses = statuses
            synchronize_cache()
            show_content('Project: ', project.name)
            show_table_project_status(statuses)

@project.command(name='member')
@click.option('--project', type=click.STRING, required=True, help='Project ID')
def member_list(project):
    """List all members under the project"""
    for project in get_all_projects():
        members = MemberListAPI.run(get_organization_id(), project)
        if members:
            project.members = members
            synchronize_cache()
            show_content('Project: ', project.name)
            show_table_member(members)

@cli.group(invoke_without_command=True)
@click.pass_context
def workitem(ctx):
    """Workitem management commands"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(workitem_task_list)

@workitem.command(name='task')
@click.option('--assigned-to', type=click.STRING, help='User ID')
def workitem_task_list(assigned_to):
    """List task workitems with filters"""
    condition = {
        "conditionGroups": [
            [
                Condition.assigned_to(assigned_to or get_user_id()),
                # Condition.status(),
            ]
        ]
    }

    for project in get_all_projects():
        workitems = WorkItemListAPI.run(get_organization_id(), project.identifier, Category.Task.value, condition)
        if workitems:
            show_content('Project: ' , project.name)
            show_table_workitem(workitems)

@workitem.command(name='bug')
@click.option('--assigned-to', type=click.STRING, help='User ID')
def workitem_bug_list(assigned_to):
    """List bug workitems with filters"""
    condition = {
        "conditionGroups": [
            [
                Condition.assigned_to(assigned_to or get_user_id()),
            ]
        ]
    }

    for project in get_all_projects():
        workitems = WorkItemListAPI.run(get_organization_id(), project.identifier, Category.Bug.value, condition)
        if workitems:
            show_content('Project: ' , project.name)
            show_table_workitem(workitems)

@workitem.command(name='info')
@click.argument('id', type=click.STRING, required=True)
def workitem_info(id):
    """Get workitems details"""
    workitem = WorkItemDetailAPI.run(get_organization(), id)
    show_table_workitem([workitem])

if __name__ == '__main__':
    cli()
