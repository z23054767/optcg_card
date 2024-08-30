import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Function.Log.Log import Logger
from Function.DB.DB import SQLiteHandle
from Function.Common.Common import CommonHandle

class DriverHandle:
    """
        爬蟲相關類別
    """

    def __init__(self, script_directory : str):
        """
            爬蟲相關類別 建構子 

            Args:
            script_directory (str): 腳本目錄的路徑
        """
        self._logger : Logger = Logger(script_directory)
        """ 日誌記錄器 """
        self._dbHandle : SQLiteHandle = SQLiteHandle(script_directory)
        """ DB存取類別 """
        self._common : CommonHandle = CommonHandle()
        """ 通用方法類別 """

    def cookie_suggestion_close(self, driver) -> None:
        """
        關閉 cookie 設定頁面

        Args:
            driver (webdriver): 爬蟲driver
        """

        # 選擇至cookie設定頁之 x 按鈕 並點擊
        wait = WebDriverWait(driver, 10)
        close_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-close-btn-container')))
        close_button.find_element(By.TAG_NAME, 'button').click()
        print("稍後5秒")
        time.sleep(5)
    
    def get_cardlist(self, language_url) -> None:
        """
            取得系列列表
        
            Args:
            language_url (str): 用戶選擇的語言對應的網址
        """
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        # 註解下行可以開啟瀏覽器觀看操作
        options.add_argument("headless")
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        driver = webdriver.Chrome(options = options)

        try:
            driver.get(f"{language_url}/cardlist")

            self.cookie_suggestion_close(driver)
            
            # 等待 
            wait = WebDriverWait(driver, 10)
            series_col = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.formsetDefaultArea .seriesCol')))
            # 找到 select 元素
            select_element = series_col.find_element(By.TAG_NAME, 'select')
            options = select_element.find_elements(By.TAG_NAME, 'option')
            # 儲存系列資訊
            option_dict = {}
            for option in options:
                option_text = driver.execute_script("return arguments[0].text;", option).strip()
                option_value = option.get_attribute('value').strip() if option.get_attribute('value') else ''
                
                if not option_value:
                    continue
                
                option_text = self._common.process_series_name(option_text)
                
                if option_text and option_value:
                    option_dict[option_text] = option_value
        
            self._dbHandle.save_cardInfo(option_dict)
            driver.refresh()
        except Exception as err:
            self._logger.log_error_message(f"get_cardlist : {err}")
        finally:
            driver.quit()

    def handle_series_cardlist(self, series_id: str, language_url: str) -> None:
        """
        根據指定的系列 ID 和語言 URL 處理該系列的卡表信息。

        該方法使用給定的系列 ID 和對應語言的 URL 來獲取或處理特定系列的卡表數據。包括從網頁抓取數據、解析網頁內容等操作。

        Args:
            series_id (str): 系列的 ID。
            language_url (str): 用戶選擇的語言對應的卡表網頁 URL。

        Returns:
            None: 該方法不返回任何值，僅進行數據處理操作。
        """
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        # 註解下行可以開啟瀏覽器觀看操作
        options.add_argument("headless")
        options.add_argument('--log-level=3')
        options.add_argument('--silent')
        driver = webdriver.Chrome(options = options)

        try:
            card_list = []
            url = f'{language_url}/cardlist/?series={series_id}'
            driver.get(url)
            print("稍後5秒")
            time.sleep(5)

            self.cookie_suggestion_close(driver)

            result_col = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "resultCol")))
            modal_cols = result_col.find_elements(By.CLASS_NAME, "modalCol")
            for modal_col in modal_cols:
                # 找到所有 class="frontCol" 的 div 下的 img 標籤
                front_cols = modal_col.find_elements(By.CLASS_NAME, "frontCol")
                for front_col in front_cols:
                    img_tag = front_col.find_element(By.TAG_NAME, "img")
                    img_src = img_tag.get_attribute("data-src")
                    card_name = img_tag.get_attribute("alt")
                    
                    # 移除 ? 後的數字
                    if '?' in img_src:
                        img_src = img_src.split('?')[0]

                    # 替換 路徑
                    img_src = img_src.replace("../images/", f"{language_url}/images/")
                
                # 撈取 infoCol 欄位值
                info_col = WebDriverWait(modal_col, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "infoCol")))
                spans = info_col.find_elements(By.TAG_NAME, "span")
                card_id = driver.execute_script("return arguments[0].childNodes[0].nodeValue;", spans[0]).strip() if len(spans) > 0 else ""
                card_species = driver.execute_script("return arguments[0].childNodes[0].nodeValue;", spans[1]).strip() if len(spans) > 1 else ""
                card_type = driver.execute_script("return arguments[0].childNodes[0].nodeValue;", spans[2]).strip() if len(spans) > 2 else ""

                # 撈取 backCol 標籤值
                back_col = modal_col.find_element(By.CLASS_NAME, "backCol")
                cost_element = back_col.find_element(By.CLASS_NAME, "cost")
                cost_value = driver.execute_script("return arguments[0].childNodes[1].nodeValue;", cost_element).strip()             
                cost_value = 0 if not cost_value.isdigit() else int(cost_value)

                attribute_element = back_col.find_elements(By.CLASS_NAME, "attribute")
                if attribute_element:
                    img_element = attribute_element[0].find_elements(By.TAG_NAME, "img")
                    if img_element:
                        attribute_value = img_element[0].get_attribute("alt")
                    else:
                        attribute_value = '-'
                else:
                    attribute_value = '-'

                # 提取力量值
                power_element = back_col.find_element(By.CLASS_NAME, "power")
                power_value = driver.execute_script("return arguments[0].childNodes[1].nodeValue;", power_element).strip()
                power_value = 0 if not power_value.isdigit() else int(power_value)

                # 提取反擊值
                counter_element = back_col.find_element(By.CLASS_NAME, "counter")  
                counter_value = driver.execute_script("return arguments[0].childNodes[1].nodeValue;", counter_element).strip()     
                counter_value = 0 if not counter_value.isdigit() else int(counter_value)

                # 提取卡片顏色
                color_element = back_col.find_element(By.CLASS_NAME, "color")  
                color_value = driver.execute_script("return arguments[0].childNodes[1].nodeValue;", color_element).strip()

                # 提取特徵
                feature = back_col.find_element(By.CLASS_NAME, "feature")
                feature_value = driver.execute_script("return arguments[0].childNodes[1].nodeValue;", feature).strip()     

                # 提取效果
                effect = back_col.find_element(By.CLASS_NAME, "text")
                effect_value = driver.execute_script("return arguments[0].childNodes[1].nodeValue;", effect).strip()
                
                # 入手方式
                get_info = back_col.find_element(By.CLASS_NAME, "getInfo")
                get_info_value = driver.execute_script("return arguments[0].childNodes[1].nodeValue;", get_info).strip()

                card_info = {
                    "card_id" : card_id,
                    "card_name": card_name,
                    "card_species" : card_species,
                    "card_type" : card_type,
                    "img_src": img_src,
                    "cost": cost_value,
                    "attribute": attribute_value,
                    "power": power_value,
                    "counter": counter_value,
                    "color": color_value,
                    "feature": feature_value,
                    "effect": effect_value,
                    "get_info" : get_info_value,
                    "series_id" : series_id
                }

                card_list.append(card_info)

            # 將卡片資訊存入資料庫    
            self._dbHandle.save_series_database(card_list)
            driver.refresh()
            
        except Exception as err:
            self._logger.log_error_message(f"handle_series_cardlist : {err}")
        finally:
            driver.quit()

    def handle_all_cardlist(self, language_url) -> None:
        """
        處理全系列卡表，儲存資訊至資料庫

        Args:
            language_url (str): 用戶選擇的語言對應的網址
        """
        try:
            # 取得 卡片系列列表相關資訊
            self.get_cardlist(language_url)
            # 取出 卡片系列列表
            all_card_list_infos = self._dbHandle.load_cardInfo()
            # 逐一取出 product_id 並處理
            for product_name, product_id in all_card_list_infos.items():
                self.handle_series_cardlist(product_id, language_url)
                print(f"{product_name} 已處理完畢，並存入資料庫")
        except Exception as err:
            self._logger.log_error_message(f"handle_all_cardlist : {err}")