import pytest
from core.http.client import HTTPClient
from utils.constant import variable_cache
from utils.jsonpath import jsonpath
from core.http.response import response_handler
from core.assertion.assertion import *


class TestFullAPI:
    """完整API测试类
    
    使用参数化测试和数据驱动的方式测试多个API接口
    """
    
    def setup_class(self):
        """测试类初始化"""
        self.http_client = HTTPClient()
        
    def teardown_class(self):
        """测试类清理"""
        # 清理全局变量缓存
        variable_cache.clear()
    @pytest.mark.parametrize("case_data_path", get_test_data_path())
    def test_api_with_excel_data(self, case_data_path, get_test_case_data):

        for index, case_data in enumerate(get_test_case_data, 2):

            response_data =self.http_client.send_request(method=case_data.get("method"),
                                                  url=case_data.get("url"),
                                                  headers=case_data.get("header"),
                                                  params=case_data.get("params"),
                                                  data=case_data.get("data"),
                                                  json=case_data.get("json"),
                                                  files=case_data.get("files"),
                                                  )


            for i in case_data.get("exception"):
                if i.get("asset_type") == "status_code":
                    assert_status_code(response_data,i.get("excpect_value"))
                assert_body_value(response_data, exp=i.get("exp"),expected_value=i.get("excpect_value"))

            if case_data.get("variable",{}) :
                for var_name, var_value in case_data.get("variable",{}).items():
                    var_value = jsonpath(var_value, response_handler(response_data))
                    variable_cache.set_variable(var_name, var_value)

