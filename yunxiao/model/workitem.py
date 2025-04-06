from .base import *

class WorkItem(ModelBase):
    '''
    {
        'assignedTo': '1234567890',
        'categoryIdentifier': 'Task',
        'creator': '1234567890',
        'document': '',
        'gmtCreate': 1741345082000,
        'gmtModified': 1742377068000,
        'identifier': '1234567890',
        'logicalStatus': 'NORMAL',
        'modifier': '1234567890',
        'parentIdentifier': 'EMPTY_VALUE',
        'serialNumber': 'ABC-123',
        'spaceIdentifier': 'ffffffff',
        'spaceName': 'NAME',
        'spaceType': 'Project',
        'status': '测试中',
        'statusIdentifier': '100012',
        'statusStageIdentifier': '12',
        'subject': 'Setup environment',
        'updateStatusAt': 1742377068000,
        'workitemTypeIdentifier': 'ffffffff',
        'customFields': [
          {
            'fieldClassName': 'option',
            'fieldFormat': 'list',
            'fieldIdentifier': 'priority',
            'value': 'xxxxxxxx',
            'valueList': [{'displayValue': '中',
                          'identifier': 'xxxxxxxx',
                          'level': 4,
                          'value': '中',
                          'valueEn': 'Medium'}],
            'workitemIdentifier': 'xxxxxxxx'}]
          }
        ]
      }
    '''

    @property
    def web_url(self):
        return f'https://devops.aliyun.com/projex/project/{self.spaceIdentifier}/{self.categoryIdentifier.lower()}/{self.identifier}'

    def get_display_value_of_custom_field(self, field_id: str) -> Optional[str]:
        """
        Retrieves the value of a custom field by its identifier.
        """
        for field in self.customFields:
            if field['fieldIdentifier'] == field_id:
                return field.get('valueList', [])[0].get('displayValue')
