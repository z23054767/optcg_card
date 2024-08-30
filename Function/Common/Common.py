import os
import sys
import re

class CommonHandle:
    """
        通用方法類別
    """
    
    def get_script_directory(self, script_directory: str) -> str:
        """
        獲取腳本目錄的路徑，考慮到打包後的情況

        Args:
        script_directory (str): 當前腳本文件的路徑

        Returns:
        str: 調整後的腳本目錄路徑
        """
        if getattr(sys, 'frozen', False):
            # 如果是被打包的可執行文件，使用 sys.executable
            return os.path.dirname(sys.executable)
        else:
            # 否則使用原始的腳本目錄
            return os.path.dirname(os.path.abspath(script_directory))
        
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
        
    def get_user_choice_language_url(self) -> str:
        """
        提示用戶選擇網站語言版本並返回對應的 URL。

        該方法將提示用戶輸入 'Y' 或 'N' 來選擇日文版網頁URL或繁體中文版網頁URL。
        - 'Y' 代表選擇日文版網站，將返回對應的日文版 URL。
        - 'N' 代表選擇繁體中文版網站，將返回對應的繁體中文版 URL。

        如果用戶輸入無效（非 'Y' 或 'N'），將繼續提示用戶直到輸入有效。

        Returns:
            str: 返回用戶選擇的語言對應的網址。
        """
        while True:
            choice = input("是否選擇日文版網站？(Y/N)：").strip().upper()
            if choice in ['Y', 'N']:
                break
            else:
                print("無效輸入，請輸入 'Y' 或 'N'。")

        url = 'https://www.onepiece-cardgame.com' if choice == 'Y' else 'https://asia-tw.onepiece-cardgame.com'
        return url