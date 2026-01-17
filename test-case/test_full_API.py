import pytest
from common.send_request import SendRequest
from constant.constant import variable_cache
from utils.assertion_util import *


class TestFullAPI:
    """完整API测试类
    
    使用参数化测试和数据驱动的方式测试多个API接口
    """
    
    def setup_class(self):
        """测试类初始化"""
        self.send_request = SendRequest()
        
    def teardown_class(self):
        """测试类清理"""
        # 清理全局变量缓存
        variable_cache.clear()
    @pytest.mark.parametrize("case_data_path", get_test_data_path())
    def test_api_with_excel_data(self, case_data_path, get_case_data):

        for index, case_data in enumerate(get_case_data, 2):

            response_data =self.send_request.send(method=case_data.get("method"),
                                                  url=case_data.get("url"),
                                                  headers=case_data.get("header"),
                                                  params=case_data.get("params"),
                                                  data=case_data.get("data"),
                                                  json=case_data.get("json"),
                                                  files=case_data.get("files"),
                                                  )


            for i in case_data.get("exception"):
                if i.get["asset_type"]) == "status_code":
                    assert_status_code(response_data.status_code,i.get("excpect_value"))
                assert_body_value(response_data, exp=i.get("exp"),expected_value=i.get("excpect_value"))

