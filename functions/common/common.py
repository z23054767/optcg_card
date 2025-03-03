import json
import logging
import os
import re
import sys


class Common:
    """
    通用方法類別
    """

    @staticmethod
    def exception_handler(func):
        """
        統一處理異常。
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error("在 %s 發生錯誤: %s", func.__name__, e)
                raise

        return wrapper

    @exception_handler
    def get_script_directory(self, script_directory: str) -> str:
        """
        獲取腳本目錄的路徑，考慮到打包後的情況

        Args:
        script_directory (str): 當前腳本文件的路徑

        Returns:
        str: 調整後的腳本目錄路徑
        """
        if getattr(sys, "frozen", False):
            # 如果是被打包的可執行文件，使用 sys.executable
            return os.path.dirname(sys.executable)
        # 否則使用原始的腳本目錄
        return os.path.dirname(os.path.abspath(script_directory))

    @exception_handler
    def process_series_name(self, series_name: str) -> str:
        """
        根據給定的 series_name 提取 `【】` 內的文字，若無 `【】`，則返回處理過的 option_text

        Args:
            series_name (str): 卡片系列原始名稱
        """
        match = re.search(r"【(.*?)】", series_name)
        if match:
            return match.group(1)
        return series_name.split("<br")[0].strip()

    @exception_handler
    def get_user_choice_language_url(self) -> str:
        """
        提示用戶選擇網站語言版本並返回對應的 URL。

        該方法將提示用戶輸入語言代碼（如 'ja', 'cn', 'hk', 'tw', 'th', 'asia-en', 'en', 'fr'）來選擇對應的網頁URL。
        如果用戶輸入無效，將繼續提示用戶直到輸入有效。

        Returns:
            str: 返回用戶選擇的語言對應的網址。
        """
        with open("json/language_url.json", "r", encoding="utf-8") as file:
            language_urls = json.load(file)

        language_prompt = (
            "請輸入語言代碼：\n"
            "日本語(請輸入：ja)\n"
            "简体中文(請輸入：cn)\n"
            "繁體中文(HK)(請輸入：hk)\n"
            "繁體中文(TW)(請輸入：tw)\n"
            "ไทย(請輸入：th)\n"
            "English(Asia)(請輸入：asia-en)\n"
            "English(US/Europe/LatAm/Oceania)(請輸入：en)\n"
            "Français(請輸入：fr)\n"
            "離開(請輸入：exit)\n"
        )

        while True:
            choice = input(language_prompt).strip().lower()
            if choice == "exit":
                print("程式結束....")
                sys.exit()
            elif choice in language_urls:
                print("=====================================")
                return language_urls[choice]
            print("無效輸入，請輸入有效的語言代碼。")
