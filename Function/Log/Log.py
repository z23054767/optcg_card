import os
from datetime import datetime

class Logger:   
    """
        錯誤紀錄類別
    """

    def __init__(self, script_directory : str):
        """
            錯誤紀錄類別 建構子

            Args:
            script_directory (str): 腳本目錄的路徑
        """
        self._script_directory : str = script_directory
        """ 腳本目錄的路徑 """

    def log_error_message(self, message : str) -> None:
        """
            寫入錯誤訊息至指定路徑
            
            Args:
            message (str): 錯誤訊息
        """

        # 創建LOG文件夾（如果不存在）
        log_folder = os.path.join(self._script_directory, 'log')
        os.makedirs(log_folder, exist_ok = True)
        # 獲取當前日期
        current_date = datetime.now().strftime('%Y%m%d')
        # 設置日誌文件名
        log_file = os.path.join(log_folder, f'{current_date}.txt')
        current_time = datetime.now().strftime('%H:%M:%S')
        log_message = f'[{current_time}] : {message}\n'
        with open(log_file, 'a') as log:
            log.write(log_message)