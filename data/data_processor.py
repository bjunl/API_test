from pathlib import Path
from typing import BinaryIO, Dict
from requests_toolbelt.multipart.encoder import MultipartEncoder
from utils.logger import logger


def data_processing(excel_dict: Dict) -> Dict[str, str | MultipartEncoder | Dict]:
    """处理Excel数据, 返回一个字典

    Args:
        excel_dict (Dict): Excel中读取的字典数据

    Returns:
        Dict[str, str | MultipartEncoder | Dict]: 将Excel中file类型数据转换为二进制流数据，将form类型数据转换为form表单,
        并添加到字典中
    """
    logger.debug(f"开始处理Excel数据，数据类型: {excel_dict.get('data_type')}")
    
    data_type: str = excel_dict["data_type"]

    if data_type == "file":
        logger.info("处理file类型数据")
        file_dict: dict[str, tuple[str, BinaryIO]] = {}
        for k, v in excel_dict["data"].items():
            file_name = Path(v).name
            file_dict.update({k: (file_name, open(v, 'rb'))})
            logger.debug(f"添加文件: {k} -> {v} (文件名: {file_name})")
        excel_dict["files"] = file_dict
        excel_dict.pop("data")
        logger.info(f"file类型数据处理完成，共处理 {len(file_dict)} 个文件")

    elif data_type == "form":
        logger.info("处理form类型数据")
        mp_encoder = MultipartEncoder(fields=excel_dict["data"])
        excel_dict["headers"].update({"content_type": mp_encoder.content_type})
        excel_dict["data"] = mp_encoder
        logger.debug(f"form类型数据处理完成，Content-Type: {mp_encoder.content_type}")

    elif data_type == "json":
        logger.info("处理json类型数据")
        value = excel_dict["data"]
        excel_dict['json'] = value
        excel_dict.pop("data")
        logger.debug("json类型数据处理完成")

    else:
        logger.warning(f"未知的数据类型: {data_type}")
    
    return excel_dict