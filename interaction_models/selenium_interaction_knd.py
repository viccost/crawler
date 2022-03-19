import selenium
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from .selenium_interaction import SeleniumInteraction
from typing import Union
from selenium.webdriver.support.ui import Select


class SeleniumKndInteraction(SeleniumInteraction):
    def alternar_voltagem(
        self, navegador: selenium.webdriver, url_page: str
    ) -> Union[SeleniumInteraction.pegar_html_selenium, int]:
        navegador.get(url_page)
        WebDriverWait(navegador, 12).until(
            ec.presence_of_element_located((By.CLASS_NAME, "row"))
        )
        try:
            select = Select(
                navegador.find_element(
                    By.XPATH,
                    '//*[@id="single-product'
                    '"]/div[2]/div/div[2]/div['
                    "2]/div/div[4]/div["
                    "2]/div/div/select",
                )
            )
            select.select_by_visible_text("220 V")
            WebDriverWait(navegador, 14).until(
                ec.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="single-product'
                        '"]/div[2]/div/div[2]/div['
                        "2]/div/div[4]/div["
                        "2]/div/div/select",
                    )
                )
            )
            sleep(2)
            return self.pegar_html_selenium(navegador)
        except ElementNotInteractableException:
            return 0


if __name__ == "__main__":
    '''url = "https://www.ferramentaskennedy.com.br/6830/aspirador-e-extratora-ea135-1400w-220v-ipc-soteco"
    drive = iniciar_chrome()
    X = SeleniumKndInteraction()
    test = X.alternar_voltagem(drive, url)'''
