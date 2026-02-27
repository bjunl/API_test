import pathlib
from typing import Any, Dict, List, Optional
import yaml


# 配置文件路径
CONFIG_FILE_PATH = pathlib.Path(__file__).parent.parent / "config/base_config.yaml"
# 缓存配置，避免重复读取文件
_CONFIG_CACHE: Optional[Dict[str, Any]] = None


def read_config() -> dict:
    """读取配置文件"""
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
        return config or {}


def get_host_headers(host_name: str) -> Dict[str, str]:
    """
    获取指定host的header配置

    Args:
        host_name: host名称

    Returns:
        dict: host对应的header配置
    """
    config = get_config()
    host_config: List[Dict[str, Any]] = config.get("Host", [])

    # 查找指定host的配置
    for host_item in host_config:
        if host_item.get("name") == host_name:
            return host_item.get("headers", {})

    return {}


def get_global_headers() -> Dict[str, str]:
    """
    获取全局通用header配置

    Returns:
        dict: 全局通用header配置
    """
    config = get_config()
    return config.get("GlobalHeaders", {})


def get_config() -> Dict[str, Any]:
    """获取配置数据，使用缓存提高性能"""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        try:
            _CONFIG_CACHE = read_config()
        except Exception:
            _CONFIG_CACHE = {}
    return _CONFIG_CACHE


def clear_config_cache() -> None:
    """清除配置缓存，用于测试或配置更新后"""
    global _CONFIG_CACHE
    _CONFIG_CACHE = None
