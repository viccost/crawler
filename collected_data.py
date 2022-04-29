from pandas import DataFrame
import salvar_ajustar.salvar_ajustar as sv


class SpreadsheetCollectData:

    dataFrameDict = {
        "URL Produto": [],
        "SKU Ferimport": [],
        "Grade Ferimport": [],
        "Grade Concorrente": [],
        "Preço a Vista": [],
        "Preço a Prazo": [],
        "Disponibilidade": [],
        "Observação": [],
    }

    def __init__(self):
        pass

    def add_url_error(
        self, product_url: str, sku_ferimport: int, grade_ferimport: str
    ) -> None:
        error_message = "invalid url"
        self.dataFrameDict["URL Produto"].append(product_url)
        self.dataFrameDict["SKU Ferimport"].append(sku_ferimport)
        self.dataFrameDict["Grade Ferimport"].append(grade_ferimport)
        self.dataFrameDict["Grade Concorrente"].append(error_message)
        self.dataFrameDict["Preço a Vista"].append(error_message)
        self.dataFrameDict["Preço a Prazo"].append(error_message)
        self.dataFrameDict["Disponibilidade"].append(error_message)
        self.dataFrameDict["Observação"].append(error_message)

    def add_price_collect(
        self,
        product_url,
        grade_ferimport,
        grade_concorrente,
        spot_price,
        price,
        disponibility,
        sku_ferimport,
    ):
        self.dataFrameDict["URL Produto"].append(product_url)
        self.dataFrameDict["SKU Ferimport"].append(sku_ferimport)
        self.dataFrameDict["Grade Ferimport"].append(grade_ferimport)
        self.dataFrameDict["Grade Concorrente"].append(grade_concorrente)
        self.dataFrameDict["Preço a Vista"].append(spot_price)
        self.dataFrameDict["Preço a Prazo"].append(price)
        self.dataFrameDict["Disponibilidade"].append(disponibility)
        if grade_ferimport != grade_concorrente and grade_ferimport != " ":
            observacao = "não há grade correspondente"
        else:
            observacao = "ok"
        self.dataFrameDict["Observação"].append(observacao)

    def save_collected_data(self):
        dataFrame = DataFrame.from_dict(self.dataFrameDict)
        sv.salvar_arquivo_planilha(
            dataFrame, "Scraping", "xlsx"
        )  # passando df para func que salva a planilha
