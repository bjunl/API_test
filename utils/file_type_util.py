from pathlib import Path


class FileTypeUtil:
    """文件类型判断辅助类"""
    
    @staticmethod
    def get_file_helper(file_path: str):
        """根据文件后缀返回对应的处理类名
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 对应的处理类名
            
        Raises:
            ValueError: 当文件类型不支持时
        """
        suffix = Path(file_path).suffix.lower()
        
        if suffix in ['.xlsx', '.xls']:
            return 'Excel'
        elif suffix == '.json':
            return 'Json'
        elif suffix in ['.yaml', '.yml']:
            return 'Yaml'
        else:
            raise ValueError(f"不支持的文件类型: {suffix}")