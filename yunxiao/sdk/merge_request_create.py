from .base import *
from ..model import MergeRequest
from ..utils.config import *

class API(APIBase):

    @staticmethod
    def create_api_info(repository_id: str) -> open_api_models.Params:
        """
        API 相关
        @param path: string Path parameters
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='CreateMergeRequest',
            # 接口版本,
            version='2021-06-25',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='POST',
            auth_type='AK',
            style='ROA',
            # 接口 PATH,
            pathname=f'/api/v4/projects/{repository_id}/merge_requests',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    @staticmethod
    def run(
        organization: str,
        project_id: int,
        source_branch: str,
        target_branch: str,
        title: str,
        reviewer_ids: Optional[List[str]] = None,
    ) -> None:
        client = API.create_client()
        params = API.create_api_info()
        # query params
        queries = {}
        queries['organizationId'] = organization
        queries['body'] = {
            'sourceProjectId': project_id,
            'targetProjectId': project_id,
            'sourceBranch': source_branch,
            'targetBranch': target_branch,
            'title': title,
            'createFrom': 'WEB',
            'reviewerIds': reviewer_ids,
        }
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries)
        )
        dict = client.call_api(params, request, runtime)
        data = dict.get('body', {}).get('result')
        return MergeRequest(**data) if data else None
