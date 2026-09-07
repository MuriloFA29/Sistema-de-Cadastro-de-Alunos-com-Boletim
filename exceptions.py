"""Módulo de exceções de domínio do sistema escolar."""


class SistemaEscolarError(Exception):
    """Exceção base para erros de domínio do sistema escolar."""
    pass


class DadoInvalidoError(SistemaEscolarError):
    """Lançada quando um dado de entrada não atende às regras de negócio."""
    pass


class NotaInvalidaError(DadoInvalidoError):
    """Lançada quando uma nota informada está fora da faixa permitida (0.0 a 10.0)."""
    pass


class MatriculaInvalidaError(DadoInvalidoError):
    """Lançada quando uma matrícula é vazia ou inválida."""
    pass


class AlunoDuplicadoError(SistemaEscolarError):
    """Lançada quando se tenta cadastrar um aluno com matrícula já existente."""
    pass


class AlunoNaoEncontradoError(SistemaEscolarError):
    """Lançada quando uma busca ou operação não encontra o aluno correspondente."""
    pass
