
# read yaml file
import yaml
from typing import Any, Dict, List, Optional


def read_yaml(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Read YAML file content
    
    Args:
        file_path (str): Path to the YAML file
        
    Returns:
        Optional[Dict[str, Any]]: Parsed YAML content, or None if file not found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data
    except FileNotFoundError:
        return None
    except yaml.YAMLError:
        return None
    except Exception:
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
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, indent=2)
        return True
    except IOError:
        return False
    except yaml.YAMLError:

        return False
    except Exception:
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
