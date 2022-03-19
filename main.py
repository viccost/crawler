import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from page_models.pagina_produto_ldm import PaginaProdutoLdm
from page_models.pagina_produto_dtr import PaginaProdutoDtr
from page_models.pagina_produto_b2u import PaginaProdutoB2U
from page_models.pagina_produto_knd import PaginaProdutoKnd
from interaction_models.selenium_interaction_knd import SeleniumKndInteraction
from interaction_models.selenium_interaction_ldm import SeleniumLdmInteraction
from interaction_models.selenium_interaction_b2u import SeleniumB2UInteraction
from interaction_models.selenium_interaction_dtr import SeleniumDtrInteraction
from collected_data import SpreadsheetCollectData
from time import sleep
from selenium.webdriver.chrome.options import Options
from typing import Union
from constants import HEADER
import planilha_toscrape
import salvar_ajustar.salvar_ajustar as sv


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
        print(
            "Houve um problema ao transformar seus dados! Tente verificar o nome de suas colunas"
        )
        exit()


def get_page(url_pagina_produto) -> Union[BeautifulSoup, int]:
    try:
        site = requests.get(url_pagina_produto, headers=HEADER)
        conteudo = site.content
        pagina = BeautifulSoup(conteudo.decode("utf-8", "ignore"), features="lxml")
        return pagina
    except requests.exceptions.InvalidURL:
        print("URL INVÁLIDA")
        return 0


def get_page_model(
    page_model_to_scrape: Union[
        PaginaProdutoLdm, PaginaProdutoDtr, PaginaProdutoB2U, PaginaProdutoKnd
    ],
    page: BeautifulSoup(),
):
    return page_model_to_scrape(page)


def get_page_status(
    page_model_to_scrape: Union[
        PaginaProdutoLdm, PaginaProdutoDtr, PaginaProdutoB2U, PaginaProdutoKnd
    ]
) -> tuple:
    return page_model_to_scrape.all_status_product_page()


def check_if_needs_selenium(
    grade_pre_selecionada: str, searched_grid: str, multiplas_grades: bool
) -> bool:
    if (
        grade_pre_selecionada == searched_grid
        or searched_grid not in "110V220V"
        or not multiplas_grades
    ):
        return False
    else:
        return True


def main():
    planilha_to_scrape = get_spreadsheet_to_scrape()
    chrome = iniciar_chrome()
    collected_data = SpreadsheetCollectData()
    progress = 0

    # alterar conforme o conccorrente a ser scrapado
    iteraction_model: Union[
        SeleniumDtrInteraction,
        SeleniumLdmInteraction,
        SeleniumB2UInteraction,
        SeleniumKndInteraction,
    ] = SeleniumKndInteraction()
    page_model_to_scrape: Union[
        PaginaProdutoLdm, PaginaProdutoDtr, PaginaProdutoB2U, PaginaProdutoKnd
    ] = PaginaProdutoKnd

    to_scraping = transform_in_list(planilha_to_scrape)

    for record_to_collect in to_scraping:
        sleep(2)
        progress += 1
        print(progress)
        sku_ferimport = record_to_collect[0]
        url_product = record_to_collect[1]
        searched_grid = str(record_to_collect[2]).upper().replace("V", "")
        page = get_page(url_product)

        if page != 0:
            product_page = get_page_model(page_model_to_scrape, page)
            get_page_status(product_page)
            (
                disponibilidade,
                multiplas_grades,
                grade_pre_selecionada,
                spot_price,
                price,
            ) = get_page_status(product_page)
            # testing if interaction is necessary
            if check_if_needs_selenium(
                grade_pre_selecionada, searched_grid, multiplas_grades
            ):
                pass
            elif searched_grid in "110V220V":
                # NEEDS VALIDATION
                page = iteraction_model.alternar_voltagem(chrome, url_product)
                # if it returns 0 is because there is no iterable button
                if page != 0:
                    setattr(product_page, "pagina_produto", page)
                    (
                        disponibilidade,
                        multiplas_grades,
                        grade_pre_selecionada,
                        spot_price,
                        price,
                    ) = product_page.all_status_product_page()
                else:
                    print("Não foi possível encontrar o resultado da interação.")
            collected_data.add_price_collect(
                url_product,
                searched_grid,
                grade_pre_selecionada,
                spot_price,
                price,
                disponibilidade,
                sku_ferimport,
            )
        else:
            collected_data.add_url_error(url_product, sku_ferimport, searched_grid)
    collected_data.save_collected_data()


if __name__ == "__main__":
    main()
