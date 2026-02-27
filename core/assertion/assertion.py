from core.http.response import response_handler
from utils.jsonpath import jsonpath
from requests import Response
import re
from utils.logger import logger


def assert_status_code(response: Response, expected_status_code: int) -> None:
    """
    断言响应状态码是否符合预期。

    Args:
        response: HTTP响应对象
        expected_status_code: 期望的状态码

    Returns:
        None: 如果断言失败会抛出AssertionError
    """
    actual_status_code = response.status_code
    logger.debug(f"断言状态码: 期望={expected_status_code}, 实际={actual_status_code}")
    
    assert expected_status_code == actual_status_code
    
    logger.info(f"状态码断言成功: {actual_status_code}")


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
    logger.debug(f"开始断言响应体值，表达式: {exp}, 期望值: {expected_value}")
    
    value = response_handler(response)
    
    if isinstance(value, str):
        # 字符串响应，使用正则表达式匹配
        logger.debug("响应为字符串类型，使用正则表达式匹配")
        match = re.search(exp, value)
        assert match is not None, f"正则表达式 '{exp}' 在响应中未找到匹配"
        actual_value = match.group()
        assert actual_value == expected_value, f"匹配值 '{actual_value}' 不等于期望值 '{expected_value}'"
        logger.info(f"字符串响应断言成功: 匹配值={actual_value}")
    
    elif isinstance(value, dict):
        # JSON响应，使用JSONPath提取值
        logger.debug("响应为JSON类型，使用JSONPath提取值")
        extracted_values = jsonpath(value, exp)
        assert extracted_values, f"JSONPath '{exp}' 未找到任何匹配的值"
        actual_value = extracted_values[0]
        assert actual_value == expected_value, f"提取值 '{actual_value}' 不等于期望值 '{expected_value}'"
        logger.info(f"JSON响应断言成功: 提取值={actual_value}")
    
    else:
        error_msg = f"不支持的响应类型: {type(value)}"
        logger.error(error_msg)
        raise TypeError(error_msg)