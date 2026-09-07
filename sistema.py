"""Módulo responsável pelo gerenciamento de alunos e persistência de dados."""

import json
import os
from typing import Any, Dict, List, Optional
from aluno import Aluno
from exceptions import AlunoDuplicadoError, AlunoNaoEncontradoError


class SistemaAlunos:
    """Gerencia a coleção de alunos, operações de CRUD, relatórios e persistência.

    Attributes:
        arquivo_padrao (str): Caminho do arquivo JSON de persistência.
        alunos (List[Aluno]): Lista de alunos em memória.
    """

    def __init__(self, arquivo_padrao: str = "alunos.json") -> None:
        self.arquivo_padrao: str = arquivo_padrao
        self.alunos: List[Aluno] = []

    def cadastrar_aluno(self, nome: str, idade: int, matricula: str) -> Aluno:
        """Cadastra um novo aluno no sistema, garantindo matrícula única.

        Args:
            nome: Nome completo do aluno.
            idade: Idade do aluno.
            matricula: Identificador único.

        Returns:
            Aluno: Instância do aluno criado.

        Raises:
            AlunoDuplicadoError: Se já existir aluno com a matrícula informada.
        """
        matricula_formatada = matricula.strip().upper()
        if self.buscar_por_matricula(matricula_formatada):
            raise AlunoDuplicadoError(
                f"Já existe um aluno cadastrado com a matrícula '{matricula_formatada}'."
            )

        novo_aluno = Aluno(nome, idade, matricula_formatada)
        self.alunos.append(novo_aluno)
        return novo_aluno

    def remover_aluno(self, matricula: str) -> bool:
        """Remove um aluno com base na matrícula.

        Args:
            matricula: Matrícula do aluno a ser removido.

        Returns:
            bool: True se o aluno foi encontrado e removido, False caso contrário.
        """
        matricula_formatada = matricula.strip().upper()
        tamanho_original = len(self.alunos)
        self.alunos = [
            a for a in self.alunos if a.matricula != matricula_formatada
        ]
        return len(self.alunos) < tamanho_original

    def buscar_por_matricula(self, matricula: str) -> Optional[Aluno]:
        """Busca um aluno específico pela matrícula exata (case-insensitive)."""
        matricula_formatada = matricula.strip().upper()
        for aluno in self.alunos:
            if aluno.matricula == matricula_formatada:
                return aluno
        return None

    def buscar_aluno(self, termo: str) -> Optional[Aluno]:
        """Busca o primeiro aluno correspondente por matrícula ou parte do nome."""
        termo_limpo = termo.strip().lower()
        if not termo_limpo:
            return None

        # 1º: Prioriza correspondência exata de matrícula
        por_matricula = self.buscar_por_matricula(termo_limpo)
        if por_matricula:
            return por_matricula

        # 2º: Busca parcial no nome
        for aluno in self.alunos:
            if termo_limpo in aluno.nome.lower():
                return aluno
        return None

    def buscar_por_nome(self, nome: str) -> List[Aluno]:
        """Retorna todos os alunos cujo nome contém o termo buscado."""
        termo = nome.strip().lower()
        if not termo:
            return []
        return [a for a in self.alunos if termo in a.nome.lower()]

    def listar_alunos(self) -> List[Aluno]:
        """Retorna a lista completa de alunos cadastrados."""
        return list(self.alunos)

    def listar_aprovados(self) -> List[Aluno]:
        """Retorna lista de alunos aprovados (média >= 6.0)."""
        return [a for a in self.alunos if a.verificar_aprovacao()]

    def listar_reprovados(self) -> List[Aluno]:
        """Retorna lista de alunos reprovados (média < 6.0)."""
        return [a for a in self.alunos if not a.verificar_aprovacao()]

    def calcular_media_turma(self) -> float:
        """Calcula a média geral da turma (média das médias dos alunos com notas)."""
        alunos_com_notas = [a for a in self.alunos if a.notas]
        if not alunos_com_notas:
            return 0.0
        soma_medias = sum(a.calcular_media() for a in alunos_com_notas)
        return round(soma_medias / len(alunos_com_notas), 2)

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna um resumo analítico do desempenho escolar da turma."""
        total = len(self.alunos)
        aprovados = len(self.listar_aprovados())
        reprovados = total - aprovados
        taxa_aprovacao = round((aprovados / total * 100), 1) if total > 0 else 0.0

        return {
            "total_alunos": total,
            "aprovados": aprovados,
            "reprovados": reprovados,
            "taxa_aprovacao_pct": taxa_aprovacao,
            "media_turma": self.calcular_media_turma()
        }

    def salvar_em_arquivo(self, caminho: Optional[str] = None) -> str:
        """Persiste os dados de todos os alunos em um arquivo JSON.

        Args:
            caminho: Caminho do arquivo. Se omitido, usa self.arquivo_padrao.

        Returns:
            str: Caminho do arquivo salvo.
        """
        destino = caminho or self.arquivo_padrao
        dados = [aluno.to_dict() for aluno in self.alunos]

        diretorio = os.path.dirname(destino)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio, exist_ok=True)

        with open(destino, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        return destino

    def carregar_de_arquivo(self, caminho: Optional[str] = None) -> int:
        """Carrega os alunos a partir de um arquivo JSON.

        Args:
            caminho: Caminho do arquivo. Se omitido, usa self.arquivo_padrao.

        Returns:
            int: Quantidade de alunos carregados.
        """
        origem = caminho or self.arquivo_padrao
        if not os.path.exists(origem):
            return 0

        try:
            with open(origem, "r", encoding="utf-8") as f:
                dados = json.load(f)

            novos_alunos: List[Aluno] = []
            for item in dados:
                aluno = Aluno(
                    nome=item["nome"],
                    idade=item["idade"],
                    matricula=item["matricula"]
                )
                for nota in item.get("notas", []):
                    aluno.adicionar_nota(nota)
                novos_alunos.append(aluno)

            self.alunos = novos_alunos
            return len(self.alunos)

        except (json.JSONDecodeError, KeyError, TypeError):
            # Arquivo corrompido ou formato inválido
            return 0
