from jsonpath_ng import parse

def jsonpath_fixture(json_data: dict, jsonpath_expr: str) -> list:
    """
    解析JSON数据并返回匹配的节点列表

    Args:
        json_data (dict): JSON数据
        jsonpath_expr (str): JSONPath表达式

    Returns:
        list: 匹配的节点列表
    """
    jsonpath_expr = parse(jsonpath_expr)
    return [match.value for match in jsonpath_expr.find(json_data)]