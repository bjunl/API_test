import re
from typing import Dict, Any, List, Tuple
from utils import yaml_util
from constant.constant import variable_cache


def replace_url(url: str) -> str:
    """
    替换url中的变量
    
    Args:
        url (str): 需要替换变量的URL字符串
        
    Returns:
        str: 替换后的URL字符串
    """
    if not url:
        return url
        
    # 查找所有形如 ${variable_name} 的变量
    keys = re.findall(r"\$\{([a-zA-Z0-9_]+)\}", url)
    if not keys:
        return url
    
    # 获取host配置
    try:
        host_config = yaml_util.read_yaml(get_yaml_path()).get("Host", {})
    except Exception as e:
        host_config = {}
    
    # 构建替换映射
    replacements = {}
    for var_name in keys:
        # 优先从host配置获取
        if var_name in host_config:
            replacements[f"${{{var_name}}}"] = host_config[var_name]
        # 其次从variable_cache获取
        else:
            cache_value = variable_cache.get_value(var_name)
            if cache_value is not None:
                replacements[f"${{{var_name}}}"] = cache_value
    
    # 执行替换
    result_url = url
    for placeholder, value in replacements.items():
        result_url = result_url.replace(placeholder, str(value))
        
    return result_url


def replace_data(data: Dict[str, Any]) -> None:
    """
    替换data中的变量
    
    Args:
        data (Dict[str, Any]): 需要替换数据的字典
        
    Returns:
        None
    """
    if not isinstance(data, dict):
        return
        
    # 使用栈来保存待处理的字典及其键值对
    stack: List[Tuple[Dict[str, Any], str, Any]] = [(data, k, v) for k, v in data.items()]
    
    while stack:
        current_dict, key, value = stack.pop()
        
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            var_name = value[2:-1]  # 提取变量名
            try:
                replacement = variable_cache.get_value(var_name)
                if replacement is not None:
                    current_dict[key] = replacement
            except Exception as e:
                print(f"Error: {e}")
        elif isinstance(value, dict):
            # 将子字典的键值对加入栈中
            stack.extend([(value, k, v) for k, v in value.items()])