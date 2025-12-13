from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Union


def path_util(
    start_path: Union[str, Path] = ".",
    extensions: Optional[List[str]] = None
) -> Dict[str, List[str]]:
    """
    按目录分组文件，可以过滤文件类型

    Args:
        start_path: 起始目录或文件路径，默认为当前目录
        extensions: 允许的文件扩展名列表，如 ['.py', '.txt']，为None时包含所有文件

    Returns:
        字典，键为目录路径，值为该目录下的文件路径列表
        
    Raises:
        ValueError: 如果起始路径不存在
    """
    start_path = Path(start_path)
    
    if not start_path.exists():
        raise ValueError(f"路径不存在: {start_path}")
    
    # 预处理扩展名列表，统一转为小写
    normalized_extensions = None
    if extensions is not None:
        normalized_extensions = {ext.lower() for ext in extensions}
    
    file_dict: Dict[str, List[str]] = defaultdict(list)
    
    # 如果是文件，直接处理该文件
    if start_path.is_file():
        _process_file(start_path, file_dict, normalized_extensions)
        return dict(file_dict)
    
    # 根据是否默认路径选择不同的遍历策略
    search_path = _get_search_path(start_path)
    _process_directory(search_path, file_dict, normalized_extensions)
    
    return dict(file_dict)


def _process_file(file_path: Path, file_dict: Dict[str, List[str]], extensions: Optional[set]) -> None:
    """处理单个文件，将其添加到对应目录"""
    if extensions is None or file_path.suffix.lower() in extensions:
        dir_path = str(file_path.parent)
        file_dict[dir_path].append(str(file_path))


def _get_search_path(start_path: Path) -> Path:
    """根据start_path返回搜索路径"""
    # 默认情况下处理test-data目录
    if str(start_path) == ".":
        return start_path / "test-data"
    return start_path


def _process_directory(search_path: Path, file_dict: Dict[str, List[str]], extensions: Optional[set]) -> None:
    """递归处理目录及其子目录"""
    try:
        # 使用rglob递归遍历所有文件和子目录
        for file_path in search_path.rglob("*"):
            if file_path.is_file():
                _process_file(file_path, file_dict, extensions)
    except (PermissionError, OSError) as e:
        print(f"警告: 访问文件时发生错误: {e}")


if __name__ == "__main__":
    files_by_dir = path_util()
    print(files_by_dir)
