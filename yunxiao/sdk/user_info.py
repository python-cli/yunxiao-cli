from aliyunsdkcore.client import AcsClient
from aliyunsdksts.request.v20150401 import GetCallerIdentityRequest
from json import loads

from ..utils.config import *

def fetch_user_id():
    '''
    Return current user's aliyun account ID.
    '''
    id, secret = get_credential()
    client = AcsClient(id, secret, 'cn-hangzhou')
    request = GetCallerIdentityRequest.GetCallerIdentityRequest()
    response = client.do_action_with_exception(request)
    
    if not response:
        return None

    data = loads(response.decode('utf-8'))
    return data.get('UserId')
