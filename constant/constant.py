"""
变量缓存模块
提供全局变量存储和检索功能
"""

from typing import Any, Dict, Optional


class VariableCache:
    """简单的全局变量缓存类"""

    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def set_value(self, key: str, value: Any) -> None:
        """设置变量值"""
        self._cache[key] = value

    def get_value(self, key: str, default: Any = None) -> Optional[Any]:
        """获取变量值，如果不存在则返回默认值"""
        return self._cache.get(key, default)

    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()

    def remove(self, key: str) -> bool:
        """删除指定变量"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def get_all(self) -> Dict[str, Any]:
        """获取所有变量"""
        return self._cache.copy()


# 创建全局实例
variable_cache = VariableCache()


# 提供便捷的全局函数
def set_variable(key: str, value: Any) -> None:
    """设置全局变量"""
    variable_cache.set_value(key, value)


def get_variable(key: str, default: Any = None) -> Optional[Any]:
    """获取全局变量"""
    return variable_cache.get_value(key, default)


def clear_variables() -> None:
    """清空所有全局变量"""
    variable_cache.clear()


def remove_variable(key: str) -> bool:
    """删除指定全局变量"""
    return variable_cache.remove(key)