from .base import *

class Status(ModelBase):
    '''
    {
      "identifier": "100005",
      "creator": "AK-ADMIN",
      "workflowStageName": "确认阶段",
      "name": "待处理",
      "description": "",
      "source": "system",
      "gmtCreate": 1613805843000,
      "workflowStageIdentifier": "1",
      "resourceType": "Workitem"
    }
    '''

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Status):
            return False
        return self.identifier == other.identifier
