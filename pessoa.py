"""Módulo que define a entidade base Pessoa."""

from exceptions import DadoInvalidoError


class Pessoa:
    """Representa uma pessoa com nome e idade validados.

    Attributes:
        nome (str): Nome completo da pessoa.
        idade (int): Idade em anos (deve ser entre 0 e 130).
    """

    def __init__(self, nome: str, idade: int) -> None:
        self.nome = nome
        self.idade = idade

    @property
    def nome(self) -> str:
        """Retorna o nome da pessoa."""
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        """Valida e define o nome da pessoa."""
        if not isinstance(valor, str) or not valor.strip():
            raise DadoInvalidoError("O nome não pode ser vazio e deve ser um texto.")
        self._nome = valor.strip()

    @property
    def idade(self) -> int:
        """Retorna a idade da pessoa."""
        return self._idade

    @idade.setter
    def idade(self, valor: int) -> None:
        """Valida e define a idade da pessoa."""
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise DadoInvalidoError("A idade deve ser um número inteiro.")
        if valor < 0 or valor > 130:
            raise DadoInvalidoError("A idade deve estar entre 0 e 130 anos.")
        self._idade = valor

    # Métodos de compatibilidade
    def get_nome(self) -> str:
        """Compatibilidade com versões legadas."""
        return self.nome

    def get_idade(self) -> int:
        """Compatibilidade com versões legadas."""
        return self.idade

    def __str__(self) -> str:
        return f"{self.nome}, {self.idade} anos"

    def __repr__(self) -> str:
        return f"Pessoa(nome={self.nome!r}, idade={self.idade})"
