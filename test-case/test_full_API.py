import pytest
from typing import Dict, Any
from common.send_request import SendRequest
from constant.constant import variable_cache
from fixture.data_fixture import data_processing


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
    
    @pytest.mark.parametrize(
        "test_data",
        [
            {
                "test_name": "GET请求测试",
                "method": "GET",
                "base_url": "https://jsonplaceholder.typicode.com",  # 更可靠的服务
                "endpoint": "/posts/1",
                "expected_status": [200],
                "require_internet": True
            },
            {
                "test_name": "POST请求测试",
                "method": "POST", 
                "base_url": "https://jsonplaceholder.typicode.com",
                "endpoint": "/posts",
                "json": {
                    "title": "test post",
                    "body": "This is a test post",
                    "userId": 1
                },
                "expected_status": [200, 201],
                "require_internet": True
            },
            {
                "test_name": "本地测试 - 无效URL",
                "method": "GET",
                "base_url": "http://localhost:9999",  # 故意使用不存在的本地服务
                "endpoint": "/test",
                "expected_status": [200],
                "require_internet": False,
                "expected_to_fail": True
            }
        ]
    )
    def test_api_requests(self, test_data: Dict[str, Any]):
        """参数化API请求测试
        
        Args:
            test_data: 测试数据字典，包含请求参数和期望结果
        """
        # 检查是否需要网络连接
        if test_data.get("require_internet", True):
            # 这里可以添加网络连接检查逻辑
            pass
            
        # 提取测试数据
        test_name = test_data["test_name"]
        method = test_data["method"]
        base_url = test_data["base_url"]
        endpoint = test_data.get("endpoint", "")
        url = f"{base_url}{endpoint}"
        expected_status_codes = test_data.get("expected_status", [200])
        expected_to_fail = test_data.get("expected_to_fail", False)
        
        # 根据数据类型处理请求参数
        request_kwargs = {}
        if "params" in test_data:
            request_kwargs["params"] = test_data["params"]
        if "json" in test_data:
            request_kwargs["json"] = test_data["json"]
        if "data" in test_data:
            request_kwargs["data"] = test_data["data"]
        if "headers" in test_data:
            request_kwargs["headers"] = test_data["headers"]
            
        try:
            # 发送请求
            response = self.send_request.send(method, url, **request_kwargs)
            
            # 预期失败的测试
            if expected_to_fail:
                # 如果请求应该失败但实际成功，则测试失败
                pytest.fail(f"测试 '{test_name}' 应该失败但实际成功了")
            
            # 断言验证状态码
            assert response.status_code in expected_status_codes, (
                f"测试 '{test_name}' 失败: "
                f"期望状态码 {expected_status_codes}, 实际状态码 {response.status_code}"
            )
            
            # 保存响应结果到全局变量缓存（可选）
            if response.status_code < 400:  # 只在成功响应时保存
                try:
                    variable_cache.set_value(f"response_{test_name}", response.json())
                except Exception:
                    # 如果JSON解析失败，保存原始文本
                    variable_cache.set_value(f"response_{test_name}", response.text)
            
            print(f"✅ {test_name} - 成功 (状态码: {response.status_code})")
            
        except Exception as e:
            # 如果预期会失败，那么异常是正常的
            if expected_to_fail:
                print(f"✅ {test_name} - 预期失败: {str(e)}")
                return
                
            # 对于网络错误，提供更友好的错误信息
            error_msg = str(e)
            if "connect" in error_msg.lower() or "network" in error_msg.lower():
                pytest.skip(f"测试 '{test_name}' 跳过: 网络连接问题 - {error_msg}")
            else:
                pytest.fail(f"测试 '{test_name}' 异常: {error_msg}")
    
    def test_response_data_structure(self):
        """测试响应数据结构
        
        验证不同API端点返回的响应数据是否符合预期结构
        """
        # 从全局变量缓存获取之前测试的响应
        get_response = variable_cache.get_value("response_GET请求测试")
        post_response = variable_cache.get_value("response_POST请求测试")
        
        # 验证GET响应结构 (jsonplaceholder返回的结构)
        if get_response:
            # jsonplaceholder返回的帖子数据结构验证
            assert "id" in get_response, "POST响应缺少id字段"
            assert "title" in get_response, "POST响应缺少title字段"
            assert "body" in get_response, "POST响应缺少body字段"
            assert "userId" in get_response, "POST响应缺少userId字段"
            print(f"✅ GET响应结构验证成功 - 包含所有必需字段")
        
        # 验证POST响应结构 (jsonplaceholder返回的结构)
        if post_response:
            # jsonplaceholder创建帖子后返回的数据结构验证
            expected_fields = ["id", "title", "body", "userId"]
            for field in expected_fields:
                assert field in post_response, f"POST响应缺少{field}字段"
            print(f"✅ POST响应结构验证成功 - 包含所有必需字段")
        
        # 如果缓存中没有数据，跳过详细验证
        if not get_response and not post_response:
            pytest.skip("没有可用的响应数据进行结构验证")
    
    @pytest.mark.skip(reason="需要真实API端点，待配置")
    def test_custom_api_endpoint(self):
        """测试自定义API端点（需要配置）
        
        此测试需要配置真实API端点，默认跳过
        """
        # 示例：测试自定义API
        response = self.send_request.send(
            "GET", 
            "https://api.example.com/endpoint",
            headers={"Authorization": "Bearer token"}
        )
        assert response.status_code in [200, 201]


def test_data_fixture_integration():
    """测试与data_fixture模块的集成"""
    # 模拟Excel数据
    excel_data = {
        "data_type": "json",
        "data": {"key": "value", "number": 42},
        "headers": {"Content-Type": "application/json"}
    }
    
    # 使用fixture处理数据
    processed_data = data_processing(excel_data)
    
    # 验证处理结果
    assert "json" in processed_data
    assert processed_data["json"] == {"key": "value", "number": 42}
    assert "headers" in processed_data


if __name__ == "__main__":
    # 直接运行测试（用于调试）
    pytest.main([__file__, "-v"])