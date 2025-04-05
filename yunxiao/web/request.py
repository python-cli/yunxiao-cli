import requests
from typing import Optional, Dict, List
from ..model.project import Project

def fetch_user_info(ticket: str) -> Optional[Dict]:
    url = 'https://devops.aliyun.com/uiless/api/sdk/users/me'
    cookies = {
        'login_aliyunid_ticket': ticket
    }

    response = requests.get(url, cookies=cookies)
    data = response.json()

    if data.get('code') != 200:
        print(f'Failed to get user info: {data}')
        return None

    return data.get('result')

def fetch_project_sets(ticket: str) -> Optional[Dict]:
    url = 'https://devops.aliyun.com/projex/api/workspace/program/search/list'
    params = {
        'category': 'Program',
        'toPage': 1,
        'pageSize': 20,
        '_input_charset': 'utf-8'
    }
    headers = {
        'content-type': 'application/json'
    }
    cookies = {
        'login_aliyunid_ticket': ticket
    }

    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    data = response.json()

    if data.get('code') != 200:
        print(f'Failed to get project sets: {data}')
        return None

    return data.get('result')

def fetch_projects(project_set_id: str, ticket: str) -> List[Project]:
    url = f'https://devops.aliyun.com/projex/api/workspace/program/{project_set_id}/binding/project/list'
    headers = {
        'content-type': 'application/json',
    }
    cookies = {
        'login_aliyunid_ticket': ticket
    }

    response = requests.get(url, headers=headers, cookies=cookies)
    data = response.json()

    if data.get('code') != 200:
        print(f'Failed to get project sets: {data}')
        return None

    return [Project(**d) for d in data.get('result', [])]
