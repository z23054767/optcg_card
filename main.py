import sqlite3

import requests
from selenium.common.exceptions import WebDriverException

from functions.common.common import Common
from functions.crawler.crawler import Crawler
from functions.database.database import Database
from functions.download.image_download import Download
from functions.log.log import Log

# 初始化設定
_common: Common = Common()
_script_directory: str = _common.get_script_directory(__file__)
_database: Database = Database(_script_directory)
_database.check_db_folder()
_download: Download = Download(_script_directory)
_download.check_image_folder()

# 初始化類別
_crawler: Crawler = Crawler(_script_directory)
_log: Log = Log(_script_directory)


if __name__ == "__main__":
    try:
        # 選擇網站語言(Y:日文 N:中文)
        LANGUAGE_URL = _common.get_user_choice_language_url()
        # 將所有的卡片資料存入資料庫
        _crawler.handle_all_card_list(LANGUAGE_URL)
        print("儲存卡片資料至資料庫完畢....")
        # 資料庫正規化
        _database.normalize_database()
        print("資料庫正規化完畢")
        # 逐一讀取卡片資料
        all_cards_info = _database.fetch_card_info_with_series_id()
        print("取出儲存資料")
        # 逐一取出 series_id 並處理
        for card_info in all_cards_info:
            _download.download_image(
                card_info["cid"], card_info["img_src"], card_info["series_name"]
            )
        print("下載全系列卡圖完畢....")
    except sqlite3.DatabaseError as err:
        _log.log_error_message(f"Database error: {err}")
        print(f"Database error: {err}")
    except requests.RequestException as err:
        _log.log_error_message(f"Request error: {err}")
        print(f"Request error: {err}")
    except WebDriverException as err:
        _log.log_error_message(f"WebDriver error: {err}")
        print(f"WebDriver error: {err}")
    except IOError as err:
        _log.log_error_message(f"An I/O error occurred: {err}")
        print(f"I/O error occurred: {err}")
