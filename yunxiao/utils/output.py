from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.style import Style

from typing import Iterable, Optional, List, Union, Dict, Sequence, Any
from datetime import datetime

from ..model import Organization, Project, Status, Member, WorkItem, Repository, Branch, RepositoryMember, MergeRequest

def _show_table(table_data: Iterable[Any], headers: Optional[List[str]], title: Optional[str] = None):
    console = Console()
    table = Table(title=title)
    
    # Add headers
    if headers:
        for header in headers:
            table.add_column(header)
    
    # Add rows
    for row in table_data:
        table.add_row(*[cell if isinstance(cell, Text) else str(cell) for cell in row])
    
    console.print(table)

def _add_link(text, url):
    txt = Text()
    txt.append(text, style=Style(color="green", link=url))
    return txt

def _get_username(user):
    from ..main import GlobalState
    return GlobalState.current().get_matching_member_name(user)

def _print_property(title, content):
    console = Console()
    text = Text()
    text.append(title)
    text.append(': ')

    if isinstance(content, Text):
        text.append(content)
    else:
        text.append(content, style="bold italic")

    console.print(text)

def format_date_string(value):
    date_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    return date_obj.strftime("%Y-%m-%d %H:%M")

def show_table_generic(items: Iterable[Iterable[Any]], headers=List[str]):
    '''
    Print generic iterable items with Rich table.
    '''
    _show_table(items, headers=headers)

def show_table_organization(items: Iterable[Organization]):
    '''
    Print organizations with Rich table.
    '''

    table = list(map(lambda x: [x.id, x.name, x.isOrgAdmin], items))
    headers = ['ID', 'Name', 'IsAdmin']
    _show_table(table, headers=headers)

def show_table_project(items: Iterable[Project]):
    '''
    Print projects with Rich table.
    '''

    table = list(map(lambda x: [x.identifier, x.customCode, x.name], items))
    headers = ['ID', 'Code', 'Name']
    _show_table(table, headers=headers)

def show_table_project_status(items: Iterable[Status]):
    '''
    Print projects with Rich table.
    '''

    table = list(map(lambda x: [x.identifier, x.name, x.source], items))
    headers = ['ID', 'Name', 'Source']
    _show_table(table, headers=headers)

def show_table_member(items: Iterable[Member]):
    '''
    Print members with Rich table.
    '''

    table = list(map(lambda x: [x.identifier, x.displayName, x.roleName], items))
    headers = ['ID', 'Name', 'Role']
    _show_table(table, headers=headers)

def show_table_workitem(items: Iterable[WorkItem]):
    '''
    Print work items with Rich table.
    '''
    table = list(map(lambda x: [_add_link(x.serialNumber, x.web_url), x.subject, _get_username(x.assignedTo), x.status], items))
    headers = ['NO.', 'Title', 'Assigned To', 'Status']
    _show_table(table, headers=headers)

def show_panel_workitem(item: WorkItem):
    '''
    Print work item with panel.
    '''
    from ..main import GlobalState

    def format_timestamp(value):
        from datetime import datetime, timezone
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    _print_property('ID', _add_link(item.serialNumber, item.web_url))
    _print_property('Subject', item.subject)
    _print_property('Project', item.spaceName)
    _print_property('Category', item.categoryIdentifier)
    _print_property('Assigned To', _get_username(item.assignedTo))
    _print_property('Status', item.status)
    _print_property('Update Status At', format_timestamp(item.updateStatusAt))
    _print_property('Creator', _get_username(item.creator))
    _print_property('Created At', format_timestamp(item.gmtCreate))
    _print_property('Modifier', _get_username(item.modifier))
    _print_property('Modified At', format_timestamp(item.gmtModified))
    _print_property('Finish Time', format_timestamp(item.finishTime))

    project_id = item.spaceIdentifier
    category = item.categoryIdentifier

    for field in item.customFields:
        field_name = GlobalState.current().get_matching_field_name(project_id, category, field.get('fieldIdentifier'))
        field_value = item.get_display_value_of_custom_field(field.get('fieldIdentifier'))
        _print_property(field_name, field_value)

def show_content(title: str, content: str):
    console = Console()
    text = Text()
    text.append(title)
    text.append(content, style="bold italic")
    console.print(text)

def show_table_repository(items: Iterable[Repository]):
    '''
    Print repositories with Rich table.
    '''

    def format_repo_path(path):
        components = path.split('/')
        return '/'.join(components[1:])

    table = list(map(lambda x: [_add_link(x.path, x.webUrl), format_repo_path(x.pathWithNamespace), format_date_string(x.updatedAt)], items))
    headers = ['Name', 'Path', 'Update At']
    _show_table(table, headers=headers)

def show_table_branch(items: Iterable[Branch]):
    '''
    Print branches with Rich table.
    '''

    table = list(map(lambda x: [x.name, x.commit.get('shortId'), x.commit.get('authorName'), x.commit.get('title'), format_date_string(x.commit.get('committedDate'))], items))
    headers = ['Name', 'Last Commit ID', 'Last Commit User', 'Last Commit Message', 'Last Commit Date']
    _show_table(table, headers=headers)

def show_table_repository_member(items: Iterable[RepositoryMember]):
    '''
    Print repository members with Rich table.
    '''

    table = list(map(lambda x: [x.id, x.name, x.email], items))
    headers = ['ID', 'Name', 'Email']
    _show_table(table, headers=headers)

def show_table_merge_request(items: Iterable[MergeRequest]):
    '''
    Print merge requests with Rich table.
    '''

    def format_branch(mr):
        return _add_link(f'{mr.sourceBranch} -> {mr.targetBranch}', mr.detailUrl)

    table = list(map(lambda x: [x.localId, x.repo_name, format_branch(x), x.title, format_date_string(x.updatedAt), x.author.get('name'), x.newVersionState], items))
    headers = ['ID', 'Repo', 'Branch', 'Title', 'Updated At', 'Author', 'Status']
    _show_table(table, headers=headers)

def show_panel_merge_request(item: MergeRequest):
    '''
    Print merge request with table.
    '''

    _print_property('ID', _add_link(f'{item.localId}', item.detailUrl))
    _print_property('Title', item.title)
    _print_property('Project', item.targetProjectPathWithNamespace)
    _print_property('Source branch', item.sourceBranch)
    _print_property('Target branch', item.targetBranch)
    _print_property('Author', item.author.get('name'))
    _print_property('Status', item.status)
    _print_property('Create At', format_date_string(item.createTime))
    _print_property('Update At', format_date_string(item.updateTime))
