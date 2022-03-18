import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pagina_produto_ldm import PaginaProdutoLdm
from pagina_produto_dtr import PaginaProdutoDtr
from pagina_produto_b2u import PaginaProdutoB2U
import planilha_toscrape
import salvar_ajustar.salvar_ajustar as sv
from collected_data import SpreadsheetCollectData
from selenium_interaction_ldm import SeleniumLdmInteraction
from selenium_interaction_b2u import SeleniumB2UInteraction
from selenium_interaction_dtr import SeleniumDtrInteraction
from time import sleep
from selenium.webdriver.chrome.options import Options
from typing import Union
from constants import HEADER


def iniciar_chrome() -> webdriver.Chrome:
    options = Options()
    options.headless = True
    driver = webdriver.Chrome()
    # add headless later, didn't work to ldm
    return driver


def get_spreadsheet_to_scrape():
    planilha_to_scrape = sv.gerar_dataframe(sv.escolher_arquivo())
    planilha_to_scrape = planilha_to_scrape.fillna(" ")
    return planilha_to_scrape


def transform_in_list(planilha_to_scrape):
    try:
        to_scraping = planilha_toscrape.PlanilhaToScrape(
            planilha_to_scrape
        ).transformar_em_lista()
        return to_scraping
    except planilha_toscrape.FormatoPlanilhaErrado:
        print("Houve um problema ao transformar seus dados! Tente verificar o nome de suas colunas")
        exit()


def main():
    planilha_to_scrape = get_spreadsheet_to_scrape()
    chrome = iniciar_chrome()
    collected_data = SpreadsheetCollectData()
    progress = 0

    # alterar conforme o conccorrente a ser scrapado
    iteraction: Union[
        SeleniumDtrInteraction, SeleniumLdmInteraction, SeleniumB2UInteraction
    ] = SeleniumB2UInteraction()
    concorrent_page: Union[PaginaProdutoLdm, PaginaProdutoDtr, PaginaProdutoB2U] = PaginaProdutoB2U

    to_scraping = transform_in_list(planilha_to_scrape)

    for produto_para_coleta in to_scraping:
        sleep(4)
        progress += 1
        print(progress)
        sku_correspondente = produto_para_coleta[0]
        url_pagina_produto = produto_para_coleta[1]
        grade_procurada = str(produto_para_coleta[2]).upper().replace("V", "")
        try:
            site = requests.get(url_pagina_produto, headers=HEADER)
            conteudo = site.content
            pagina = BeautifulSoup(conteudo.decode("utf-8", "ignore"), features="lxml")

        except requests.exceptions.InvalidURL:
            collected_data.add_url_error(
                url_pagina_produto, sku_correspondente, grade_procurada
            )
            continue
        # pre search
        _pagina_produto = concorrent_page(pagina)
        (
            disponibilidade,
            multiplas_grades,
            grade_pre_selecionada,
            spot_price,
            price,
        ) = _pagina_produto.all_status_product_page()

        # testing if interaction is necessary
        if (
                grade_pre_selecionada == grade_procurada
                or grade_procurada not in "110V220V"
                or not multiplas_grades
        ):
            spot_price, price = _pagina_produto.coletar_preco()
        elif grade_procurada in "110V220V":
            pagina = iteraction.alternar_voltagem(chrome, url_pagina_produto)
            # if it returns 0 is because there is no iterable button
            if pagina != 0:
                setattr(_pagina_produto, "pagina_produto", pagina)
                (
                    disponibilidade,
                    multiplas_grades,
                    grade_pre_selecionada,
                    spot_price,
                    price,
                ) = _pagina_produto.all_status_product_page()

        collected_data.add_price_collect(
            url_pagina_produto,
            grade_procurada,
            grade_pre_selecionada,
            spot_price,
            price,
            disponibilidade,
            sku_correspondente,
        )
    collected_data.save_collected_data()


if __name__ == "__main__":
    main()
