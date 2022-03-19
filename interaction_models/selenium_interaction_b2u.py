import selenium
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from .selenium_interaction import SeleniumInteraction
from typing import Union


# not implemented
class SeleniumB2UInteraction(SeleniumInteraction):
    def alternar_voltagem(
        self, navegador: selenium.webdriver, url_page: str
    ) -> Union[SeleniumInteraction.pegar_html_selenium, int]:
        try:
            return self.pegar_html_selenium(navegador)
        except (ElementNotInteractableException, NoSuchElementException):
            return 0
