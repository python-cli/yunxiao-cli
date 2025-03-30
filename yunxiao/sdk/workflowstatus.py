from .base import *
from ..model import Status
from .category import Category

class API(APIBase):

    @staticmethod
    def create_api_info(
        organization_id: str,
    ) -> open_api_models.Params:
        """
        API 相关
        @param path: string Path parameters
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='ListWorkItemWorkFlowStatus',
            # 接口版本,
            version='2021-06-25',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='GET',
            auth_type='AK',
            style='ROA',
            # 接口 PATH,
            pathname=f'/organization/{organization_id}/workitems/workflow/listWorkflowStatus',
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
    ) -> List[Status]:
        client = API.create_client()
        params = API.create_api_info(organization)
        # query params
        queries = {}
        queries['spaceType'] = 'Project'
        queries['workitemCategoryIdentifier'] = category
        queries['spaceIdentifier'] = project
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries)
        )

        try:
            dict = client.call_api(params, request, runtime)
            data = dict.get('body', {}).get('statuses') or []
            return [Status(**d) for d in data]
        except Exception as e:
            return []
