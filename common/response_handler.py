from typing import  ByteString, Dict
from xml.etree import ElementTree as ETree
from requests import Response, JSONDecodeError


def __parse_json(response: Response) -> Dict | None:
    """
    解析响应的JSON数据并返回解析结果。
    如果解析失败，则返回None。
    """
    try:
        return response.json()
    except (ValueError, JSONDecodeError):
        return None



def __parse_xml(response: Response) -> ETree.Element | None:
    """
    解析响应的XML数据并返回解析结果。
    如果解析失败，则返回None。
    """
    try:
        return ETree.fromstring(response.text)
    except ETree.ParseError:
        return None



def response_handler(response: Response) -> Dict | ETree.Element | str | ByteString | int| None:
    """
    根据响应的内容类型处理响应数据并返回处理结果。
    可能的返回值类型为JSON字典、XML元素、纯文本字符串或原始字节流。

    Args:
    - response: requests.Response对象，表示HTTP响应。

    Returns5
    - Union[Dict, ET.Element, str, bytes]: 处理后的响应数据，类型可能是字典、XML元素、字符串或字节流。
    """

    content_type_header = response.headers.get("content-type", "")
    if not content_type_header:
        return response.status_code

    content_type = content_type_header.split(";")[0].strip().lower()

    match content_type:
        case "application/json":
            return __parse_json(response)
        case "application/xml" | "text/xml":
            return __parse_xml(response)
        case "text/html" | "text/plain":
            return response.text
        case "application/octet-stream":
            return response.content
        case _:
            return response.status_code