from pessoa import Pessoa


class Aluno(Pessoa):
    def __init__(self, nome, idade, matricula):
        super().__init__(nome, idade)
        self.__matricula = matricula
        self.__notas = []

    def adicionar_nota(self, nota):
        self.__notas.append(nota)

    def calcular_media(self):
        if not self.__notas:
            return 0
        return sum(self.__notas) / len(self.__notas)

    def verificar_aprovacao(self):
        return self.calcular_media() >= 6

    def get_matricula(self):
        return self.__matricula

    def get_notas(self):
        return self.__notas

    def __str__(self):
        status = "Aprovado" if self.verificar_aprovacao() else "Reprovado"
        return f"{super().__str__()} - Matrícula: {self.__matricula} - Média: {self.calcular_media():.2f} - {status}"

    # Getters

    def get_matricula(self):
        return self.__matricula

    def get_notas(self):
        return self.__notas
