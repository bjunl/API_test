from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Union
from utils.logger import logger

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
    logger.info("开始获取测试数据文件路径")
    
    # 处理默认路径情况
    if start_path is None:
        search_path = PROJECT_ROOT / "test_data"
        logger.debug(f"使用默认路径: {search_path}")
    else:
        start_path = Path(start_path)

        if not start_path.exists():
            error_msg = f"路径不存在: {start_path}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # 如果是文件，直接返回该文件
        if start_path.is_file():
            logger.debug(f"传入的是文件路径: {start_path}")
            file_dict: Dict[str, List[str]] = defaultdict(list)
            _process_file(start_path, file_dict, extensions)
            result = dict(file_dict)
            logger.info(f"找到 {len(result)} 个目录，共 {sum(len(v) for v in result.values())} 个文件")
            return result

        # 如果是目录，使用该目录作为搜索路径
        search_path = start_path
        logger.debug(f"传入的是目录路径: {search_path}")

    # 预处理扩展名列表，统一转为小写
    normalized_extensions = None
    if extensions is not None:
        normalized_extensions = {ext.lower() for ext in extensions}
        logger.debug(f"过滤文件扩展名: {extensions}")

    file_dict: Dict[str, List[str]] = defaultdict(list)
    _process_directory(search_path, file_dict, normalized_extensions)
    
    result = dict(file_dict)
    total_files = sum(len(v) for v in result.values())
    logger.info(f"扫描完成，找到 {len(result)} 个目录，共 {total_files} 个文件")
    
    return result


def _process_file(
    file_path: Path, file_dict: Dict[str, List[str]], extensions: Optional[List[str]]
) -> None:
    """处理单个文件，将其添加到对应目录"""
    if extensions is None or file_path.suffix.lower() in extensions:
        # 使用父级目录名作为键，而不是完整路径
        dir_name = file_path.parent.name
        file_dict[dir_name].append(str(file_path))
        logger.debug(f"添加文件: {file_path} (目录: {dir_name})")


def _process_directory(
    search_path: Path, file_dict: Dict[str, List[str]], extensions: Optional[set]
) -> None:
    """递归处理目录及其子目录"""
    logger.debug(f"开始扫描目录: {search_path}")
    try:
        # 使用rglob递归遍历所有文件和子目录
        for file_path in search_path.rglob("*"):
            if file_path.is_file():
                _process_file(file_path, file_dict, extensions)
    except (PermissionError, OSError) as e:
        logger.error(f"访问文件时发生错误: {e}")


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
