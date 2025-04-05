from typing import List, Dict, Any
from abc import ABC, abstractmethod
from json import dumps, loads

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient

from ..utils.config import get_credential, get_endpoint

#
# Docs:
# https://api.aliyun.com/api/devops/
#

class APIBase(ABC):
    """Abstract base class for API endpoints"""
    
    @staticmethod
    def create_client() -> OpenApiClient:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        id, secret = get_credential()
        config = open_api_models.Config(access_key_id=id, access_key_secret=secret, endpoint=get_endpoint())
        return OpenApiClient(config)

    @staticmethod
    @abstractmethod
    def create_api_info(**kwargs) -> open_api_models.Params:
        """
        API 相关
        @param path: string Path parameters
        @return: OpenApi.Params
        """
        pass

    @staticmethod
    @abstractmethod
    def run(**kwargs) -> Any | None:
        """
        Send API request.
        """
        pass
