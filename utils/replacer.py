import re
from typing import Dict, Any, List, Tuple
from utils import config_reader, constant, logger


def replace_url(url: str) -> str:
    """
    替换url中的变量

    Args:
        url (str): 需要替换变量的URL字符串

    Returns:
        str: 替换后的URL字符串
    """
    logger.debug(f"开始替换URL变量，原始URL: {url}")

    if not url:
        logger.warning("URL为空，跳过替换")
        return url

    # 查找所有形如 ${variable_name} 的变量
    keys = re.findall(r"\$\{([a-zA-Z0-9_]+)\}", url)
    if not keys:
        logger.debug("URL中未找到需要替换的变量")
        return url

    logger.info(f"在URL中找到 {len(keys)} 个需要替换的变量: {keys}")

    # 获取host配置
    config: Dict[str, Any] = config_reader.get_config()
    host_config: List[Dict[str, Any]] = config.get("Host", [])

    # 构建替换映射
    replacements = {}
    for var_name in keys:
        # 优先从host配置获取
        replacement_found = False
        for host_item in host_config:
            if host_item.get("name") == var_name:
                replacements[f"${{{var_name}}}"] = str(host_item.get("url", ""))
                replacement_found = True
                logger.debug(
                    f"从host配置中找到变量 '{var_name}' 的值: {host_item.get('url', '')}"
                )
                break

        # 如果host配置中没找到，从variable_cache获取
        if not replacement_found:
            cache_value = constant.get_variable(var_name)
            if cache_value is not None:
                replacements[f"${{{var_name}}}"] = str(cache_value)
                logger.debug(f"从变量缓存中找到变量 '{var_name}' 的值: {cache_value}")
            else:
                logger.warning(f"未找到变量 '{var_name}' 的值，跳过替换")

    # 执行替换
    result_url = url
    for placeholder, value in replacements.items():
        result_url = result_url.replace(placeholder, str(value))

    logger.info(f"URL变量替换完成，结果: {result_url}")
    return result_url


def replace_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    替换data中的变量，返回修改后的副本

    Args:
        data (Dict[str, Any]): 需要替换数据的字典

    Returns:
        Dict[str, Any]: 替换后的字典副本
    """
    logger.debug(f"开始替换数据中的变量，原始数据: {data}")

    if not isinstance(data, dict):
        logger.warning(f"输入数据不是字典类型，类型为: {type(data)}")
        return {}

    # 深拷贝数据避免修改原字典
    import copy

    result = copy.deepcopy(data)

    # 使用栈来保存待处理的字典及其键值对
    stack: List[Tuple[Dict[str, Any], str]] = []

    # 初始化栈
    for key in result:
        stack.append((result, key))

    replaced_count = 0
    while stack:
        current_dict, key = stack.pop()
        value = current_dict[key]

        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            var_name = value[2:-1]  # 提取变量名
            try:
                replacement = constant.get_variable(var_name)
                if replacement is not None:
                    current_dict[key] = replacement
                    replaced_count += 1
                    logger.debug(f"成功替换变量 '{var_name}' 的值为: {replacement}")
                else:
                    logger.warning(f"未找到变量 '{var_name}' 的值，跳过替换")
            except Exception as e:
                logger.error(f"替换变量 '{var_name}' 时发生异常: {e}")
        elif isinstance(value, dict):
            # 将子字典的键值对加入栈中
            for sub_key in value:
                stack.append((value, sub_key))

    logger.info(f"数据变量替换完成，共替换了 {replaced_count} 个变量")
    logger.info(f"数据变量替换结果: {result}")
    return result


if __name__ == "__main__":
    from utils import constant

    # 测试配置路径读取
    constant.set_variable("user_id", 1)
    constant.set_variable("username", "123")
    constant.set_variable("nested_var", "123")
    constant.set_variable("conunt_var", 15)

    # 测试配置读取
    config_reader1 = config_reader.get_config()
    print(f"Host config: {config_reader1.get('Host', [])}")

    # 测试URL替换
    test_url = "http://${host1}/api/${user_id}"
    result = replace_url(test_url)
    print(f"URL replacement test: {test_url} -> {result}")

    # 测试数据替换
    test_data = {
        "user": "${username}",
        "nested": {"value": "${nested_var}", "conunt": "${conunt_var}"},
    }
    result_data = replace_data(test_data)
    print(f"原始数据: {test_data}")
    print(f"替换后数据: {result_data}")
    print("检查变量替换:")
    print(f"  ${{username}} -> {result_data['user']}")
    print(f"  ${{nested_var}} -> {result_data['nested']['value']}")
