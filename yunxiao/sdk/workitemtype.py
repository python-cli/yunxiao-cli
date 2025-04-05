from .base import *
from ..model import WorkItemType

class API(APIBase):

    @staticmethod
    def create_api_info(
        organization_id: str,
        project_id: str,
    ) -> open_api_models.Params:
        """
        API 相关
        @param path: string Path parameters
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='ListProjectWorkitemTypes',
            # 接口版本,
            version='2021-06-25',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='GET',
            auth_type='AK',
            style='ROA',
            # 接口 PATH,
            pathname=f'/organization/{organization_id}/projects/{project_id}/getWorkitemType',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    @staticmethod
    def run(
        organization: str,
        project: str,
        category: str,
    ) -> None:
        client = API.create_client()
        params = API.create_api_info(organization, project)
        # query params
        queries = {}
        queries['spaceType'] = 'Project'
        queries['category'] = category
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries)
        )
        dict = client.call_api(params, request, runtime)
        data = dict.get('body', {}).get('workitemTypes') or []
        return [WorkItemType(**d) for d in data]
