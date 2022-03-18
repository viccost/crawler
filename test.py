from selenium import webdriver


def iniciar_chrome() -> webdriver.Chrome:
    driver = webdriver.Chrome()
    # add headless later, didn't work to ldm
    return driver


drive = iniciar_chrome()
drive.get('https://pagespeed.web.dev/report?url=https%3A%2F%2Fwww.ferimport.com.br%2F')