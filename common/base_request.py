'''
FilePath: \API_Test\common\base_request.py
Date: 2022-09-02
Author: @author
Email: @author_email
Environment: @env
Description: Description
'''

from requests import Request, Session


class BaseRequest():

    _session = None

    @classmethod
    def session(cls):
        if cls._session is None:
            cls._session = Session()
        return cls._session

    @classmethod
    def send_api(cls,
                 url,
                 method,
                 parametric_key,
                 params=None,
                 header=None,
                 data=None,
                 file=None) -> object:
        """
        :param method: 请求方法
        :param url: 请求url
        :param parametric_key: 入参关键字， params(查询参数类型，明文传输，一般在url?参数名=参数值), data(一般用于form表单类型参数)
        json(一般用于json类型请求参数)
        :param data: 参数数据，默认等于None
        :param file: 文件对象
        :param header: 请求头
        :return: 返回res对象
        """

        if parametric_key == "" or parametric_key == None:
            res = cls.send_request(method=method,
                                   url=url,
                                   params=params,
                                   headers=header)


        elif parametric_key == "data":
            res = cls.send_request(method=method,
                                   url=url,
                                   params=params,
                                   data=data,
                                   files=file,
                                   headers=header)

                                   
        elif parametric_key == "json":
            res = cls.send_request(method=method,
                                   url=url,
                                   params=params,
                                   json=data,
                                   files=file,
                                   headers=header)
        return res

    @classmethod
    def send_request(cls,
                     method: str,
                     url: str,
                     params: dict,
                     json: dict,
                     data: dict,
                     files: str,
                     header: dict = None) -> "Any":
        """
        预处理请求
 
        :param str method: 请求方法
        :param str url: 请求地址
        :param dict params: 关键字参数
        :param dict json: json格式消息体参数
        :param dict data: 消息体参数
        :param str files: 上传文件
        :param dict header: 请求头, defaults to None
        :return object: _description_
        """
        # 转换请求方法小写
        method = str(method).lower()
        # 创建会话
        session = cls.session()
        req = Request(method=method,
                      url=url,
                      params=params,
                      data=data,
                      json=json,
                      files=files)
        # 预处理请求,请求有固定的自定义内容，在预处理请求中可以进行处理
        prepped = session.prepare_request(req)
        if header:
            prepped.headers.update(header)

        resp = session.send(prepped, timeout=60)

        return resp