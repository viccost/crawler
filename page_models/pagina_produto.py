import abc


class PaginaProduto(metaclass=abc.ABCMeta):
    """Represents the scraped product page and all informations that is necessary to get informatios."""
    @abc.abstractmethod
    def disponibilidade(self) -> bool:
        """Checks if the product is avaliable to buy."""
        ...

    @abc.abstractmethod
    def existe_mais_de_um_sku(self) -> bool:
        """Checks if the product have sku variation, like voltage specification."""
        ...

    @abc.abstractmethod
    def identificar_grade_selecionada(self) -> str:
        """Checks the variation selected in the first load page"""
        ...

    @abc.abstractmethod
    def coletar_preco(self) -> tuple:
        """Collect prices, in cash, parcels..."""

        ...

    def all_status_product_page(self) -> tuple:
        """Returns all page stats"""
        disponibilty = self.disponibilidade()
        multiple_grid = self.existe_mais_de_um_sku()
        selected_grid = self.identificar_grade_selecionada()
        spot_price, price = self.coletar_preco()
        return disponibilty, multiple_grid, selected_grid, spot_price, price
