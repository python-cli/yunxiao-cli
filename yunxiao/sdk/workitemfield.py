from .base import *
from ..model import WorkItemField

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
            action='ListWorkItemAllFields',
            # 接口版本,
            version='2021-06-25',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='GET',
            auth_type='AK',
            style='ROA',
            # 接口 PATH,
            pathname=f'/organization/{organization_id}/workitems/fields/listAll',
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
        workitem_type_id: str
    ) -> None:
        client = API.create_client()
        params = API.create_api_info(organization)
        # query params
        queries = {}
        queries['spaceType'] = 'Project'
        queries['spaceIdentifier'] = project
        queries['workitemTypeIdentifier'] = workitem_type_id
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(queries)
        )
        # 复制代码运行请自行打印 API 的返回值
        # 返回值实际为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
        dict = client.call_api(params, request, runtime)
        data = dict.get('body', {}).get('fields') or []
        return [WorkItemField(**d) for d in data]
