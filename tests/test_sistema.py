import json
import pytest
from exceptions import AlunoDuplicadoError
from sistema import SistemaAlunos


@pytest.fixture
def sistema():
    return SistemaAlunos()


class TestSistemaAlunosCRUD:
    def test_cadastrar_aluno_sucesso(self, sistema):
        aluno = sistema.cadastrar_aluno("Lucas Mendes", 20, "MAT01")
        assert aluno.nome == "Lucas Mendes"
        assert aluno.matricula == "MAT01"
        assert len(sistema.listar_alunos()) == 1

    def test_cadastrar_aluno_matricula_duplicada_lanca_excecao(self, sistema):
        sistema.cadastrar_aluno("Lucas Mendes", 20, "MAT01")
        with pytest.raises(AlunoDuplicadoError):
            sistema.cadastrar_aluno("Outro Lucas", 22, "mat01")  # case-insensitive

    def test_remover_aluno_existente(self, sistema):
        sistema.cadastrar_aluno("Lucas Mendes", 20, "MAT01")
        removido = sistema.remover_aluno("MAT01")
        assert removido is True
        assert len(sistema.listar_alunos()) == 0

    def test_remover_aluno_inexistente_retorna_false(self, sistema):
        removido = sistema.remover_aluno("INEXISTENTE")
        assert removido is False

    def test_buscar_aluno_por_matricula(self, sistema):
        sistema.cadastrar_aluno("Ana Paula", 18, "ANA123")
        encontrado = sistema.buscar_por_matricula("ana123")
        assert encontrado is not None
        assert encontrado.nome == "Ana Paula"

    def test_buscar_aluno_por_nome_parcial(self, sistema):
        sistema.cadastrar_aluno("Fernanda Lima", 21, "FL01")
        sistema.cadastrar_aluno("Fernando Silva", 23, "FS02")
        sistema.cadastrar_aluno("Bruno Costa", 20, "BC03")

        resultados = sistema.buscar_por_nome("fernan")
        assert len(resultados) == 2


class TestSistemaAlunosEstatisticas:
    def test_estatisticas_turma_vazia(self, sistema):
        stats = sistema.obter_estatisticas()
        assert stats["total_alunos"] == 0
        assert stats["media_turma"] == 0.0
        assert stats["taxa_aprovacao_pct"] == 0.0

    def test_estatisticas_com_alunos(self, sistema):
        a1 = sistema.cadastrar_aluno("Aluno 1", 20, "M1")
        a1.adicionar_nota(8.0)
        a1.adicionar_nota(8.0)  # Média 8.0 -> Aprovado

        a2 = sistema.cadastrar_aluno("Aluno 2", 20, "M2")
        a2.adicionar_nota(4.0)
        a2.adicionar_nota(4.0)  # Média 4.0 -> Reprovado

        stats = sistema.obter_estatisticas()
        assert stats["total_alunos"] == 2
        assert stats["aprovados"] == 1
        assert stats["reprovados"] == 1
        assert stats["taxa_aprovacao_pct"] == 50.0
        assert stats["media_turma"] == 6.0


class TestSistemaAlunosPersistencia:
    def test_salvar_e_carregar_arquivo(self, sistema, tmp_path):
        caminho_teste = str(tmp_path / "test_alunos.json")

        aluno = sistema.cadastrar_aluno("Juliana Ramos", 24, "JR99")
        aluno.adicionar_nota(9.5)
        aluno.adicionar_nota(8.5)
        sistema.salvar_em_arquivo(caminho_teste)

        # Criar novo sistema e carregar
        novo_sistema = SistemaAlunos(arquivo_padrao=caminho_teste)
        qtd = novo_sistema.carregar_de_arquivo()

        assert qtd == 1
        carregado = novo_sistema.buscar_por_matricula("JR99")
        assert carregado is not None
        assert carregado.nome == "Juliana Ramos"
        assert carregado.notas == [9.5, 8.5]
        assert carregado.calcular_media() == 9.0

    def test_carregar_arquivo_inexistente_retorna_zero(self, sistema, tmp_path):
        caminho_inexistente = str(tmp_path / "nao_existe.json")
        qtd = sistema.carregar_de_arquivo(caminho_inexistente)
        assert qtd == 0

    def test_carregar_arquivo_corrompido_retorna_zero_sem_crash(self, sistema, tmp_path):
        arquivo_corrompido = tmp_path / "corrompido.json"
        arquivo_corrompido.write_text("{conteudo invalido de json", encoding="utf-8")

        qtd = sistema.carregar_de_arquivo(str(arquivo_corrompido))
        assert qtd == 0
