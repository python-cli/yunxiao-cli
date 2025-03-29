import click

from .sdk import *
from .utils.output import *
from .utils.config import *

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
    """List all projects"""
    organizations = OrganizationListAPI.run()
    show_table_organization(organizations)

@cli.group(invoke_without_command=True)
@click.pass_context
def project(ctx):
    """Project management commands"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(project_list)

@project.command(name='list')
def project_list():
    """List all projects"""
    projects = ProjectListAPI.run(get_organization())
    show_table_project(projects)

@project.command(name='status')
def project_status():
    """List all projects"""
    statuses = WorkFlowStatusAPI.run(get_organization(), get_project(), Category.Task)
    show_table_project_status(statuses)

@project.command(name='member')
def member_list():
    """List all members under the project"""
    members = MemberListAPI.run(get_organization(), get_project())
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
    """List workitems with filters"""
    condition = {
        "conditionGroups": [
            [
                Condition.assigned_to(assigned_to or get_user_id()),
                # Condition.status(),
            ]
        ]
    }

    for project in ProjectListAPI.run(get_organization()):
        workitems = WorkItemListAPI.run(get_organization(), project.identifier, Category.Task, condition)
        if workitems:
            click.echo(f'Project: {project.name}')
            show_table_workitem(workitems)

@workitem.command(name='bug')
@click.option('--assigned-to', type=click.STRING, help='User ID')
def workitem_bug_list(assigned_to):
    """List workitems with filters"""
    condition = {
        "conditionGroups": [
            [
                Condition.assigned_to(assigned_to or get_user_id()),
            ]
        ]
    }

    for project in ProjectListAPI.run(get_organization()):
        click.echo(f'Project: {project.name}')
        workitems = WorkItemListAPI.run(get_organization(), project.identifier, Category.Bug, condition)
        show_table_workitem(workitems)

@workitem.command(name='info')
@click.argument('id', type=click.STRING, required=True)
def workitem_info(id):
    """Get workitems details"""
    workitem = WorkItemDetailAPI.run(get_organization(), id)
    show_table_workitem([workitem])

if __name__ == '__main__':
    cli()
