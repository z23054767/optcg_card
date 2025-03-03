import os
import shutil

import requests

from functions.common.common import Common
from functions.database.database import Database


class Download:
    """
    圖片下載類別
    """

    def __init__(self, script_directory: str):
        """
        圖片下載類別 建構子

        Args:
        script_directory (str): 腳本目錄的路徑
        """
        self._script_directory: str = script_directory
        """ 腳本目錄的路徑 """
        self._database: Database = Database(script_directory)
        """ DB存取類別 """

    @Common.exception_handler
    def check_image_folder(self):
        """
        檢查是否存在 'Image' 資料夾，若存在則刪除後重新建立
        """
        image_dir = os.path.join(self._script_directory, "Image")

        if os.path.exists(image_dir):
            shutil.rmtree(image_dir)
            print(f"已刪除資料夾: {image_dir}")

        os.makedirs(image_dir, exist_ok=True)
        print(f"已建立資料夾: {image_dir}")

    @Common.exception_handler
    def download_image(self, cid: int, img_url: str, series_name: str):
        """
        下載檔案到指定目錄下

        Args:
            cid (int): 圖片所屬卡片的cid (識別碼)
            img_url (str) : 圖片網址
            series_name (str): 系列名稱
        """
        # 如果目錄不存在，創建目錄
        dir_path = os.path.join(self._script_directory, "Image", series_name)
        os.makedirs(dir_path, exist_ok=True)

        # 從URL中提取檔名
        file_name = os.path.basename(img_url)

        # 圖片將被保存的完整路徑
        file_path = os.path.join(dir_path, file_name)

        # 下載圖片並保存到指定路徑
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()  # 檢查請求是否成功

        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"圖片已保存到 {file_path}")
        # 將檔案資訊儲存到資料庫
        self._database.save_file_info(cid, file_path)
