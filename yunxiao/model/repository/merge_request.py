from ..base import *

class MergeRequest(ModelBase):
    '''
    {
      "workInProgress": false,
      "sourceProjectId": 123456,
      "description": "message...",
      "mrBizId": "ffffffff",
      "title": "feat: add something magic",
      "localId": 123,
      "creationMethod": "WEB",
      "createdAt": "2025-04-20T15:27:38+08:00",
      "newMergeRequestIdentifier": true,
      "state": "accepted",
      "updatedAt": "2025-04-20T15:27:38+08:00",
      "sourceBranch": "feature/magic",
      "targetProjectId": 123456,
      "subscribers": [],
      "author": {
        "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/sample.png",
        "name": "bot",
        "id": 123456,
        "state": "active",
        "email": "user.name@company.com",
        "username": "aliyun:username_xyz"
      },
      "targetType": "BRANCH",
      "reviewers": [
        {
          "hasReviewed": false,
          "hasCommented": false,
          "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/sample.png",
          "name": "bot",
          "id": 123456,
          "state": "active",
          "email": "user.name@company.com",
          "username": "aliyun:aliyunxxxx_yyyy",
          "status": "pending"
        }
      ],
      "supportMergeFFOnly": false,
      "newVersionState": "TO_BE_MERGED",
      "labels": [],
      "targetBranch": "develop",
      "sourceType": "BRANCH",
      "nameWithNamespace": "ffffffff / sample / repo-name",
      "webUrl": "https://codeup.aliyun.com/ffffffff/sample/repo-name",
      "detailUrl": "https://codeup.aliyun.com/ffffffff/sample/repo-name/change/772",
      "projectId": 123456
    }
    '''

    @property
    def repo_name(self):
        return self.nameWithNamespace.split('/')[-1].strip()

    @property
    def merged_by_user(self) -> str:
        return next((a.get('name') for a in self.reviewers if a.get('reviewOpinionStatus') == 'PASS'), '')

class MergeRequestDetail(ModelBase):
    '''
    {
        "todoList": {
            "requirementCheckItems": []
        },
        "sourceProjectId": 4704627,
        "mrBizId": "971d6b5ae0ac4e39a12856ba2e87ab2d",
        "title": "feat: update the launch image.",
        "targetProjectPathWithNamespace": "1234567890/project/repo",
        "localId": 64,
        "createFrom": "WEB",
        "mrType": "CODE_REVIEW",
        "allRequirementsPass": true,
        "sourceBranch": "launch",
        "mergedRevision": "f0ac91f6b6673c61a541fdeed090ce5563d33b68",
        "targetProjectId": 4704627,
        "subscribers": [],
        "author": {
        "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/113f27c4ed1119a605b68ef7fba226ab750c/w/200/h/200",
        "name": "",
        "id": 1525251,
        "state": "active",
        "email": "user.name",
        "username": "aliyun:user.name@qq.com_JMvf3"
        },
        "updateTime": "2025-04-15T19:27:25+08:00",
        "reviewers": [
            {
            "hasReviewed": false,
            "hasCommented": false,
            "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/sample.png",
            "name": "bot",
            "id": 123456,
            "state": "active",
            "email": "user.name@company.com",
            "username": "aliyun:aliyunxxxx_yyyy",
            "status": "pending"
            },
            {
            "hasReviewed": true,
            "hasCommented": false,
            "avatarUrl": "https://tcs-devops.aliyuncs.com/thumbnail/sample.png",
            "name": "bot",
            "id": 123456,
            "state": "active",
            "email": "user.name@company.com",
            "username": "aliyun:aliyunxxxx_yyyy",
            "status": "pending",
            "reviewOpinionStatus": "PASS",
            "reviewTime": "2025-06-25T11:01:14+08:00"
            }
        ],
        "supportMergeFastForwardOnly": false,
        "targetBranch": "develop",
        "createTime": "2025-04-15T19:20:50+08:00",
        "targetProjectNameWithNamespace": "1234567890 / project / repo",
        "webUrl": "https://codeup.aliyun.com/1234567890/project/repo",
        "detailUrl": "https://codeup.aliyun.com/1234567890/project/repo/change/64",
        "projectId": 123456,
        "status": "MERGED"
    }
    '''

    @property
    def merged_by_user(self) -> str:
        return next((a.get('name') for a in self.reviewers if a.get('reviewOpinionStatus') == 'PASS'), '')

    @property
    def reviewer_names(self) -> List[str]:
        return list(map(lambda x: x.get('name'), self.reviewers))
