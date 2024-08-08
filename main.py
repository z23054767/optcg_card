import os
from Function.DriverHandle.DriverHandle import DriverHandle
from Function.DB.DB import SQLiteHandle
from Function.Download.Download import ImageDownload
from Function.Log.Log import Logger


# 初始化設定
_script_directory : str = os.path.dirname(os.path.abspath(__file__))
_driverhandle : DriverHandle  = DriverHandle(_script_directory)
_dbHandle : SQLiteHandle = SQLiteHandle(_script_directory)
_download : ImageDownload = ImageDownload(_script_directory)
_logger : Logger = Logger(_script_directory)



if __name__ == "__main__":
    try:
        # 將所有的卡片資料存入資料庫
        _driverhandle.handle_all_cardlist()
        print("儲存卡片資料至資料庫完畢....")
        # 逐一讀取卡片資料
        print("取出儲存資料")
        all_cards_info = _dbHandle.fetch_card_info_with_series_id()
        # 逐一取出 series_id 並處理
        for card_info in all_cards_info:
            _download.download_image(card_info["cid"] , card_info["img_src"], card_info["series_name"])

        print("下載全系列卡圖完畢....")
    except Exception as err:
        _logger.log_error_message(f"__main__ : {err}")
        print(f"__main__ : {err}")
