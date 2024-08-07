import re

class CommonHandle:
    """
        通用方法類別
    """
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