import json

from aluno import Aluno


class SistemaAlunos:
    def __init__(self):
        self.alunos = []

    def cadastrar_aluno(self, nome, idade, matricula):
        novo_aluno = Aluno(nome, idade, matricula)
        self.alunos.append(novo_aluno)

    def remover_aluno(self, matricula):
        self.alunos = [
            aluno for aluno in self.alunos if aluno.get_matricula() != matricula]

    def buscar_aluno(self, termo):
        for aluno in self.alunos:
            if termo.lower() in aluno.get_nome().lower() or termo == aluno.get_matricula():
                return aluno
        return None

    def listar_alunos(self):
        return self.alunos

    def salvar_em_arquivo(self, caminho="alunos.json"):
        with open(caminho, "w", encoding="utf-8") as f:
            dados = []
            for aluno in self.alunos:
                dados.append({
                    "nome": aluno.get_nome(),
                    "idade": aluno.get_idade(),
                    "matricula": aluno.get_matricula(),
                    "notas": aluno.get_notas()
                })
            json.dump(dados, f, ensure_ascii=False, indent=4)

    def carregar_de_arquivo(self, caminho="alunos.json"):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                for item in dados:
                    aluno = Aluno(
                        item["nome"], item["idade"], item["matricula"])
                    for nota in item["notas"]:
                        aluno.adicionar_nota(nota)
                    self.alunos.append(aluno)
        except FileNotFoundError:
            pass
