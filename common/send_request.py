from typing import Any, Dict, Literal, Optional
from requests import Request, Response, Session


type MethodType = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]


class SendRequest:
    """HTTP请求发送工具类

    该类封装了requests库，提供了一个简洁的接口来发送各种类型的HTTP请求。
    使用Session来管理连接，提高请求效率。
    """

    def __init__(self):
        """初始化SendRequest实例

        创建一个requests.Session对象用于管理HTTP连接。
        """
        self.__session = Session()

    def send(
        self,
        method: MethodType,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Any] = None,
        data: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        auth: Optional[Any] = None,
        cookies: Optional[Any] = None,
        hooks: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        timeout: int = 10,
    ) -> Response:
        """发送HTTP请求

        Args:
            method (MethodType): HTTP请求方法，可选值为 "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"
            url (str): 请求的目标URL地址
            headers (Optional[Dict[str, str]], optional): 请求头信息. Defaults to None.
            files (Optional[Any], optional): 要上传的文件. Defaults to None.
            data (Optional[Dict[str, str]], optional): 表单数据. Defaults to None.
            params (Optional[Dict[str, Any]], optional): URL参数. Defaults to None.
            auth (Optional[Any], optional): 认证信息. Defaults to None.
            cookies (Optional[Any], optional): Cookie信息. Defaults to None.
            hooks (Optional[Any], optional): 回调函数. Defaults to None.
            json (Optional[Dict[str, Any]], optional): JSON格式的请求体数据. Defaults to None.
            timeout (int, optional): 请求超时时间（秒）. Defaults to 10.

        Returns:
            Response: HTTP响应对象，包含响应状态码、响应头和响应体等信息
        """
        request = Request(
            method=method,
            url=url,
            headers=headers,
            files=files,
            data=data,
            params=params,
            json=json,
            cookies=cookies,
            hooks=hooks,
            auth=auth,
        )
        prepared_request = request.prepare()
        response = self.__session.send(prepared_request, timeout=timeout)
        return response
