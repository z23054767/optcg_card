import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from functions.common.common import Common
from functions.database.database import Database


class Crawler:
    """
    爬蟲相關類別
    """

    def __init__(self, script_directory: str):
        """
        爬蟲相關類別 建構子

        Args:
        script_directory (str): 腳本目錄的路徑
        """
        self._database: Database = Database(script_directory)
        """ DB存取類別 """
        self._common: Common = Common()
        """ 通用方法類別 """

    @Common.exception_handler
    def cookie_suggestion_close(self, driver) -> None:
        """
        關閉 cookie 設定頁面

        Args:
            driver (webdriver): 爬蟲driver
        """
        wait = WebDriverWait(driver, 10)
        close_button = wait.until(
            EC.element_to_be_clickable((By.ID, "onetrust-close-btn-container"))
        )
        close_button.find_element(By.TAG_NAME, "button").click()
        print("稍後5秒")
        time.sleep(5)

    @Common.exception_handler
    def get_card_list(self, language_url) -> None:
        """
        取得系列列表

        Args:
        language_url (str): 用戶選擇的語言對應的網址
        """
        options = self.setup_driver_options()
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(f"{language_url}/cardlist")

            self.cookie_suggestion_close(driver)

            wait = WebDriverWait(driver, 10)
            series_col = wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".formsetDefaultArea .seriesCol")
                )
            )
            select_element = series_col.find_element(By.TAG_NAME, "select")
            options = select_element.find_elements(By.TAG_NAME, "option")
            option_dict = {}
            for option in options:
                option_text = driver.execute_script(
                    "return arguments[0].text;", option
                ).strip()
                option_value = (
                    option.get_attribute("value").strip()
                    if option.get_attribute("value")
                    else ""
                )

                if not option_value:
                    continue

                option_text = self._common.process_series_name(option_text)

                if option_text and option_value:
                    option_dict[option_text] = option_value

            self._database.save_card_info(option_dict)
            driver.refresh()
        finally:
            driver.quit()

    @Common.exception_handler
    def extract_card_info(self, modal_col, language_url) -> dict:
        """
        提取卡片信息

        Args:
            modal_col (WebElement): 卡片模態框元素
            language_url (str): 用戶選擇的語言對應的網址

        Returns:
            dict: 卡片信息字典
        """
        front_cols = modal_col.find_elements(By.CLASS_NAME, "frontCol")
        card_info = {}
        for front_col in front_cols:
            img_tag = front_col.find_element(By.TAG_NAME, "img")
            img_src = img_tag.get_attribute("data-src")
            card_name = img_tag.get_attribute("alt")

            if "?" in img_src:
                img_src = img_src.split("?")[0]

            img_src = img_src.replace("../images/", f"{language_url}/images/")
            card_info["img_src"] = img_src
            card_info["card_name"] = card_name

        return card_info

    @Common.exception_handler
    def get_element_text(self, driver, element, script) -> str:
        """
        獲取元素文本

        Args:
            driver (webdriver): 爬蟲driver
            element (WebElement): 目標元素
            script (str): 執行的JavaScript腳本

        Returns:
            str: 元素文本
        """
        return driver.execute_script(script, element).strip()

    @Common.exception_handler
    def get_cost_value(self, driver, back_col) -> int:
        """
        獲取卡片費用

        Args:
            driver (webdriver): 爬蟲driver
            back_col (WebElement): 卡片資訊列

        Returns:
            int: 卡片成本值
        """
        cost_element = back_col.find_element(By.CLASS_NAME, "cost")
        cost_value = self.get_element_text(
            driver, cost_element, "return arguments[0].childNodes[1].nodeValue;"
        )
        return 0 if not cost_value.isdigit() else int(cost_value)

    @Common.exception_handler
    def get_attribute_value(self, back_col) -> str:
        """
        獲取卡片屬性

        Args:
            back_col (WebElement): 卡片資訊列

        Returns:
            str: 卡片屬性值
        """
        attribute_element = back_col.find_elements(By.CLASS_NAME, "attribute")
        if attribute_element:
            img_element = attribute_element[0].find_elements(By.TAG_NAME, "img")
            if img_element:
                return img_element[0].get_attribute("alt")
        return "-"

    @Common.exception_handler
    def get_power_value(self, driver, back_col) -> int:
        """
        獲取卡片力量值

        Args:
            driver (webdriver): 爬蟲driver
            back_col (WebElement): 卡片資訊列

        Returns:
            int: 卡片力量值
        """
        power_element = back_col.find_element(By.CLASS_NAME, "power")
        power_value = self.get_element_text(
            driver, power_element, "return arguments[0].childNodes[1].nodeValue;"
        )
        return 0 if not power_value.isdigit() else int(power_value)

    @Common.exception_handler
    def get_counter_value(self, driver, back_col) -> int:
        """
        獲取卡片反擊值

        Args:
            driver (webdriver): 爬蟲driver
            back_col (WebElement): 卡片資訊列

        Returns:
            int: 卡片反擊值
        """
        counter_element = back_col.find_element(By.CLASS_NAME, "counter")
        counter_value = self.get_element_text(
            driver, counter_element, "return arguments[0].childNodes[1].nodeValue;"
        )
        return 0 if not counter_value.isdigit() else int(counter_value)

    @Common.exception_handler
    def get_color_value(self, driver, back_col) -> str:
        """
        獲取卡片顏色

        Args:
            driver (webdriver): 爬蟲driver
            back_col (WebElement): 卡片資訊列

        Returns:
            str: 卡片顏色值
        """
        color_element = back_col.find_element(By.CLASS_NAME, "color")
        return self.get_element_text(
            driver, color_element, "return arguments[0].childNodes[1].nodeValue;"
        )

    @Common.exception_handler
    def get_feature_value(self, driver, back_col) -> str:
        """
        獲取卡片特徵

        Args:
            driver (webdriver): 爬蟲driver
            back_col (WebElement): 卡片資訊列

        Returns:
            str: 卡片特徵值
        """
        feature = back_col.find_element(By.CLASS_NAME, "feature")
        return self.get_element_text(
            driver, feature, "return arguments[0].childNodes[1].nodeValue;"
        )

    @Common.exception_handler
    def get_effect_value(self, driver, back_col) -> str:
        """
        獲取卡片效果

        Args:
            driver (webdriver): 爬蟲driver
            back_col (WebElement): 卡片資訊列

        Returns:
            str: 卡片效果值
        """
        effect = back_col.find_element(By.CLASS_NAME, "text")
        return driver.execute_script(
            """
            let element = arguments[0];
            let htmlContent = element.innerHTML;
            htmlContent = htmlContent.replace(/<h3[^>]*>.*?<\\/h3>/gi, '');
            htmlContent = htmlContent.replace(/<br\\s*\\/?>/gi, ' ');
            return htmlContent.trim();
            """,
            effect,
        ).strip()

    @Common.exception_handler
    def get_get_info_value(self, driver, back_col) -> str:
        """
        獲取卡片信息

        Args:
            driver (webdriver): 爬蟲driver
            back_col (WebElement): 卡片資訊列

        Returns:
            str: 卡片信息值
        """
        get_info = back_col.find_element(By.CLASS_NAME, "getInfo")
        return self.get_element_text(
            driver, get_info, "return arguments[0].childNodes[1].nodeValue;"
        )

    @Common.exception_handler
    def extract_card_attributes(self, driver, back_col) -> dict:
        """
        提取卡片屬性

        Args:
            driver (webdriver): 爬蟲driver
            back_col (WebElement): 卡片資訊列

        Returns:
            dict: 卡片屬性字典
        """
        cost_value = self.get_cost_value(driver, back_col)
        attribute_value = self.get_attribute_value(back_col)
        power_value = self.get_power_value(driver, back_col)
        counter_value = self.get_counter_value(driver, back_col)
        color_value = self.get_color_value(driver, back_col)
        feature_value = self.get_feature_value(driver, back_col)
        effect_value = self.get_effect_value(driver, back_col)
        get_info_value = self.get_get_info_value(driver, back_col)

        return {
            "cost": cost_value,
            "attribute": attribute_value,
            "power": power_value,
            "counter": counter_value,
            "color": color_value,
            "feature": feature_value,
            "effect": effect_value,
            "get_info": get_info_value,
        }

    @Common.exception_handler
    def setup_driver_options(self) -> webdriver.ChromeOptions:
        """
        設置 WebDriver 選項

        Returns:
            webdriver.ChromeOptions: 設置好的 WebDriver 選項
        """
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
        options.add_argument("headless")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        return options

    @Common.exception_handler
    def process_card_info(self, driver, modal_col, language_url, series_id) -> dict:
        """
        處理卡片信息

        Args:
            driver (webdriver): 爬蟲driver
            modal_col (WebElement): 爬蟲driver撈取的卡片元素列表
            language_url (str): 用戶選擇的語言對應的網址
            series_id (str): 系列ID

        Returns:
            dict: 卡片信息字典
        """
        card_info = self.extract_card_info(modal_col, language_url)

        info_col = WebDriverWait(modal_col, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "infoCol"))
        )
        spans = info_col.find_elements(By.TAG_NAME, "span")
        card_id = (
            driver.execute_script(
                "return arguments[0].childNodes[0].nodeValue;", spans[0]
            ).strip()
            if len(spans) > 0
            else ""
        )
        card_species = (
            driver.execute_script(
                "return arguments[0].childNodes[0].nodeValue;", spans[1]
            ).strip()
            if len(spans) > 1
            else ""
        )
        card_type = (
            driver.execute_script(
                "return arguments[0].childNodes[0].nodeValue;", spans[2]
            ).strip()
            if len(spans) > 2
            else ""
        )

        back_col = modal_col.find_element(By.CLASS_NAME, "backCol")
        card_attributes = self.extract_card_attributes(driver, back_col)

        card_info.update(
            {
                "card_id": card_id,
                "card_species": card_species,
                "card_type": card_type,
                "series_id": series_id,
            }
        )
        card_info.update(card_attributes)

        return card_info

    @Common.exception_handler
    def handle_series_card_list(self, series_id: str, language_url: str) -> None:
        """
        處理系列卡片列表，儲存資訊至資料庫

        Args:
            series_id (str): 系列ID
            language_url (str): 用戶選擇的語言對應的網址
        """
        options = self.setup_driver_options()
        driver = webdriver.Chrome(options=options)

        try:
            card_list = []
            url = f"{language_url}/cardlist/?series={series_id}"
            driver.get(url)
            print("稍後5秒")
            time.sleep(5)

            self.cookie_suggestion_close(driver)

            result_col = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "resultCol"))
            )
            modal_cols = result_col.find_elements(By.CLASS_NAME, "modalCol")
            for modal_col in modal_cols:
                card_info = self.process_card_info(
                    driver, modal_col, language_url, series_id
                )
                card_list.append(card_info)

            self._database.save_series_database(card_list)
            driver.refresh()
        finally:
            driver.quit()

    @Common.exception_handler
    def handle_all_card_list(self, language_url) -> None:
        """
        處理全系列卡表，儲存資訊至資料庫

        Args:
            language_url (str): 用戶選擇的語言對應的網址
        """
        self.get_card_list(language_url)
        all_card_list_infos = self._database.load_card_info()
        for product_name, product_id in all_card_list_infos.items():
            self.handle_series_card_list(product_id, language_url)
            print(f"{product_name} 已處理完畢，並存入資料庫")
