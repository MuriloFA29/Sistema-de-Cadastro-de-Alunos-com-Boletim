from sistema import SistemaAlunos

sistema = SistemaAlunos()
sistema.carregar_de_arquivo()


def menu():
    print("\n📚 MENU - Sistema de Cadastro de Alunos")
    print("1. Cadastrar aluno")
    print("2. Adicionar nota a um aluno")
    print("3. Mostrar boletim de um aluno")
    print("4. Listar todos os alunos")
    print("5. Remover aluno")
    print("6. Sair")


while True:
    menu()
    opcao = input("Escolha uma opção: ")

    match opcao:
        case "1":
            nome = input("Nome: ")
            idade = int(input("Idade: "))
            matricula = input("Matrícula: ")
            sistema.cadastrar_aluno(nome, idade, matricula)
            print("✅ Aluno cadastrado com sucesso.")

        case "2":
            matricula = input("Matrícula do aluno: ")
            aluno = sistema.buscar_aluno(matricula)
            if aluno:
                nota = float(input("Digite a nota: "))
                aluno.adicionar_nota(nota)
                print("✅ Nota adicionada.")
            else:
                print("❌ Aluno não encontrado.")

        case "3":
            termo = input("Digite o nome ou matrícula do aluno: ")
            aluno = sistema.buscar_aluno(termo)
            if aluno:
                print("\n📄 Boletim:")
                print(aluno)
            else:
                print("❌ Aluno não encontrado.")

        case "4":
            alunos = sistema.listar_alunos()
            if not alunos:
                print("⚠️ Nenhum aluno cadastrado.")
            else:
                print("\n📋 Lista de Alunos:")
                for a in alunos:
                    print(a)

        case "5":
            matricula = input("Matrícula do aluno a remover: ")
            sistema.remover_aluno(matricula)
            print("🗑️ Aluno removido (se matrícula existia).")

        case "6":
            sistema.salvar_em_arquivo()
            print("👋 Saindo do sistema. Até mais!")
            break

        case _:
            print("❌ Opção inválida. Tente novamente.")
