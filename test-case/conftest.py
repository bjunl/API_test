import pytest
from typing import List, Dict, Any
from fixture import data_fixture
from utils import excel_util, file_type_util
# def get_data():
#     excel_paths = path_fixture.get_excel_path()
#     data_list = []
#     for excel_path in excel_paths:
#         data = excel_util.read_excel(excel_path)
#         data_list += data
#     return data_list
#
#
# @pytest.fixture(autouse=True, params=get_data())  # autouse=True means that this fixture will be used for all tests
# def get_case_data(request):
#     data = request.param
#     data_fixture.data_processing(data)
#     data["url"] = replace_fixture.replace_url(data["url"])
#     replace_fixture.replace_data(data)
#     print("data: ", data)
#     yield data  # yield is used to return data to the test function



@pytest.fixture(autouse=True)
def get_excel_path():
    return path_fixture.get_excel_path()

@pytest.fixture(autouse=True)
def get_case_data(excel_path: str) -> List[Dict[str, Any]]:
    data: List[Dict[str, Any]] = excel_util.read_excel(excel_path)
    for i in data:
        data_fixture.data_processing(i) 
        i["url"] = replace_fixture.replace_url(i["url"])
        replace_fixture.replace_data(i)
        print("data: ", i)
    return data