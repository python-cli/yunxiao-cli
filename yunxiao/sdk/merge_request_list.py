from .base import *
from ..model import MergeRequest
from ..utils.config import *

class API(APIBase):

    @staticmethod
    def create_api_info() -> open_api_models.Params:
        """
        API 相关
        @param path: string Path parameters
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='ListMergeRequests',
            # 接口版本,
            version='2021-06-25',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='GET',
            auth_type='AK',
            style='ROA',
            # 接口 PATH,
            pathname=f'/api/v4/projects/merge_requests/advanced_search',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    @staticmethod
    def run(
        organization: str,
        project_ids: Optional[str] = None,
        author_ids: Optional[str] = None,
        page_size: int = 20,
    ) -> None:
        client = API.create_client()
        params = API.create_api_info()
        # query params
        queries = {}
        queries['organizationId'] = organization
        queries['authorIds'] = author_ids
        queries['projectIds'] = project_ids
        queries['pageSize'] = page_size
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries)
        )
        dict = client.call_api(params, request, runtime)
        data = dict.get('body', {}).get('result') or []
        return [MergeRequest(**d) for d in data]
