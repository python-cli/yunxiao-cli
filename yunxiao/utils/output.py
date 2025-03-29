from rich.table import Table
from rich.console import Console

from typing import Iterable, Union, Dict, Sequence, Any

from ..model import Organization, Project, Status, Member, WorkItem

def _show_table(table_data: Iterable[Any], headers=None):
    console = Console()
    table = Table()
    
    # Add headers
    if headers:
        for header in headers:
            table.add_column(header)
    
    # Add rows
    for row in table_data:
        table.add_row(*[str(cell) for cell in row])
    
    console.print(table)

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

    table = list(map(lambda x: [x.serialNumber, x.subject, x.assignedTo, x.status, x.updateStatusAt], items))
    headers = ['NO.', 'Title', 'Assigned To', 'Status', 'Last Modified']
    _show_table(table, headers=headers)
