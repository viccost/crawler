import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pagina_ldm
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException
from time import sleep
from pandas import DataFrame
import planilha_ldm
import salvar_ajustar.salvar_ajustar as sv


def iniciar_chrome() -> webdriver.Chrome:
    driver = webdriver.Chrome()
    return driver


def iniciar_coleta_sem_trocar_sku(_pagina_produto_ldm: pagina_ldm.PaginaProdutoLdm) -> tuple:
    preco_vista, preco_prazo = _pagina_produto_ldm.coletar_preco()
    return preco_vista, preco_prazo


def iniciar_coleta_com_troca_sku(navegador: webdriver, url_pagina_produto: str, grade_procurada: str,
                                 grade_pre_selecionada: str, _pagina_produto_ldm: pagina_ldm.PaginaProdutoLdm) -> tuple:
    """Vai requistar do selenium a interação com a página"""

    def pegar_html_selenium() -> BeautifulSoup:
        html = navegador.page_source
        pagina_navegador = BeautifulSoup(html, features="lxml")
        return pagina_navegador

    def alternar_voltagem() -> tuple:
        _observacao = "Ok."
        try:
            navegador.find_element(By.CLASS_NAME, 'btn-secondary').click()
            WebDriverWait(navegador, 14).until(
                ec.presence_of_element_located((By.ID, 'product')))
            sleep(2)
        except ElementNotInteractableException:
            _observacao = "Não há grade semelhante."
        finally:
            pagina_grade_atualizada = pegar_html_selenium()
            return pagina_grade_atualizada, _observacao

    navegador.get(url_pagina_produto)
    WebDriverWait(navegador, 14).until(
        ec.presence_of_element_located((By.ID, 'product')))
    observacao = ""

    pagina_produto = pegar_html_selenium()
    if grade_procurada != grade_pre_selecionada:
        pagina_produto, observacao = alternar_voltagem()

    setattr(_pagina_produto_ldm, 'pagina_produto', pagina_produto)
    disponibilidade, mais_de_uma_grade, grade_selecionada = _pagina_produto_ldm.status_produto_da_pagina()
    preco_vista, preco_prazo = _pagina_produto_ldm.coletar_preco()

    return preco_vista, preco_prazo, grade_selecionada, observacao, disponibilidade


def verificar_se_tem_grade():
    def incrementar_listas(_url, grade, grade_ldm, _preco_vista, _preco_prazo, _observacao, disponivel, multiplas_grades):
        df_url.append(_url)
        df_grade.append(grade)
        df_grade_ldm.append(grade_ldm)
        df_preco_vista.append(_preco_vista)
        df_preco_prazo.append(_preco_prazo)
        df_observacao.append(_observacao)
        df_disponibilidade.append(disponivel)
        df_sku_corresp.append(multiplas_grades)

    def gerar_planilha():
        dataFrame = DataFrame()
        dataFrame["URL"] = df_url
        dataFrame["Tem grade"] = df_sku_corresp
        dataFrame["Grade"] = df_grade
        dataFrame["Grade LDM"] = df_grade_ldm
        dataFrame["A Vista"] = df_preco_vista
        dataFrame["A Prazo"] = df_preco_prazo
        dataFrame["Disponibilidade"] = df_disponibilidade
        dataFrame["Observação"] = df_observacao

        sv.salvar_arquivo_planilha(dataFrame, "Scrape LDM", "xlsx")  # passando df para func que salva a planilha

    df_url, df_grade, df_grade_ldm, df_preco_vista, df_preco_prazo, df_sku_corresp, df_disponibilidade, df_observacao = \
        ([] for i in range(8))  # listas que serão colunas na planilha

    arquivo_excel = sv.gerar_dataframe(sv.escolher_arquivo())
    chrome = iniciar_chrome()
    progress = 0
    try:
        ldm_para_coleta = planilha_ldm.PlanilhaLdm(arquivo_excel).transformar_em_lista()
        for produto_para_coleta in ldm_para_coleta:
            progress += 1
            print(progress)
            sku_correspondente = produto_para_coleta[0]
            url_pagina_produto = produto_para_coleta[1]
            grade_procurada = str(produto_para_coleta[2]).replace('V', '')

            try:
                site = requests.get(url_pagina_produto)
                conteudo = site.content
                pagina = BeautifulSoup(conteudo.decode('utf-8', 'ignore'), features="lxml")
                pagina_produto_ldm = pagina_ldm.PaginaProdutoLdm(pagina)
                disponibilidade, multiplas_grades, grade_pre_selecionada = pagina_produto_ldm.status_produto_da_pagina()

                if str(produto_para_coleta[2]) in '110V220V':
                    preco_vista, preco_prazo, grade_selecionada, observacao, disponibilidade = \
                        iniciar_coleta_com_troca_sku(chrome, url_pagina_produto, grade_procurada, grade_pre_selecionada,
                                                     pagina_produto_ldm)

                    incrementar_listas(url_pagina_produto, grade_procurada, grade_selecionada, preco_vista, preco_prazo,
                                       observacao, disponibilidade, sku_correspondente)
                else:
                    preco_vista, preco_prazo = iniciar_coleta_sem_trocar_sku(pagina_produto_ldm)
                    incrementar_listas(url_pagina_produto, grade_procurada, grade_pre_selecionada, preco_vista,
                                       preco_prazo, "Ok", disponibilidade, multiplas_grades)

            except requests.exceptions.InvalidURL:  # caso a url esteja errada
                incrementar_listas(url_pagina_produto, "Erro URL", "Erro URL", "Erro URL", "Erro URL", "Erro URL",
                                   "Erro URL", sku_correspondente)
        gerar_planilha()
    except planilha_ldm.FormatoPlanilhaErrado:
        print("Formato inválido da planilha")


def main():
    def incrementar_listas(_url, grade, grade_ldm, _preco_vista, _preco_prazo, _observacao, disponivel, sku_coorresp):
        df_url.append(_url)
        df_grade.append(grade)
        df_grade_ldm.append(grade_ldm)
        df_preco_vista.append(_preco_vista)
        df_preco_prazo.append(_preco_prazo)
        df_observacao.append(_observacao)
        df_disponibilidade.append(disponivel)
        df_sku_corresp.append(sku_coorresp)

    def gerar_planilha():
        dataFrame = DataFrame()
        dataFrame["URL"] = df_url
        dataFrame["SKU Correspondente"] = df_sku_corresp
        dataFrame["Grade"] = df_grade
        dataFrame["Grade LDM"] = df_grade_ldm
        dataFrame["A Vista"] = df_preco_vista
        dataFrame["A Prazo"] = df_preco_prazo
        dataFrame["Disponibilidade"] = df_disponibilidade
        dataFrame["Observação"] = df_observacao

        sv.salvar_arquivo_planilha(dataFrame, "Scrape LDM", "xlsx")  # passando df para func que salva a planilha

    df_url, df_grade, df_grade_ldm, df_preco_vista, df_preco_prazo, df_sku_corresp, df_disponibilidade, df_observacao = \
        ([] for i in range(8))  # listas que serão colunas na planilha

    arquivo_excel = sv.gerar_dataframe(sv.escolher_arquivo())
    chrome = iniciar_chrome()
    progress = 0
    try:
        ldm_para_coleta = planilha_ldm.PlanilhaLdm(arquivo_excel).transformar_em_lista()
        for produto_para_coleta in ldm_para_coleta:
            progress += 1
            print(progress)
            sku_correspondente = produto_para_coleta[0]
            url_pagina_produto = produto_para_coleta[1]
            grade_procurada = str(produto_para_coleta[2]).replace('V', '')

            try:
                site = requests.get(url_pagina_produto)
                conteudo = site.content
                pagina = BeautifulSoup(conteudo.decode('utf-8', 'ignore'), features="lxml")
                pagina_produto_ldm = pagina_ldm.PaginaProdutoLdm(pagina)
                disponibilidade, multiplas_grades, grade_pre_selecionada = pagina_produto_ldm.status_produto_da_pagina()

                if str(produto_para_coleta[2]) in '110V220V':
                    preco_vista, preco_prazo, grade_selecionada, observacao, disponibilidade = \
                        iniciar_coleta_com_troca_sku(chrome, url_pagina_produto, grade_procurada, grade_pre_selecionada,
                                                     pagina_produto_ldm)

                    incrementar_listas(url_pagina_produto, grade_procurada, grade_selecionada, preco_vista, preco_prazo,
                                       observacao, disponibilidade, sku_correspondente)
                else:
                    preco_vista, preco_prazo = iniciar_coleta_sem_trocar_sku(pagina_produto_ldm)
                    incrementar_listas(url_pagina_produto, grade_procurada, grade_pre_selecionada, preco_vista,
                                       preco_prazo, "Ok", disponibilidade, sku_correspondente)

            except requests.exceptions.InvalidURL:  # caso a url esteja errada
                incrementar_listas(url_pagina_produto, "Erro URL", "Erro URL", "Erro URL", "Erro URL", "Erro URL",
                                   "Erro URL", sku_correspondente)
        gerar_planilha()
    except planilha_ldm.FormatoPlanilhaErrado:
        print("Formato inválido da planilha")


if __name__ == '__main__':
    main()
