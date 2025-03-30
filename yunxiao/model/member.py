from .base import *

class Member(ModelBase):
    '''
    {
        'avatar': 'https://tcs-devops.aliyuncs.com/thumbnail/ffffffff/w/100/h/100',
        'displayName': 'GOD',
        'division': {},
        'identifier': '1234567890',
        'nickName': 'GOD',
        'organizationUserInfo': {},
        'realName': 'GOD',
        'roleName': '管理员',
        'tbRoleId': 'project.admin'
    }
    '''

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Member):
            return False
        return self.identifier == other.identifier
