from selenium import webdriver


class ChromeOptions:

    def __init__(self):
        self.__chrome_options = webdriver.ChromeOptions()
        self.__chrome_options = webdriver.ChromeOptions()
        self.__chrome_options.add_argument("--window-size=1920x1080")
        self.__chrome_options.add_argument("--disable-notifications")
        self.__chrome_options.add_argument("--no-sandbox")
        self.__chrome_options.add_argument("--verbose")
        self.__chrome_options.add_experimental_option(
            "prefs",
            {
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False,
            },
        )
        self.__chrome_options.add_argument("--disable-gpu")
        self.__chrome_options.add_argument("--disable-software-rasterizer")
        self.__chrome_options.add_argument("--headless")
        self.__chrome_options.add_argument("--log-level=3")
        self.__chrome_options.add_argument("--disable-dev-shm-usage")
        ''' driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=chrome_options
        )'''

    @property
    def chrome_options(self):
        return self.__chrome_options
