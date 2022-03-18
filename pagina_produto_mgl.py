from bs4 import BeautifulSoup
from pagina_produto import PaginaProduto


class PaginaProdutoMGLU(PaginaProduto):
    pagina_produto: BeautifulSoup

    def __init__(self, pagina: BeautifulSoup):
        self.pagina_produto = pagina
        pass

    def disponibilidade(self) -> bool:
        obj = self.pagina_produto.find("div", {"class": "wrapper-product-unavailable__right"})
        if obj:
            disponivel = False
        else:
            disponivel = True
        return disponivel

    # OK
    def existe_mais_de_um_sku(self) -> bool:
        existe_grade = False
        try:
            text = self.pagina_produto.find("select", {"id": "variation-label"}).text
            if '110' in text and '220' in text:
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
                "select", class_="variation-label"
            ).text
        except AttributeError:
            grade_ja_selecionada = "Não há"
        return grade_ja_selecionada

    # testing
    def coletar_preco(self) -> tuple:
        def clean_model(text):
            """desconto à vista, sem parcelamento"""
            splited = text.split()
            idx = splited.index('por')
            preco_prazo = splited[idx + 2]
            preco_vista = splited[idx + 4]

            print(f"Preço a vista: {preco_prazo}")
            print(f"Preço a vista: {preco_vista}")

        def dirty_model(text):
            """desconto à vista, com parcelamento"""
            splited = text.split()
            idx = splited.index('por')
            preco_vista = splited[idx + 2]
            preco_prazo = splited[idx + 10]

            print(f"Preço a prazo: {preco_prazo}")
            print(f"Preço a vista: {preco_vista}")

        # check the price, the type...

        try:
            preco_vista = self.pagina_produto.find("span", {"class": "price-template__text"}).text
        except AttributeError:
            preco_vista = ""
        try:
            preco_prazo = self.pagina_produto.find("div", {"class": "price-template"}).text
        except AttributeError:
            preco_prazo = ""
        return preco_vista, preco_prazo
