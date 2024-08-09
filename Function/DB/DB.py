import os
import shutil
import sqlite3
from Function.Log.Log import Logger

class SQLiteHandle:
    """
        SQLite DB 存取類別
    """

    def __init__(self, script_directory : str):
        """
            SQLite DB 存取類別 建構子

            Args:
            script_directory (str): 腳本目錄的路徑
        """
        
        self._script_directory : str = script_directory
        """ 腳本目錄的路徑 """
        self._logger : Logger = Logger(script_directory)
        """ 日誌記錄器 """
        self._dbPath : str = os.path.join(script_directory, 'DB', 'optcg.db')
        """ db連接資訊 """

    def check_dbFolder(self) -> None:
        """
            檢查是否存在 'DB' 資料夾，若存在則刪除後重新建立
        """
        try:
            db_dir = os.path.join(self._script_directory, 'DB')
            if os.path.exists(db_dir):
                shutil.rmtree(db_dir)
                print(f"已刪除資料夾: {db_dir}")
            
            os.makedirs(db_dir, exist_ok = True)
            print(f"已建立資料夾: {db_dir}")
            
        except Exception as err:
            self._logger.log_error_message(f"check_dbFolder : {err}")

    def save_cardInfo(self, series_cardlist_datas : dict) -> None:
        """
            將卡片系列名稱及ID存入資料庫
        """
        try:
            conn = sqlite3.connect(self._dbPath)
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS series_cardlist (
                series_id TEXT PRIMARY KEY,
                series_name TEXT
            )
            ''')
            for series_name, series_id in series_cardlist_datas.items():
                cursor.execute('''
                INSERT OR IGNORE INTO series_cardlist (series_id, series_name) VALUES (?, ?)
                ''', (series_id, series_name))
            conn.commit()
        except Exception as err:
            self._logger.log_error_message(f"save_cardInfo : {err}")
        finally:
            conn.close()

    def load_cardInfo(self) -> dict:
        """
        從資料庫中讀取卡表信息並轉換為字典

        Returns:
            dict : 包含所有卡片信息的字典，鍵為 series_name, 值為 series_id
        """
        card_infos = {}
        try:
            conn = sqlite3.connect(self._dbPath)
            cursor = conn.cursor()
            cursor.execute('SELECT series_id, series_name FROM series_cardlist')
            rows = cursor.fetchall()
            for row in rows:
                card_infos[row[1]] = row[0]
        except Exception as err:
            self._logger.log_error_message(f"load_cardInfo : {err}")
        finally:
            conn.close()

        return card_infos
    
    def save_series_database(self, card_series_list) -> None:
        """
        將網站上提取的系列卡片資訊 儲存到資料庫

        Args:
            card_series_list (list): 卡片系列資訊
        """
        try:
            conn = sqlite3.connect(self._dbPath)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS cards_info (
                            cid INTEGER PRIMARY KEY AUTOINCREMENT,
                            card_id TEXT,
                            card_name TEXT,
                            card_species TEXT,
                            card_type TEXT,
                            img_src TEXT,
                            cost INT,
                            attribute TEXT,
                            power INT,
                            counter INT,
                            color TEXT,
                            feature TEXT,
                            effect TEXT,
                            get_info TEXT,
                            series_id TEXT)''')

            for card_info in card_series_list:
                cursor.execute('''INSERT INTO cards_info (card_id, card_name, card_species, card_type, img_src, cost, attribute, power, counter, color, feature, effect, get_info, series_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                            (card_info['card_id'], card_info['card_name'], card_info['card_species'], card_info['card_type'], card_info['img_src'], card_info['cost'], card_info['attribute'], card_info['power'], card_info['counter'], card_info['color'], card_info['feature'], card_info['effect'], card_info['get_info'], card_info['series_id']))

            conn.commit()
            conn.close()
        except Exception as err:
            self._logger.log_error_message(f"save_series_database : {err}")
        finally:
            conn.close()

    def fetch_card_info_with_series_id(self) -> list:
        """
        取得欲下載的檔案資訊
        """
        card_info_list = []

        try:
            conn = sqlite3.connect(self._dbPath)
            cursor = conn.cursor()

            query = '''
            SELECT ci.cid, ci.img_src, sc.series_name
            FROM cards_info ci
            JOIN series_cardlist sc ON ci.series_id = sc.series_id
            '''

            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                card_info = {
                    "cid": row[0],
                    "img_src": row[1],
                    "series_name": row[2]
                }
                card_info_list.append(card_info)

        except Exception as err:
            self._logger.log_error_message(f"fetch_card_info_with_series_id : {err}")
        finally:
            conn.close()

        return card_info_list
    
    def save_file_info(self, cid: int, file_path: str):
        """
        將檔案資訊儲存到資料庫

        Args:
            cid (int): 圖片所屬卡片的cid(識別碼)
            file_path (str): 檔案的實際路徑
        """
        try:
            conn = sqlite3.connect(self._dbPath)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS files_info (
                                cid INTEGER PRIMARY KEY,
                                file_path TEXT)''')

            cursor.execute('''INSERT INTO files_info (cid, file_path)
                            VALUES (?, ?)''', 
                        (cid, file_path))

            conn.commit()
            
        except Exception as err:
            self._logger.log_error_message(f"save_file_info : {err}")
        finally:
            conn.close()
       