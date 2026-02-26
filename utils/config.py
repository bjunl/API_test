import pathlib
import yaml


# 配置文件路径
CONFIG_FILE_PATH = pathlib.Path(__file__).parent.parent / "config/base_config.yaml"

def read_config() -> dict:
    """读取配置文件"""
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        return config or {}
