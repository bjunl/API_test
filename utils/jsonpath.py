from jsonpath_ng import parse, JSONPath
from typing import Any


def jsonpath(json_data: dict, jsonpath: str) -> list[Any]:
    """
    解析JSON数据并返回匹配的节点列表

    Args:
        json_data (dict): JSON数据
        jsonpath (str): JSONPath表达式

    Returns:
        list: 匹配的节点列表
    """
    jsonpath_expr: JSONPath = parse(jsonpath)
    return [match.value for match in jsonpath_expr.find(json_data)]
