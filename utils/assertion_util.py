from common.response_handler import response_handler
from fixture.jsonpath_fixture import jsonpath_fixture
from requests import Response
import re


def assert_status_code(response: Response, expected_status_code: int) -> None:
    """
    断言响应状态码是否符合预期。

    Args:
        response: HTTP响应对象
        expected_status_code: 期望的状态码

    Returns:
        None: 如果断言失败会抛出AssertionError
    """
    assert expected_status_code == response.status_code


def assert_body_value(response: Response, exp: str, expected_value: str) -> None:
    """
    断言响应体中的值是否符合预期。

    支持两种模式：
    1. 字符串响应：使用正则表达式匹配
    2. JSON响应：使用JSONPath表达式提取值

    Args:
        response: HTTP响应对象
        exp: 正则表达式或JSONPath表达式
        expected_value: 期望的值

    Returns:
        None: 如果断言失败会抛出AssertionError
    """
    value = response_handler(response)
    
    if isinstance(value, str):
        # 字符串响应，使用正则表达式匹配
        match = re.search(exp, value)
        assert match is not None, f"正则表达式 '{exp}' 在响应中未找到匹配"
        assert match.group() == expected_value, f"匹配值 '{match.group()}' 不等于期望值 '{expected_value}'"
    
    elif isinstance(value, dict):
        # JSON响应，使用JSONPath提取值
        extracted_values = jsonpath_fixture(value, exp)
        assert extracted_values, f"JSONPath '{exp}' 未找到任何匹配的值"
        assert extracted_values[0] == expected_value, f"提取值 '{extracted_values[0]}' 不等于期望值 '{expected_value}'"
    
    else:
        raise TypeError(f"不支持的响应类型: {type(value)}")