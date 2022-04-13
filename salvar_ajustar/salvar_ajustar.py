"""
Module for helps to handling excel files. As save multiple archives and
generate dataframes.

    Written by Victor Costa (victorcost_@outlook.com).
    version 1.0
"""

import pandas as pd
import xlsxwriter


def escolher_arquivo() -> str:
    """Abre uma janela para que o usuário possa escolher QUALQUER ARQUIVO."""
    import tkinter as tk
    from tkinter import filedialog

    # Talvez setar os formatos específicos seja uma bom upgrade.
    root = tk.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path == "":
        print("Encerrando")
        return exit()
    return file_path


def escolher_pasta() -> str:
    """Abre uma janela para que o usuário possa escolher QUALQUER ARQUIVO."""
    import tkinter as tk
    from tkinter import filedialog

    # Talvez setar os formatos específicos seja uma bom upgrade.
    root = tk.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    folder_path = filedialog.askdirectory()
    if folder_path == "":
        print("Encerrando")
        return exit()
    return folder_path


def gerar_dataframe(file_path, name_sheet= 0) -> pd.DataFrame:
    """Espera um arquivo .xls, .xlsx, .csv para converter para um pandas.DataFrame e retorná-lo"""
    # checar tipo do arquivo ou trycatch para tratar erros
    planilha = pd.read_excel(file_path, index_col=None, sheet_name=name_sheet)
    return planilha


def salvar_arquivo_planilha(
    planilha: pd.DataFrame, nome: str, formato: str, folder: str = ""
) -> None:
    """Recebe um DataFrame e nome do arquivo para salvá-lo como .xlsx. Ajusta automaticamente o tamanho das colunas.
    Index do DataFrame está setado como falso. E os campos em branco estão mantidos em branco sem alteração."""
    _formato = formato

    def checar_caminho() -> None:
        from os import path

        if path.exists(caminho_desktop):
            pass
        else:
            print(
                "Erro: Defina corretamente o caminho até a pasta que deseja salvar suas planilhas!\n"
                "Encerrando."
            )
            exit()

    def salvar() -> None:
        checar_caminho()
        engine = "xlsxwriter"
        if _formato == "xls":
            engine = "xlwt"

        writer = pd.ExcelWriter(
            rf"{caminho_desktop}\{nome}.{_formato}", engine=f"{engine}"
        )
        # engine_kwargs={'options': {'strings_to_numbers': True}})
        planilha.to_excel(writer, sheet_name=f"{nome}", index=False)
        try:
            writer.save()
            print(f'A planilha "{nome}" foi criada!')
        except Exception as err:
            print(f"Erro ao salvar o arquivo: {err}")
            exit()

    if folder == "":
        caminho_desktop = escolher_pasta()
    else:
        caminho_desktop = folder

    return salvar()


def salvar_planilhas(df_para_salvar: list):
    """Função para salvar uma lista de dicionarios que contenham o nome do arquivo e o dataframe a ser salvo.

    :param df_para_salvar: list -> [{},{}]"""
    caminho_desktop = escolher_pasta()
    for df in df_para_salvar:
        nome = df["Nome"]
        modelo_dataframe = df["Dataframe"]
        salvar_arquivo_planilha(modelo_dataframe, nome, "xlsx", caminho_desktop)
