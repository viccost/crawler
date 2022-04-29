from bs4 import BeautifulSoup
from page_models.pagina_produto import PaginaProduto


class PaginaProdutoB2U(PaginaProduto):
    pagina_produto: BeautifulSoup

    def __init__(self, pagina: BeautifulSoup):
        self.pagina_produto = pagina
        pass

    def disponibilidade(self) -> bool:
        obj = self.pagina_produto.find(
            "button", {"class": "styles__Button-sc-13a2o83-3 llNZvE"}
        )
        if obj:
            disponivel = False
        else:
            disponivel = True
        return disponivel

    # OK
    def existe_mais_de_um_sku(self) -> bool:
        existe_grade = False
        try:
            text = self.pagina_produto.find(
                "div", {"class": "old__Type-sc-uaqko9-6 miAcb"}
            ).text
            if "110" in text and "220" in text:
                existe_grade = True
            else:
                existe_grade = False
        except AttributeError:
            existe_grade = False
        finally:
            return existe_grade

    # ok MVP
    def identificar_grade_selecionada(self) -> str:
        try:
            grade_ja_selecionada = self.pagina_produto.find(
                "button", class_="old__Item-sc-uaqko9-7 kprnfv"
            ).text
        except AttributeError:
            try:
                grade_ja_selecionada = self.pagina_produto.find(
                    "strong", class_="old__Bold-sc-uaqko9-3 ldVOLn"
                ).text
            except AttributeError:
                grade_ja_selecionada = "Não há"
        return grade_ja_selecionada

    # don't working
    def coletar_preco(self) -> tuple:
        try:
            preco_vista = self.pagina_produto.find(
                "div", {"class": "styles__PriceText-sc-x06r9i-0 dUTOlD priceSales"}
            ).text
        except AttributeError:
            preco_vista = ""
        preco_prazo = ""
        return preco_vista, preco_prazo
