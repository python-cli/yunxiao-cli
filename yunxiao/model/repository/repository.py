from ..base import *

class Repository(ModelBase):
    '''
    {
      "importStatus": "none",
      "star": false,
      "accessLevel": 0,
      "lastActivityAt": "2025-04-17T22:47:38+08:00",
      "archive": false,
      "createdAt": "2024-12-27T18:27:03+08:00",
      "path": "repo path",
      "starCount": 0,
      "namespaceId": 123456,
      "nameWithNamespace": "ffffffffffffff / sample / repo-name",
      "webUrl": "https://codeup.aliyun.com/ffffffffffffff/sample/repo-name",
      "visibilityLevel": "10",
      "name": "repo name",
      "Id": 123456,
      "pathWithNamespace": "ffffffffffffff/sample/repo-name",
      "updatedAt": "2025-04-17T22:47:38+08:00"
    }
    '''

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Repository):
            return False
        return self.Id == other.Id
