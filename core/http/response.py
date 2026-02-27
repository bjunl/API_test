from typing import Dict
from xml.etree import ElementTree as ETree
from requests import Response, JSONDecodeError
from utils.logger import logger


def __parse_json(response: Response) -> Dict | None:
    """
    解析响应的JSON数据并返回解析结果
    如果解析失败，则返回None。
    """
    logger.debug("开始解析JSON响应")
    try:
        json_data = response.json()
        logger.info("JSON响应解析成功")
        return json_data
    except (ValueError, JSONDecodeError) as e:
        logger.error(f"JSON响应解析失败: {e}")
        return None



def __parse_xml(response: Response) -> ETree.Element | None:
    """
    解析响应的XML数据并返回解析结果。
    如果解析失败，则返回None。
    """
    logger.debug("开始解析XML响应")
    try:
        xml_element = ETree.fromstring(response.text)
        logger.info("XML响应解析成功")
        return xml_element
    except ETree.ParseError as e:
        logger.error(f"XML响应解析失败: {e}")
        return None



def response_handler(response: Response) -> Dict | ETree.Element | str | bytes | int | None:
    """
    根据响应的内容类型处理响应数据并返回处理结果。
    可能的返回值类型为JSON字典、XML元素、纯文本字符串或原始字节流。

    Args:
    - response: requests.Response对象，表示HTTP响应。

    Returns:
    - Union[Dict, ET.Element, str, bytes]: 处理后的响应数据，类型可能是字典、XML元素、字符串或字节流。
    """
    logger.debug(f"开始处理响应，状态码: {response.status_code}")
    
    content_type_header = response.headers.get("content-type", "")
    if not content_type_header:
        logger.warning("响应头中未找到Content-Type，返回状态码")
        return response.status_code

    content_type = content_type_header.split(";")[0].strip().lower()
    logger.debug(f"响应Content-Type: {content_type}")

    match content_type:
        case "application/json":
            result = __parse_json(response)
            if result is None:
                logger.warning("JSON解析失败，返回None")
            return result
        case "application/xml" | "text/xml":
            result = __parse_xml(response)
            if result is None:
                logger.warning("XML解析失败，返回None")
            return result
        case "text/html" | "text/plain":
            logger.debug("响应为文本类型，返回文本内容")
            return response.text
        case "application/octet-stream":
            logger.debug("响应为二进制流，返回字节流")
            return response.content
        case _:
            logger.warning(f"未知的Content-Type: {content_type}，返回状态码")
            return response.status_code