import click

from .sdk import *
from .utils.output import *
from .utils.cache import *
from .utils.date import *
from .utils.command import *
from .utils.state import *
from .web import *

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
    """List the cached projects"""
    projects = ProjectListAPI.run(GlobalState.current().organization_id)
    show_table_project(projects)

@project.command(name='all')
@click.option('--reload', '-r', is_flag=True, default=False, help='Force reload the following projects or not.')
@click.option('--reload-project-set', '-s', is_flag=True, default=False, help='Force reload the online project sets or not.')
def project_list_all(reload, reload_project_set):
    """List/Reload the builtin and following projects"""
    projects = GlobalState.current().get_all_projects(reload, reload_project_set)
    show_table_project(projects)

@project.command(name='field')
def project_fields_all():
    """List all the projects' field"""
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
    """Get workitem details"""
    project = ProjectDetailAPI.run(GlobalState.current().organization_id, id)
    show_table_project([project])

@project.command(name='status')
@click.option('--project', type=click.STRING, help='Project ID')
@click.option('--category', type=click.Choice([c.value for c in Category]), required=True, help='Category name')
def project_status(project, category):
    """List the project's statuses"""
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
@click.option('--not-in-statuses', type=click.STRING, help='Reversed workitem statuses, use comma as separator')
def workitem_task_list(assigned_to, statuses, not_in_statuses):
    """List task workitems with filters"""

    for project, workitems in list_workitem_by(Category.Task, assigned_to, statuses, not_in_statuses):
        if workitems:
            show_content('Project: ' , project.name)
            show_table_workitem(workitems)

@workitem.command(name='bug')
@click.option('--assigned-to', type=click.STRING, help='User ID/Name')
@click.option('--statuses', type=click.STRING, help='Workitem statuses, use comma as separator')
@click.option('--not-in-statuses', type=click.STRING, help='Reversed workitem statuses, use comma as separator')
def workitem_bug_list(assigned_to, statuses, not_in_statuses):
    """List bug workitems with filters"""
    for project, workitems in list_workitem_by(Category.Bug, assigned_to, statuses, not_in_statuses):
        if workitems:
            show_content('Project: ' , project.name)
            show_table_workitem(workitems)

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

@cli.command(name='test', hidden=True)
def test_entry():
    """Test"""
    pass

@cli.group(invoke_without_command=True)
@click.pass_context
def do(ctx):
    '''
    Do something magic.
    '''

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

def inject_do_commands():
    '''
    Inject the custom plugin commands definded in configuration file to
    `do` group.
    '''

    def bind(cls):
        def func(**kwargs):
            logging.debug(f'Start running plugin [{cls.name()}]')
            cls().run(**kwargs)
            logging.debug(f'Finish running plugin [{cls.name()}]')

        func.__name__ = cls.name()
        return func

    for cls in get_user_commands():
        command = click.Command(
            cls.name(),
            callback=bind(cls),
            help=cls.help(),
            params=cls.arguments() + cls.options(),
        )
        do.add_command(command)

inject_do_commands()

if __name__ == '__main__':
    cli()
