from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Union

# 项目根目录（使用相对路径）
# 获取当前文件的父目录的父目录作为项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


def path_util(
    start_path: Optional[Union[str, Path]] = None,
    extensions: Optional[List[str]] = None,
) -> Dict[str, List[str]]:
    """
    获取测试用例数据文件地址

    Args:
        start_path: 起始目录或文件路径，默认为None（使用默认的test_data目录）
        extensions: 允许的文件扩展名列表，如 ['.py', '.txt']，为None时包含所有文件

    Returns:
        字典，键为测试用例文件的父级目录名，值为地址的列表

    Raises:
        ValueError: 如果起始路径不存在
    """
    # 处理默认路径情况
    if start_path is None:
        search_path = PROJECT_ROOT / "test_data"
    else:
        start_path = Path(start_path)

        if not start_path.exists():
            raise ValueError(f"路径不存在: {start_path}")

        # 如果是文件，直接返回该文件
        if start_path.is_file():
            file_dict: Dict[str, List[str]] = defaultdict(list)
            _process_file(start_path, file_dict, extensions)
            return dict(file_dict)

        # 如果是目录，使用该目录作为搜索路径
        search_path = start_path

    # 预处理扩展名列表，统一转为小写
    normalized_extensions = None
    if extensions is not None:
        normalized_extensions = {ext.lower() for ext in extensions}

    file_dict: Dict[str, List[str]] = defaultdict(list)
    _process_directory(search_path, file_dict, normalized_extensions)

    return dict(file_dict)


def _process_file(
    file_path: Path, file_dict: Dict[str, List[str]], extensions: Optional[List[str]]
) -> None:
    """处理单个文件，将其添加到对应目录"""
    if extensions is None or file_path.suffix.lower() in extensions:
        # 使用父级目录名作为键，而不是完整路径
        dir_name = file_path.parent.name
        file_dict[dir_name].append(str(file_path))


def _process_directory(
    search_path: Path, file_dict: Dict[str, List[str]], extensions: Optional[set]
) -> None:
    """递归处理目录及其子目录"""
    try:
        # 使用rglob递归遍历所有文件和子目录
        for file_path in search_path.rglob("*"):
            if file_path.is_file():
                _process_file(file_path, file_dict, extensions)
    except (PermissionError, OSError) as e:
        print(f"警告: 访问文件时发生错误: {e}")


if __name__ == "__main__":
    # 测试默认情况
    print("默认情况（test_data目录）:")
    files_by_dir = path_util()
    print(files_by_dir)

    # 测试传入文件路径情况
    print("\n传入文件路径情况:")
    test_file = PROJECT_ROOT / "test_data" / "a.yaml"
    files_by_dir = path_util(test_file)
    print(files_by_dir)

    # 测试传入目录路径情况
    print("\n传入目录路径情况:")
    test_dir = PROJECT_ROOT / "test_data"
    files_by_dir = path_util(test_dir)
    print(files_by_dir)
