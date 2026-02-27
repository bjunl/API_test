import yaml
from typing import Any, Optional
from utils.logger import logger


def yaml_reader(file_path: str) -> Optional[list[dict[str, Any]]]:
    """
    Read YAML file content and return it as a dictionary.
    
    Args:
        file_path (str): Path to the YAML file
        
    Returns:
        Optional[Dict[str, Any]]: Parsed YAML content, or None if file not found
    """
    logger.debug(f"开始读取YAML文件: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            logger.info(f"成功读取YAML文件: {file_path}")
            return data
    except FileNotFoundError:
        logger.error(f"YAML文件不存在: {file_path}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"YAML文件格式错误: {file_path}, 错误: {e}")
        return None
    except Exception as e:
        logger.error(f"读取YAML文件时发生未知错误: {file_path}, 错误: {e}")
        return None



def write_yaml(file_path: str, data: Any) -> bool:
    """
    Write data to YAML file
    
    Args:
        file_path (str): Path to the YAML file
        data (Any): Data to write to the file
        
    Returns:
        bool: True if write successful, False otherwise
    """
    logger.debug(f"开始写入YAML文件: {file_path}")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, indent=2)
        logger.info(f"成功写入YAML文件: {file_path}")
        return True
    except IOError as e:
        logger.error(f"写入YAML文件失败（IO错误）: {file_path}, 错误: {e}")
        return False
    except yaml.YAMLError as e:
        logger.error(f"写入YAML文件失败（YAML错误）: {file_path}, 错误: {e}")
        return False
    except Exception as e:
        logger.error(f"写入YAML文件时发生未知错误: {file_path}, 错误: {e}")
        return False



if __name__ == '__main__':
    # Create a sample config for testing
    sample_data = {
        "host": "localhost",
        "port": 8080,
        "database": {
            "host": "db.example.com",
            "name": "test_db"
        }
    }

    # Test write and read functionality
    test_file = "test_config.yaml"
    if write_yaml(test_file, sample_data):
        print(f"Successfully wrote test config to {test_file}")
        loaded_data = read_yaml(test_file)
        if loaded_data:
            print("Successfully loaded data:")
            print(f"Host: {loaded_data.get('host')}")
            print(f"Port: {loaded_data.get('port')}")
        else:
            print("Failed to read the test file")
    else:
        print("Failed to write test file")