from .base import *

class WorkItemField(ModelBase):
    '''
    工作项字段

    {
      "identifier": "subject",
      "isRequired": true,
      "name": "标题",
      "format": "input",
      "description": "标题不能为空",
      "className": "string",
      "type": "NativeField"
    }
    {
      "identifier": "assignedTo",
      "isRequired": true,
      "gmtModified": 1728538669000,
      "isShowWhenCreate": true,
      "name": "负责人",
      "format": "list",
      "description": "负责人",
      "isSystemRequired": true,
      "className": "user",
      "gmtCreate": 1728538669000,
      "type": "NativeField",
      "resourceType": "Workitem"
    }
    '''
