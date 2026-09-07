"""Ponto de entrada do Sistema de Gestão Escolar (CLI).

Fornece uma interface de console robusta, amigável e segura contra falhas de digitação.
"""

import sys
from typing import Optional
from exceptions import DadoInvalidoError, SistemaEscolarError
from sistema import SistemaAlunos


def ler_texto(prompt: str, obrigatorio: bool = True) -> str:
    """Lê uma string do usuário com validação de obrigatoriedade."""
    while True:
        try:
            valor = input(prompt).strip()
            if obrigatorio and not valor:
                print("   ⚠️  Este campo não pode ficar em branco. Tente novamente.")
                continue
            return valor
        except (KeyboardInterrupt, EOFError):
            print("\n   ⚠️  Operação cancelada pelo usuário.")
            return ""


def ler_inteiro(prompt: str, min_val: int = 0, max_val: int = 130) -> Optional[int]:
    """Lê um número inteiro dentro de um intervalo válido."""
    while True:
        try:
            entrada = input(prompt).strip()
            if not entrada:
                print("   ⚠️  Digite um valor numérico.")
                continue
            valor = int(entrada)
            if not (min_val <= valor <= max_val):
                print(f"   ⚠️  O valor deve estar entre {min_val} e {max_val}.")
                continue
            return valor
        except ValueError:
            print("   ⚠️  Entrada inválida! Digite apenas números inteiros.")
        except (KeyboardInterrupt, EOFError):
            print("\n   ⚠️  Operação cancelada pelo usuário.")
            return None


def ler_float(prompt: str, min_val: float = 0.0, max_val: float = 10.0) -> Optional[float]:
    """Lê um número de ponto flutuante dentro de um intervalo válido."""
    while True:
        try:
            entrada = input(prompt).strip().replace(",", ".")
            if not entrada:
                print("   ⚠️  Digite uma nota numérica.")
                continue
            valor = float(entrada)
            if not (min_val <= valor <= max_val):
                print(f"   ⚠️  A nota deve estar entre {min_val:.1f} e {max_val:.1f}.")
                continue
            return valor
        except ValueError:
            print("   ⚠️  Entrada inválida! Digite um número decimal (ex: 7.5).")
        except (KeyboardInterrupt, EOFError):
            print("\n   ⚠️  Operação cancelada pelo usuário.")
            return None


def exibir_tabela_alunos(alunos: list) -> None:
    """Renderiza a lista de alunos em formato tabular alinhado."""
    if not alunos:
        print("\n   ⚠️  Nenhum aluno cadastrado no sistema.")
        return

    print("\n" + "=" * 88)
    print(f"{'MATRÍCULA':<12} | {'NOME':<25} | {'IDADE':<6} | {'MÉDIA':<7} | {'SITUAÇÃO':<12} | {'NOTAS'}")
    print("-" * 88)

    for aluno in alunos:
        notas_formatadas = ", ".join(f"{n:.1f}" for n in aluno.notas) if aluno.notas else "(Sem notas)"
        situacao_tag = "✅ Aprovado" if aluno.verificar_aprovacao() else "❌ Reprovado"
        print(
            f"{aluno.matricula:<12} | "
            f"{aluno.nome:<25} | "
            f"{aluno.idade:<6} | "
            f"{aluno.calcular_media():<7.2f} | "
            f"{situacao_tag:<12} | "
            f"{notas_formatadas}"
        )
    print("=" * 88)


def exibir_boletim(aluno) -> None:
    """Renderiza o boletim de um aluno em formato de cartão."""
    print("\n" + "┌" + "─" * 45 + "┐")
    print(f"│ {'BOLETIM ESCOLAR':^43} │")
    print("├" + "─" * 45 + "┤")
    print(f"│ Matrícula : {aluno.matricula:<31} │")
    print(f"│ Nome      : {aluno.nome:<31} │")
    print(f"│ Idade     : {aluno.idade} anos{' ' * 24} │")
    
    notas_str = ", ".join(f"{n:.1f}" for n in aluno.notas) if aluno.notas else "Nenhuma nota"
    print(f"│ Notas     : {notas_str:<31} │")
    print(f"│ Média     : {aluno.calcular_media():<31.2f} │")
    
    status_str = "APROVADO (>= 6.0)" if aluno.verificar_aprovacao() else "REPROVADO (< 6.0)"
    print(f"│ Situação  : {status_str:<31} │")
    print("└" + "─" * 45 + "┘")


def exibir_estatisticas(sistema: SistemaAlunos) -> None:
    """Exibe painel de métricas analíticas da turma."""
    stats = sistema.obter_estatisticas()
    print("\n" + "┌" + "─" * 45 + "┐")
    print(f"│ {'ESTATÍSTICAS DA TURMA':^43} │")
    print("├" + "─" * 45 + "┤")
    print(f"│ Total de Alunos  : {stats['total_alunos']:<25} │")
    print(f"│ Alunos Aprovados : {stats['aprovados']:<25} │")
    print(f"│ Alunos Reprovados: {stats['reprovados']:<25} │")
    print(f"│ Taxa de Aprovação: {stats['taxa_aprovacao_pct']:.1f}%{' ' * (24 - len(f'{stats['taxa_aprovacao_pct']:.1f}%'))} │")
    print(f"│ Média da Turma   : {stats['media_turma']:<25.2f} │")
    print("└" + "─" * 45 + "┘")


def menu_principal() -> None:
    """Renderiza as opções do menu principal."""
    print("\n" + "═" * 45)
    print("      📚 SISTEMA DE GESTÃO DE ALUNOS")
    print("═" * 45)
    print("  [1] Cadastrar novo aluno")
    print("  [2] Adicionar nota a um aluno")
    print("  [3] Buscar aluno / Ver boletim")
    print("  [4] Listar todos os alunos")
    print("  [5] Relatório e estatísticas da turma")
    print("  [6] Remover aluno")
    print("  [7] Salvar e Sair")
    print("═" * 45)


def main() -> None:
    """Execução principal do CLI com ciclo de vida seguro."""
    sistema = SistemaAlunos()
    qtd_carregados = sistema.carregar_de_arquivo()
    if qtd_carregados > 0:
        print(f"💾 {qtd_carregados} aluno(s) carregado(s) da base de dados.")

    try:
        while True:
            menu_principal()
            opcao = input("👉 Escolha uma opção: ").strip()

            match opcao:
                case "1":
                    print("\n📝 [CADASTRO DE ALUNO]")
                    nome = ler_texto("Nome completo: ")
                    if not nome:
                        continue
                    idade = ler_inteiro("Idade (anos): ", min_val=5, max_val=120)
                    if idade is None:
                        continue
                    matricula = ler_texto("Matrícula (ex: MAT01): ")
                    if not matricula:
                        continue

                    try:
                        aluno = sistema.cadastrar_aluno(nome, idade, matricula)
                        sistema.salvar_em_arquivo()
                        print(f"\n✅ Aluno '{aluno.nome}' cadastrado com sucesso!")
                    except SistemaEscolarError as err:
                        print(f"\n❌ Erro no cadastro: {err}")

                case "2":
                    print("\n🎯 [LANÇAMENTO DE NOTAS]")
                    matricula = ler_texto("Informe a matrícula do aluno: ")
                    if not matricula:
                        continue

                    aluno = sistema.buscar_por_matricula(matricula)
                    if not aluno:
                        print(f"\n❌ Aluno com matrícula '{matricula.upper()}' não encontrado.")
                        continue

                    print(f"   Aluno localizado: {aluno.nome} (Notas atuais: {aluno.notas})")
                    nota = ler_float("Digite a nota (0.0 a 10.0): ", min_val=0.0, max_val=10.0)
                    if nota is not None:
                        try:
                            aluno.adicionar_nota(nota)
                            sistema.salvar_em_arquivo()
                            print(f"\n✅ Nota {nota:.2f} lançada com sucesso!")
                            print(f"   Nova média: {aluno.calcular_media():.2f} ({aluno.status})")
                        except SistemaEscolarError as err:
                            print(f"\n❌ Erro ao adicionar nota: {err}")

                case "3":
                    print("\n🔍 [CONSULTAR ALUNO / BOLETIM]")
                    termo = ler_texto("Digite o nome ou a matrícula do aluno: ")
                    if not termo:
                        continue

                    aluno = sistema.buscar_aluno(termo)
                    if aluno:
                        exibir_boletim(aluno)
                    else:
                        print(f"\n❌ Nenhum aluno encontrado para '{termo}'.")

                case "4":
                    exibir_tabela_alunos(sistema.listar_alunos())

                case "5":
                    exibir_estatisticas(sistema)

                case "6":
                    print("\n🗑️  [REMOÇÃO DE ALUNO]")
                    matricula = ler_texto("Matrícula do aluno a remover: ")
                    if not matricula:
                        continue

                    aluno = sistema.buscar_por_matricula(matricula)
                    if not aluno:
                        print(f"\n❌ Aluno com matrícula '{matricula.upper()}' não foi encontrado.")
                        continue

                    confirmacao = input(f"❓ Tem certeza que deseja remover '{aluno.nome}'? (S/N): ").strip().upper()
                    if confirmacao == "S":
                        if sistema.remover_aluno(matricula):
                            sistema.salvar_em_arquivo()
                            print(f"\n✅ Aluno '{aluno.nome}' removido com sucesso!")
                    else:
                        print("\n↩️ Remoção cancelada.")

                case "7":
                    sistema.salvar_em_arquivo()
                    print("\n💾 Dados salvos com segurança.")
                    print("👋 Encerrando o sistema. Até logo!")
                    break

                case _:
                    print("\n⚠️ Opção inválida! Escolha um número de 1 a 7.")

    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ Interrupção detectada! Salvando dados antes de encerrar...")
        sistema.salvar_em_arquivo()
        print("💾 Dados persistidos com segurança. Até logo!")
        sys.exit(0)


if __name__ == "__main__":
    main()
