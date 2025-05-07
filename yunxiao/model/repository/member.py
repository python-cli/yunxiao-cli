from ..base import *
from ...utils.pinyin import get_pinyin

class RepositoryMember(ModelBase):
    '''
    {
      "externUserId": "123456",
      "accessLevel": 30,
      "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/sample.png",
      "inherited": {},
      "name": "<Username>",
      "state": "active",
      "id": 123456,
      "email": "user.name***@company.com",
      "username": "aliyun:user.name"
    }
    '''

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RepositoryMember):
            return False
        return self.id == other.id

    @property
    def name_pinyin(self):
        return get_pinyin(self.name)