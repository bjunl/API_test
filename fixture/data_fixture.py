from pathlib import Path
from typing import BinaryIO, Dict

from requests_toolbelt.multipart.encoder import MultipartEncoder


def data_processing(excel_dict: Dict) -> Dict[str, str | MultipartEncoder | Dict]:
    """处理Excel数据, 返回一个字典

    Args:
        excel_dict (Dict): Excel中读取的字典数据

    Returns:
        Dict[str, str | MultipartEncoder | Dict]: 将Excel中file类型数据转换为二进制流数据，将form类型数据转换为form表单,
        并添加到字典中
    """
    data_type: str = excel_dict["data_type"]

    if data_type == "file":
        file_dict: dict[str, tuple[str, BinaryIO]] = {}
        for k, v in excel_dict["data"].items():
            file_name = Path(v).name
            file_dict.update({k: (file_name, open(v, 'rb'))})
        excel_dict["files"] = file_dict
        excel_dict.pop("data")

    elif data_type == "form":
        mp_encoder = MultipartEncoder(fields=excel_dict["data"])
        excel_dict["headers"].update({"content_type": mp_encoder.content_type})
        excel_dict["data"] = mp_encoder

    elif data_type == "json":
        value = excel_dict["data"]
        excel_dict['json'] = value
        excel_dict.pop("data")

    return excel_dict