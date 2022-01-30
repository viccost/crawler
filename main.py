import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pagina_produto_ldm
import planilha_ldm
import salvar_ajustar.salvar_ajustar as sv
from collected_data import SpreadsheetCollectData
from selenium_interaction_ldm import SeleniumLdmInteraction
from selenium.webdriver.chrome.options import Options


def iniciar_chrome() -> webdriver.Chrome:
    options = Options()
    options.headless = True
    driver = webdriver.Chrome()
    # add headless later
    return driver


def main():
    planilha_to_scrape = sv.gerar_dataframe(sv.escolher_arquivo())
    planilha_to_scrape = planilha_to_scrape.fillna("")
    chrome = iniciar_chrome()
    to_scraping = []
    collected_data = SpreadsheetCollectData()
    iteraction = SeleniumLdmInteraction()

    try:
        to_scraping = planilha_ldm.PlanilhaLdm(planilha_to_scrape).transformar_em_lista()
    except planilha_ldm.FormatoPlanilhaErrado:
        print("Formato inválido da planilha!")
        exit()

    for produto_para_coleta in to_scraping:
        sku_correspondente = produto_para_coleta[0]
        url_pagina_produto = produto_para_coleta[1]
        grade_procurada = str(produto_para_coleta[2]).upper().replace('V', '')
        try:
            site = requests.get(url_pagina_produto)
            conteudo = site.content
            pagina = BeautifulSoup(conteudo.decode('utf-8', 'ignore'), features="lxml")

        except requests.exceptions.InvalidURL:
            collected_data.add_url_error(url_pagina_produto, sku_correspondente, grade_procurada)
            continue

        _pagina_produto = pagina_produto_ldm.PaginaProdutoLdm(pagina)
        disponibilidade, multiplas_grades, grade_pre_selecionada, spot_price, price \
            = _pagina_produto.all_status_product_page()

        if grade_pre_selecionada == grade_procurada or grade_procurada not in '110V220V':
            spot_price, price = _pagina_produto.coletar_preco()
        elif grade_procurada in '110V220V':
            pagina = iteraction.alternar_voltagem(chrome, url_pagina_produto)
            # if it returns 0 is because there is no iterable button
            if pagina != 0:
                setattr(_pagina_produto, 'pagina_produto', pagina)
                disponibilidade, multiplas_grades, grade_pre_selecionada, spot_price, price \
                    = _pagina_produto.all_status_product_page()

        collected_data.add_price_collect(url_pagina_produto, grade_procurada, grade_pre_selecionada,
                                         spot_price, price, disponibilidade, sku_correspondente)
    collected_data.save_collected_data()


if __name__ == '__main__':
    main()
