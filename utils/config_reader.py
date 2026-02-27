import pathlib
from typing import Any, Dict, List, Optional
import yaml
from utils.logger import logger


# 配置文件路径
CONFIG_FILE_PATH = pathlib.Path(__file__).parent.parent / "config/base_config.yaml"
# 缓存配置，避免重复读取文件
_CONFIG_CACHE: Optional[Dict[str, Any]] = None


def read_config() -> dict:
    """读取配置文件"""
    logger.info(f"开始读取配置文件: {CONFIG_FILE_PATH}")
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    if config:
        logger.info(f"配置文件读取成功，包含 {len(config)} 个顶级配置项")
    else:
        logger.warning("配置文件为空或格式不正确")
    return config or {}


def get_host_headers(host_name: str) -> Dict[str, str]:
    """
    获取指定host的header配置

    Args:
        host_name: host名称

    Returns:
        dict: host对应的header配置
    """
    logger.info(f"开始获取host配置: {host_name}")
    config = get_config()
    host_config: List[Dict[str, Any]] = config.get("Host", [])

    # 查找指定host的配置
    for host_item in host_config:
        if host_item.get("name") == host_name:
            headers = host_item.get("headers", {})
            logger.info(f"成功获取host '{host_name}' 的headers配置，包含 {len(headers)} 个header项")
            return headers

    logger.warning(f"未找到host '{host_name}' 的配置，返回空headers")
    return {}


def get_global_headers() -> Dict[str, str]:
    """
    获取全局通用header配置

    Returns:
        dict: 全局通用header配置
    """
    logger.info("开始获取全局headers配置")
    config = get_config()
    global_headers = config.get("GlobalHeaders", {})
    logger.info(f"成功获取全局headers配置，包含 {len(global_headers)} 个header项")
    return global_headers


def get_config() -> Dict[str, Any]:
    """获取配置数据，使用缓存提高性能"""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        logger.debug("配置缓存为空，开始读取配置文件")
        try:
            _CONFIG_CACHE = read_config()
            logger.debug("配置文件读取成功，已缓存")
        except Exception as e:
            logger.error(f"读取配置文件失败: {e}")
            _CONFIG_CACHE = {}
    else:
        logger.debug("使用缓存的配置数据")
    return _CONFIG_CACHE


def clear_config_cache() -> None:
    """清除配置缓存，用于测试或配置更新后"""
    global _CONFIG_CACHE
    logger.info("清除配置缓存")
    _CONFIG_CACHE = None
