# optcg_card

## 項目簡介

歡迎來到 `optcg_card` 項目！本項目旨在利用爬蟲技術從指定網站上抓取圖片和卡片資料。通過此項目，您可以輕鬆獲取並整理這些珍貴的卡片信息，使其更加便於收藏和管理。

## 項目特點

- **自動化資料抓取**：利用先進的爬蟲技術，自動從目標網站抓取卡片圖片和詳細資料。
- **高效的資料處理**：整理和存儲抓取到的資料，使其更易於訪問和使用。
- **友好的使用體驗**：通過簡潔明了的代碼結構和詳細的文檔，使得項目易於上手和維護。

## 系統要求

請確保您使用以下版本的 Python：

- **Python 版本**：3.11 或更高版本

## 安裝指南

1. 將項目克隆到本地：
    ```bash
    git clone https://github.com/z23054767/optcg_card.git
    ```
2. 進入項目目錄：
    ```bash
    cd optcg_card
    ```
3. 安裝所需的 Python 庫：
    ```bash
    pip install -r requirements.txt
    ```

## 使用說明

1. 運行主程序：
    ```bash
    python main.py
    ```
2. 根據提示輸入需要抓取的卡片網站地址及相關參數，程序將自動進行抓取並保存資料。

## 文件結構
optcg_card  
│  
├── Function/  
│ ├── Common/  
│ │ └── Common.py  
│ ├── DB/  
│ │ └── DB.py  
│ ├── Download/  
│ │ └── Download.py  
│ ├── DriverHandle/  
│ │ └── DriverHandle.py  
│ ├── Log/  
│   └── Log.py  
├── .gitignore  
├── main.py  
├── README.md  
└── requirements.txt  

## 打包為可執行文件

您可以使用 `PyInstaller` 將此項目打包為一個可在任何環境下運行的可執行文件。

1. 安裝 `PyInstaller`：
    ```bash
    pip install pyinstaller
    ```

2. 打包項目：
    ```bash
    pyinstaller --onefile --windowed --icon=optcg_card.ico --name=optcg_card --distpath D:/ main.py
    ```
    這個命令的含義如下：

    - `--onefile`：將所有文件打包成一個獨立的可執行文件。
    - `--windowed`：適用於 GUI 應用程式，不會打開控制台窗口。
    - `--icon=optcg_card.ico`：為生成的可執行文件指定圖標。
    - `--name=optcg_card`：指定生成的可執行文件名為 `optcg_card.exe`。
    - `--distpath D:/`：指定生成的可執行文件的輸出路徑為 `D:/`。

這將在 `D:/` 目錄下生成一個名為 `optcg_card.exe` 的可執行文件。

## 聯繫我們

如果您有任何疑問或需要進一步的幫助，請隨時通過以下方式與我們聯繫：

- 電子郵件: e23054767@gmail.com
- GitHub: [z23054767](https://github.com/z23054767)

感謝您使用 `optcg_card` 項目，祝您使用愉快！