from rich.table import Table
from rich.console import Console
from rich.text import Text
from rich.style import Style

from typing import Iterable, Optional, List, Union, Dict, Sequence, Any

from ..model import Organization, Project, Status, Member, WorkItem

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
    def add_link(text, url):
        txt = Text()
        txt.append(text, style=Style(color="green", link=url))
        return txt
    
    def get_username(user):
        from ..main import GlobalState
        return GlobalState.current().get_matching_member_name(user)

    table = list(map(lambda x: [add_link(x.serialNumber, x.web_url), x.subject, get_username(x.assignedTo), x.status], items))
    headers = ['NO.', 'Title', 'Assigned To', 'Status']
    _show_table(table, headers=headers)

def show_panel_workitem(item: WorkItem):
    '''
    Print work items with Rich table.
    '''
    from ..main import GlobalState

    def add_link(text, url):
        txt = Text()
        txt.append(text, style=Style(color="green", link=url))
        return txt
    
    def get_username(user):
        from ..main import GlobalState
        return GlobalState.current().get_matching_member_name(user)

    def format_timestamp(value):
        from datetime import datetime, timezone
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    def print_property(title, content):
        console = Console()
        text = Text()
        text.append(title)
        text.append(': ')

        if isinstance(content, Text):
            text.append(content)
        else:
            text.append(content, style="bold italic")

        console.print(text)

    print_property('ID', add_link(item.serialNumber, item.web_url))
    print_property('Subject', item.subject)
    print_property('Project', item.spaceName)
    print_property('Category', item.categoryIdentifier)
    print_property('Assigned To', get_username(item.assignedTo))
    print_property('Status', item.status)
    print_property('Update Status At', format_timestamp(item.updateStatusAt))
    print_property('Creator', get_username(item.creator))
    print_property('Created At', format_timestamp(item.gmtCreate))
    print_property('Modifier', get_username(item.modifier))
    print_property('Modified At', format_timestamp(item.gmtModified))
    print_property('Finish Time', format_timestamp(item.finishTime))

    project_id = item.spaceIdentifier
    category = item.categoryIdentifier

    for field in item.customFields:
        field_name = GlobalState.current().get_matching_field_name(project_id, category, field.get('fieldIdentifier'))
        field_value = item.get_display_value_of_custom_field(field.get('fieldIdentifier'))
        print_property(field_name, field_value)

def show_content(title: str, content: str):
    console = Console()
    text = Text()
    text.append(title)
    text.append(content, style="bold italic")
    console.print(text)
