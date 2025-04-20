from .base import *
from ..model import MergeRequestDetail
from ..utils.config import *

class API(APIBase):

    @staticmethod
    def create_api_info(repository_id: str, local_id: str) -> open_api_models.Params:
        """
        API 相关
        @param path: string Path parameters
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='GetMergeRequest',
            # 接口版本,
            version='2021-06-25',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='GET',
            auth_type='AK',
            style='ROA',
            # 接口 PATH,
            pathname=f'/api/v4/projects/{repository_id}/merge_requests/{local_id}/detail',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    @staticmethod
    def run(
        organization: str,
        repository_id: str,
        local_id: str,
    ) -> None:
        client = API.create_client()
        params = API.create_api_info(repository_id, local_id)
        # query params
        queries = {}
        queries['organizationId'] = organization
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries)
        )
        dict = client.call_api(params, request, runtime)
        data = dict.get('body', {}).get('result')
        return MergeRequestDetail(**data) if data else None
