import re
import pathlib
from typing import Dict, Any, List, Tuple, Optional
from utils.config import read_config
from utils.constant import get_variable

# 缓存配置，避免重复读取文件
_CONFIG_CACHE: Optional[Dict[str, Any]] = None


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
    
    # 获取host配置（使用缓存）
    config = get_config()
    host_config: List[Dict[str, str]] = config.get("Host", [])

    # 构建替换映射
    replacements = {}
    for var_name in keys:
        # 优先从host配置获取
        replacement_found = False
        for host_item in host_config:
            if var_name in host_item:
                replacements[f"${{{var_name}}}"] = str(host_item[var_name])
                replacement_found = True
                break
        
        # 如果host配置中没找到，从variable_cache获取
        if not replacement_found:
            cache_value = get_variable(var_name)
            if cache_value is not None:
                replacements[f"${{{var_name}}}"] = str(cache_value)
    
    # 执行替换
    result_url = url
    for placeholder, value in replacements.items():
        result_url = result_url.replace(placeholder, str(value))
        
    return result_url


def replace_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    替换data中的变量，返回修改后的副本
    
    Args:
        data (Dict[str, Any]): 需要替换数据的字典
        
    Returns:
        Dict[str, Any]: 替换后的字典副本
    """
    if not isinstance(data, dict):
        return {}
    
    # 深拷贝数据避免修改原字典
    import copy
    result = copy.deepcopy(data)
    
    # 使用栈来保存待处理的字典及其键值对
    stack: List[Tuple[Dict[str, Any], str]] = []
    
    # 初始化栈
    for key in result:
        stack.append((result, key))
    
    while stack:
        current_dict, key = stack.pop()
        value = current_dict[key]
        
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            var_name = value[2:-1]  # 提取变量名
            try:
                replacement = get_variable(var_name)
                if replacement is not None:
                    current_dict[key] = replacement
            except Exception as e:
                print(f"Warning: Failed to replace variable '{var_name}': {e}")
        elif isinstance(value, dict):
            # 将子字典的键值对加入栈中
            for sub_key in value:
                stack.append((value, sub_key))
    
    return result

def get_config() -> Dict[str, Any]:
    """获取配置数据，使用缓存提高性能"""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        try:
            config_path = config_yaml_path()
            _CONFIG_CACHE = read_config()
        except Exception:
            _CONFIG_CACHE = {}
    return _CONFIG_CACHE

def config_yaml_path() -> str:
    """获取配置文件路径"""
    return str(pathlib.Path(__file__).parent.parent / "config" / "base_config.yaml")

def clear_config_cache() -> None:
    """清除配置缓存，用于测试或配置更新后"""
    global _CONFIG_CACHE
    _CONFIG_CACHE = None

if __name__ == "__main__":
    from utils.constant import set_variable
    # 测试配置路径读取
    set_variable("user_id",1)
    set_variable("username", "123")
    set_variable("nested_var", "123")
    set_variable("conunt_var", 15)
    config_path = config_yaml_path()
    print(f"Config path: {config_path}")
    
    # 测试配置读取
    config = get_config()
    print(f"Host config: {config.get('Host', [])}")
    
    # 测试URL替换
    test_url = "http://${host1}/api/${user_id}"
    result = replace_url(test_url)
    print(f"URL replacement test: {test_url} -> {result}")
    
    # 测试数据替换
    test_data = {
        "user": "${username}",
        "nested": {
            "value": "${nested_var}",
            "conunt": "${conunt_var}"
        }
    }
    result_data = replace_data(test_data)
    print(f"原始数据: {test_data}")
    print(f"替换后数据: {result_data}")
    print("检查变量替换:")
    print(f"  ${{username}} -> {result_data['user']}")
    print(f"  ${{nested_var}} -> {result_data['nested']['value']}")
