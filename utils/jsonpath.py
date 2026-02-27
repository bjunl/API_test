from jsonpath_ng import parse, JSONPath
from typing import Any
from utils.logger import logger


def jsonpath(json_data: dict, jsonpath: str) -> list[Any]:
    """
    解析JSON数据并返回匹配的节点列表

    Args:
        json_data (dict): JSON数据
        jsonpath (str): JSONPath表达式

    Returns:
        list: 匹配的节点列表
    """
    logger.debug(f"开始使用JSONPath表达式解析数据: {jsonpath}")
    
    try:
        jsonpath_expr: JSONPath = parse(jsonpath)
        matches = jsonpath_expr.find(json_data)
        result = [match.value for match in matches]
        
        if result:
            logger.info(f"JSONPath解析成功，找到 {len(result)} 个匹配节点")
            logger.debug(f"匹配的值: {result}")  
        else:
            logger.warning(f"JSONPath表达式 '{jsonpath}' 未找到任何匹配节点")
        
        return result
    except Exception as e:
        logger.error(f"JSONPath解析失败，表达式: {jsonpath}, 错误: {e}")
        return []
