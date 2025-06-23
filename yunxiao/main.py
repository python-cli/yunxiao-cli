import click
import questionary as Q
from functools import reduce

from .sdk import *
from .utils.output import *
from .utils.cache import *
from .utils.date import *
from .utils.command import *
from .utils.state import *
from .utils.pinyin import *
from .utils.file import *
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

@cli.group(invoke_without_command=True, name='repo')
@click.pass_context
def repository(ctx):
    """Repository management commands"""
    if ctx.invoked_subcommand is None:
        ctx.invoke(repository_list)

@repository.command(name='list')
@click.option('--path', type=click.STRING, help='Repo path')
@click.option('--reload', '-r', is_flag=True, default=False, help='Force reload the repositories or not.')
def repository_list(path, reload):
    """List repository"""

    show_table_repository(GlobalState.current().get_all_repositories(reload))

@repository.command(name='branch')
@click.option('--repo-name', '-n', type=click.STRING, required=True, help='Repo name')
def repository_branch_list(repo_name):
    """List repository branches."""

    repo = GlobalState.current().get_repository_by_name(repo_name)
    branches = RepositoryBranchListAPI.run(GlobalState.current().organization_id, repo.Id)
    show_table_branch(branches)

@repository.command(name='member')
@click.option('--repo-name', '-n', type=click.STRING, required=True, help='Repo name')
def repository_member_list(repo_name):
    """List repository members."""

    repo = GlobalState.current().get_repository_by_name(repo_name)
    members = RepositoryMemberListAPI.run(GlobalState.current().organization_id, repo.Id)
    show_table_repository_member(members)

@cli.group(name='pr')
def merge_request():
    """Merge request management commands"""
    pass

@merge_request.command(name='list')
@click.option('--repo-name', '-n', type=click.STRING, help='Repo name')
@click.option('--author', '-u', type=click.STRING, default='me', help='Available values: all, me, <user id>, <user name>')
@click.option('--count', '-c', type=click.INT, default=5, required=True, help='Result count')
def merge_request_list(repo_name, author, count):
    """List merge requests."""

    repo_id = GlobalState.current().get_repository_by_name(repo_name).Id if repo_name else None

    if author == 'me':
        user_id = GlobalState.current().user_id
    elif author == 'all':
        user_id = None
    else:
        user_id = next(map(lambda x: x.identifier, GlobalState.current().get_matching_members(author)))

    requests = MergeRequestListAPI.run(GlobalState.current().organization_id, repo_id, user_id, count)
    show_table_merge_request(requests)

@merge_request.command(name='info')
@click.option('--repo-name', '-n', type=click.STRING, required=True, help='Repo name')
@click.option('--id', '-i', type=click.STRING, required=True, help='Identifier')
def merge_request_list(repo_name, id):
    """Show the details of merge request."""

    repo = GlobalState.current().get_repository_by_name(repo_name)
    request = MergeRequestDetailAPI.run(GlobalState.current().organization_id, repo.Id, id)
    show_panel_merge_request(request)

@merge_request.command(name='create')
@click.option('--repo-name', '-n', type=click.STRING, help='Repo name')
@click.option('--branch', '-b', type=click.STRING, help='<source-branch>:<target-branch>')
@click.option('--title', '-t', type=click.STRING, help='Title')
@click.option('--reviewers', '-r', type=click.STRING, help='Reviewers\' name (ASCII), use comma as separator')
@click.option('--interactive', '-i', is_flag=True, default=False, help='Enter interactive mode instead.')
def merge_request_create(repo_name, branch, title, reviewers, interactive):
    """Create merge request."""

    if interactive:
        all_repo_names = list(map(lambda x: x.name, GlobalState.current().get_all_repositories()))

        def validate_repo(value):
            return len(list(filter(lambda x: x == value, all_repo_names))) > 0

        def validate_branch(value):
            return len(list(filter(lambda x: x.name == value, branches))) > 0

        if repo_name and len(repo_name) > 0:
            current_repo_name = repo_name
        else:
            current_repo = get_current_working_git_repo()
            current_repo_name = os.path.basename(current_repo)

        if current_repo_name not in all_repo_names:
            current_repo_name = None

        selected_repo_name = Q.autocomplete('Repository', 
                                            choices=all_repo_names, 
                                            validate=validate_repo, 
                                            default=current_repo_name or '', 
                                            style=get_default_questionary_style()).ask()
        repo = GlobalState.current().get_repository_by_name(selected_repo_name)
        branches = RepositoryBranchListAPI.run(GlobalState.current().organization_id, repo.Id)

        default_source_branch_name, default_target_branch_name = (branch.split(':') + [None, None])[:2] if branch else (None, None)

        if default_target_branch_name is None:
            default_target_branch_name = get_default_merge_request_target_branch()

        if default_target_branch_name:
            if not next(filter(lambda x: x.name == default_target_branch_name, branches), None):
                default_target_branch_name = None

        source_branch_name = Q.autocomplete('Source branch', 
                                            choices=list(map(lambda x: x.name, branches)), 
                                            validate=validate_branch, 
                                            style=get_default_questionary_style(), 
                                            default=default_source_branch_name or '').ask()
        target_branch_name = Q.autocomplete('Target branch', 
                                            choices=list(map(lambda x: x.name, branches)), 
                                            validate=validate_branch, 
                                            style=get_default_questionary_style(), 
                                            default=default_target_branch_name or '').ask()

        source_branch = next(filter(lambda x: x.name == source_branch_name, branches), None)
        title = Q.text("Title", default=source_branch.commit.get('title'), 
                       validate=lambda text: len(text.strip()) > 0 or "Title cannot be empty", 
                       style=get_default_questionary_style()).ask()

        members = RepositoryMemberListAPI.run(GlobalState.current().organization_id, repo.Id)
        members_pinyin = list(map(lambda x: x.name_pinyin, members))
        members_meta = reduce(lambda d, s: {**d, s.name_pinyin: s.name}, members, {})
        selected_members: List[Member] = []
        selected_members.extend(list(filter(lambda x: x.name_pinyin in get_default_merge_request_reviewers(), members)))

        def validate_member(value):
            if len(value) <= 0: return True
            return len(list(filter(lambda x: x == value, members_pinyin))) > 0

        while True:
            name = Q.autocomplete('Add reviewer', choices=members_pinyin, 
                                  meta_information=members_meta, validate=validate_member, 
                                  style=get_default_questionary_style()).ask()

            if name is None or len(name) <= 0:
                break

            member = next(filter(lambda x: x.name_pinyin == name, members), None)
            if member and member not in selected_members:
                selected_members.append(member)

        show_content('All reviewers: ', ', '.join(list(map(lambda x: x.name, selected_members))))
        selected_member_ids = GlobalState.current().get_merge_request_reviewer_ids(selected_members)

        if not Q.confirm('Confirm?', style=get_default_questionary_style()).ask():
            raise click.Abort()
    else:
        repo = GlobalState.current().get_repository_by_name(repo_name)
        branches = RepositoryBranchListAPI.run(GlobalState.current().organization_id, repo.Id)

        source_branch_name, target_branch_name = branch.split(':')
        source_branch = next(filter(lambda x: x.name == source_branch_name, branches), None)
        target_branch = next(filter(lambda x: x.name == target_branch_name, branches), None)

        if source_branch is None:
            raise click.ClickException(f'Branch "{source_branch_name}" not found')
        if target_branch is None:
            raise click.ClickException(f'Branch "{target_branch_name}" not found')

        title = source_branch.commit.get('title')

        if title is None:
            raise click.ClickException(f'Title can not be empty')

        members = RepositoryMemberListAPI.run(GlobalState.current().organization_id, repo.Id)
        selected_members = list(filter(lambda x: x.name_pinyin in reviewers.split(','), members))
        selected_members.extend(list(filter(lambda x: x.name_pinyin in get_default_merge_request_reviewers(), members)))
        selected_member_ids = GlobalState.current().get_merge_request_reviewer_ids(selected_members)

        show_content('Repository:  ', repo.name)
        show_content('Branch:      ', f'{source_branch_name} -> {target_branch_name}')
        show_content('Title:       ', title)
        show_content('Reviewers:   ', ', '.join(map(lambda x: x.name, selected_members)))

    merge_request = MergeRequestCreateAPI.run(GlobalState.current().organization_id, repo.Id, source_branch_name, target_branch_name, title, selected_member_ids)
    
    if merge_request is None:
        raise click.ClickException(f'Create merge request failed, info: {merge_request}')

    click.echo(f'Created merge request {merge_request.localId} successfully!')
    click.echo(f'Link: {merge_request.detailUrl}')

@cli.command(name='test', hidden=True)
def test_entry():
    """Test"""
    pass
    repo = GlobalState.current().get_repository_by_name('TongTong')
    branches = RepositoryBranchListAPI.run(GlobalState.current().organization_id, repo.Id)

    name = Q.text("What's your name?", validate=lambda text: len(text.strip()) > 0 or "Name cannot be empty", style=get_default_questionary_style()).ask()
    color = Q.select(
        "Choose color:",
        choices=["red", "green", "blue"], style=get_default_questionary_style()
    ).ask()
    confirmed = Q.confirm("Are you sure?", style=get_default_questionary_style()).ask()

    print(f"{name} chose {color} (confirmed: {confirmed})")
    return

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
    get_default_questionary_style()
    cli()
