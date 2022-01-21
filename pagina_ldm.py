import bs4


class PaginaProdutoLdm:
    pagina_produto: bs4.BeautifulSoup

    def __init__(self, pagina):
        self.pagina_produto = pagina
        pass

    def disponibilidade(self) -> bool:
        try:
            text = self.pagina_produto.find("div", {"id": "produtoEsgotado"}).get_text()
            disponivel = False if text else True
        except AttributeError:
            disponivel = True
        return disponivel

    # OK
    def existe_mais_um_sku(self) -> bool:
        existe_grade = False
        try:
            text = self.pagina_produto.find("div", class_="col-12 col-sm-12 paddingNull product-volts").text.replace(" ",
                                                                                                                "").replace(
                "\n", "").replace("Volts", "").replace("Tensão:", "")
            existe_grade = True if text == '110220' else False
        except AttributeError:
            existe_grade = False
        finally:
            return existe_grade

    def identificar_grade_selecionada(self) -> str:
        try:
            grade_ja_selecionada = self.pagina_produto.find('button', 'btn-product-volts').text.split()[0]
        except AttributeError:
            grade_ja_selecionada = "Não há"
        return grade_ja_selecionada

    # OK
    def status_produto_da_pagina(self) -> tuple:
        status_disponibilidade = self.disponibilidade()
        status_mais_de_uma_grade = self.existe_mais_um_sku()
        status_grade_ldm = self.identificar_grade_selecionada()
        return status_disponibilidade, status_mais_de_uma_grade, status_grade_ldm

    # OK
    def coletar_preco(self) -> tuple:
        try:
            preco_vista = self.pagina_produto.find("span", {"id": "product-price"}).text
        except AttributeError:
            preco_vista = ''
        try:
            preco_prazo = self.pagina_produto.find("div", class_="product-sell-price-group").text.replace("\n", "")
        except AttributeError:
            preco_prazo = ''
        return preco_vista, preco_prazo

