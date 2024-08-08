import os
import sys
import re

class CommonHandle:
    """
        通用方法類別
    """
    
    def get_script_directory(self) -> str:
        """
        獲取腳本目錄的路徑，考慮到打包後的情況
        """
        if getattr(sys, 'frozen', False):
            # 如果是被打包的可執行文件，使用 sys._MEIPASS
            return os.path.dirname(sys.executable)
        else:
            # 否則使用原始的腳本目錄
            return os.path.dirname(os.path.abspath(__file__))
        
    def process_series_name(self, series_name: str) -> str:
        """
        根據給定的 series_name 提取 `【】` 內的文字，若無 `【】`，則返回處理過的 option_text
        
        Args:
            series_name (str): 卡片系列原始名稱
        """
        match = re.search(r'【(.*?)】', series_name)
        if match:
            return match.group(1)
        else:
            return series_name.split('<br')[0].strip()