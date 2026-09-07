import pytest
from exceptions import DadoInvalidoError, MatriculaInvalidaError, NotaInvalidaError
from pessoa import Pessoa
from aluno import Aluno


class TestPessoa:
    def test_criacao_pessoa_valida(self):
        p = Pessoa("Maria Silva", 25)
        assert p.nome == "Maria Silva"
        assert p.idade == 25
        assert p.get_nome() == "Maria Silva"
        assert p.get_idade() == 25
        assert str(p) == "Maria Silva, 25 anos"

    def test_nome_vazio_lanca_excecao(self):
        with pytest.raises(DadoInvalidoError):
            Pessoa("   ", 20)

    def test_nome_nao_string_lanca_excecao(self):
        with pytest.raises(DadoInvalidoError):
            Pessoa(12345, 20)

    def test_idade_negativa_lanca_excecao(self):
        with pytest.raises(DadoInvalidoError):
            Pessoa("João", -1)

    def test_idade_invalida_tipo_lanca_excecao(self):
        with pytest.raises(DadoInvalidoError):
            Pessoa("João", "vinte")
        with pytest.raises(DadoInvalidoError):
            Pessoa("João", True)  # booleano em python herda de int


class TestAluno:
    def test_criacao_aluno_valido(self):
        a = Aluno("Carlos Souza", 19, "A001")
        assert a.nome == "Carlos Souza"
        assert a.idade == 19
        assert a.matricula == "A001"
        assert a.notas == []
        assert a.calcular_media() == 0.0
        assert not a.verificar_aprovacao()
        assert a.status == "Reprovado"

    def test_matricula_em_branco_lanca_excecao(self):
        with pytest.raises(MatriculaInvalidaError):
            Aluno("Carlos", 19, "   ")

    def test_adicao_de_notas_validas(self):
        a = Aluno("Carlos Souza", 19, "A001")
        a.adicionar_nota(7.5)
        a.adicionar_nota(8.5)
        assert a.notas == [7.5, 8.5]
        assert a.calcular_media() == 8.0
        assert a.verificar_aprovacao()
        assert a.status == "Aprovado"

    def test_adicao_de_nota_invalida_lanca_excecao(self):
        a = Aluno("Carlos", 19, "A001")
        with pytest.raises(NotaInvalidaError):
            a.adicionar_nota(-1.0)
        with pytest.raises(NotaInvalidaError):
            a.adicionar_nota(10.5)
        with pytest.raises(NotaInvalidaError):
            a.adicionar_nota("dez")

    def test_protecao_imunidade_lista_notas(self):
        a = Aluno("Carlos", 19, "A001")
        a.adicionar_nota(9.0)
        lista = a.notas
        lista.append(0.0)  # Tentativa de mutação externa
        assert a.notas == [9.0]  # Estado interno preservado

    def test_to_dict(self):
        a = Aluno("Beatriz", 22, "A002")
        a.adicionar_nota(6.0)
        d = a.to_dict()
        assert d["nome"] == "Beatriz"
        assert d["matricula"] == "A002"
        assert d["media"] == 6.0
        assert d["status"] == "Aprovado"
