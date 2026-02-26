import pytest
from typing import List, Dict, Any
from data import data_processor
from utils import replacer
from utils import  file, path


@pytest.fixture(autouse=True)
def get_test_data_path() -> list[str]:
    path_list:List[str]=[]
    data_path = path.path_util()
    for k,v in data_path.items():
        for i in v:
            path_list.append(i)
        
    return path_list

@pytest.fixture(autouse=True)
def get_case_data(file_path: str) -> List[Dict[str, Any]]:
    data = file.FileTypeUtil.get_file_helper(file_path)
    if not data:
        raise ValueError(f"无法读取文件: {file_path}")
    for i in data:
        data_processor.data_processing(i) 
        i["url"] = replacer.replace_url(i["url"])
        replacer.replace_data(i)
        print("data: ", i)
    return data