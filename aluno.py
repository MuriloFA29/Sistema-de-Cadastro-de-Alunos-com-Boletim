"""Módulo que define a entidade Aluno, com gestão de notas e aprovação."""

from typing import Any, Dict, List
from exceptions import MatriculaInvalidaError, NotaInvalidaError
from pessoa import Pessoa


class Aluno(Pessoa):
    """Representa um aluno matriculado, herdando de Pessoa.

    Attributes:
        nome (str): Nome do aluno.
        idade (int): Idade do aluno.
        matricula (str): Código identificador único da matrícula.
        notas (List[float]): Lista de avaliações do aluno.
    """

    MEDIA_APROVACAO: float = 6.0

    def __init__(self, nome: str, idade: int, matricula: str) -> None:
        super().__init__(nome, idade)
        self.matricula = matricula
        self._notas: List[float] = []

    @property
    def matricula(self) -> str:
        """Retorna o código de matrícula."""
        return self._matricula

    @matricula.setter
    def matricula(self, valor: str) -> None:
        """Valida e define a matrícula do aluno."""
        if not isinstance(valor, str) or not valor.strip():
            raise MatriculaInvalidaError("A matrícula não pode ser vazia e deve ser textual.")
        self._matricula = valor.strip().upper()

    @property
    def notas(self) -> List[float]:
        """Retorna uma cópia da lista de notas para proteger o estado interno."""
        return list(self._notas)

    def adicionar_nota(self, nota: float) -> None:
        """Adiciona uma nota ao histórico do aluno.

        Args:
            nota: Valor numérico entre 0.0 e 10.0.

        Raises:
            NotaInvalidaError: Se a nota for de tipo inválido ou fora de [0, 10].
        """
        if not isinstance(nota, (int, float)) or isinstance(nota, bool):
            raise NotaInvalidaError("A nota deve ser um valor numérico.")

        nota_float = round(float(nota), 2)
        if not (0.0 <= nota_float <= 10.0):
            raise NotaInvalidaError(f"Nota inválida ({nota}). O valor deve estar entre 0.0 e 10.0.")

        self._notas.append(nota_float)

    def calcular_media(self) -> float:
        """Calcula a média aritmética das notas cadastradas.

        Returns:
            float: Média arredondada para 2 casas decimais, ou 0.0 se não houver notas.
        """
        if not self._notas:
            return 0.0
        return round(sum(self._notas) / len(self._notas), 2)

    def verificar_aprovacao(self, media_minima: float = MEDIA_APROVACAO) -> bool:
        """Verifica se o aluno atingiu a média necessária para aprovação."""
        return self.calcular_media() >= media_minima

    @property
    def status(self) -> str:
        """Retorna a situação acadêmica textual do aluno."""
        return "Aprovado" if self.verificar_aprovacao() else "Reprovado"

    def to_dict(self) -> Dict[str, Any]:
        """Serializa os dados do aluno em um dicionário."""
        return {
            "nome": self.nome,
            "idade": self.idade,
            "matricula": self.matricula,
            "notas": self.notas,
            "media": self.calcular_media(),
            "status": self.status
        }

    # Métodos de compatibilidade com implementações anteriores
    def get_matricula(self) -> str:
        """Compatibilidade com versões legadas."""
        return self.matricula

    def get_notas(self) -> List[float]:
        """Compatibilidade com versões legadas."""
        return self.notas

    def __str__(self) -> str:
        return (
            f"{super().__str__()} - Matrícula: {self.matricula} - "
            f"Notas: {self._notas} - Média: {self.calcular_media():.2f} - {self.status}"
        )

    def __repr__(self) -> str:
        return f"Aluno(nome={self.nome!r}, idade={self.idade}, matricula={self.matricula!r})"
