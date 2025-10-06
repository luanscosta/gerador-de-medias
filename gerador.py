import json
import os

ARQUIVO_JSON = "historico.json"


def carregar_dados():
    """Carrega os dados do arquivo JSON se existir."""
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_dados(dados):
    """Salva os dados no arquivo JSON."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def atualizar_media(dados, filme, serie):
    """Recalcula a média da turma para o filme."""
    turma = dados[filme][serie]
    if turma["alunos"]:
        notas = [a["nota"] for a in turma["alunos"]]
        turma["media"] = round(sum(notas) / len(notas), 2)
    else:
        turma["media"] = 0.0


def cadastrar_aluno(dados):
    """Cadastra um novo aluno e sua nota para um filme."""
    filme = input("Digite o nome do filme: ").strip()
    serie = input("Digite a série do aluno (ex: 7A, 8B, 9C): ").strip()
    nome = input("Digite o nome do aluno: ").strip()

    while True:
        try:
            nota = int(input("Digite a nota (1 a 8) que o aluno deu: "))
            if 1 <= nota <= 8:
                break
            else:
                print("⚠️ A nota deve estar entre 1 e 8.")
        except ValueError:
            print("⚠️ Digite um número válido.")

    if filme not in dados:
        dados[filme] = {}
    if serie not in dados[filme]:
        dados[filme][serie] = {"alunos": [], "media": 0.0}

    dados[filme][serie]["alunos"].append({"nome": nome, "nota": nota})
    atualizar_media(dados, filme, serie)
    salvar_dados(dados)
    print(f"✅ Aluno {nome} da turma {serie} cadastrado para o filme '{filme}'.\n")


def mostrar_turmas(dados):
    """Exibe as médias por filme e turma."""
    if not dados:
        print("Nenhum dado cadastrado ainda.\n")
        return

    print("\n=== HISTÓRICO DE AVALIAÇÕES ===")
    for filme, turmas in dados.items():
        print(f"\n🎬 Filme: {filme}")
        for serie, info in turmas.items():
            print(f"  Turma {serie}: média {info['media']}")
            print("  Alunos:")
            for aluno in info["alunos"]:
                print(f"    - {aluno['nome']}: nota {aluno['nota']}")
            print("  -----------------------")
    print()


def editar_aluno(dados):
    """Edita nome ou nota de um aluno."""
    if not dados:
        print("Nenhum dado cadastrado.\n")
        return

    mostrar_turmas(dados)
    filme = input("Digite o nome do filme: ").strip()
    if filme not in dados:
        print("⚠️ Filme não encontrado.\n")
        return

    serie = input("Digite a série do aluno: ").strip()
    if serie not in dados[filme]:
        print("⚠️ Turma não encontrada.\n")
        return

    alunos = dados[filme][serie]["alunos"]
    for i, aluno in enumerate(alunos, start=1):
        print(f"{i}. {aluno['nome']} - nota {aluno['nota']}")

    try:
        indice = int(input("Digite o número do aluno que deseja editar: ")) - 1
        if 0 <= indice < len(alunos):
            novo_nome = input(f"Novo nome ({alunos[indice]['nome']}): ").strip()
            if novo_nome:
                alunos[indice]["nome"] = novo_nome

            while True:
                nova_nota = input(f"Nova nota ({alunos[indice]['nota']}): ").strip()
                if not nova_nota:
                    break
                try:
                    nova_nota = int(nova_nota)
                    if 1 <= nova_nota <= 8:
                        alunos[indice]["nota"] = nova_nota
                        break
                    else:
                        print("⚠️ Nota deve estar entre 1 e 8.")
                except ValueError:
                    print("⚠️ Digite um número válido.")
            atualizar_media(dados, filme, serie)
            salvar_dados(dados)
            print("✅ Aluno atualizado com sucesso!\n")
        else:
            print("⚠️ Número inválido.\n")
    except ValueError:
        print("⚠️ Entrada inválida.\n")


def excluir_aluno(dados):
    """Exclui um aluno de uma turma para um filme."""
    if not dados:
        print("Nenhum dado cadastrado.\n")
        return

    mostrar_turmas(dados)
    filme = input("Digite o nome do filme: ").strip()
    if filme not in dados:
        print("⚠️ Filme não encontrado.\n")
        return

    serie = input("Digite a série do aluno: ").strip()
    if serie not in dados[filme]:
        print("⚠️ Turma não encontrada.\n")
        return

    alunos = dados[filme][serie]["alunos"]
    for i, aluno in enumerate(alunos, start=1):
        print(f"{i}. {aluno['nome']} - nota {aluno['nota']}")

    try:
        indice = int(input("Digite o número do aluno que deseja excluir: ")) - 1
        if 0 <= indice < len(alunos):
            removido = alunos.pop(indice)
            atualizar_media(dados, filme, serie)
            salvar_dados(dados)
            print(f"✅ Aluno {removido['nome']} removido do filme '{filme}'.\n")

            # remove turma/filme vazios
            if not dados[filme][serie]["alunos"]:
                del dados[filme][serie]
                if not dados[filme]:
                    del dados[filme]
                salvar_dados(dados)
        else:
            print("⚠️ Número inválido.\n")
    except ValueError:
        print("⚠️ Entrada inválida.\n")


def menu():
    """Menu principal da aplicação."""
    dados = carregar_dados()

    while True:
        print("=== SISTEMA DE AVALIAÇÃO DE FILMES ===")
        print("1. Cadastrar novo aluno")
        print("2. Mostrar médias e histórico")
        print("3. Editar aluno")
        print("4. Excluir aluno")
        print("5. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_aluno(dados)
        elif opcao == "2":
            mostrar_turmas(dados)
        elif opcao == "3":
            editar_aluno(dados)
        elif opcao == "4":
            excluir_aluno(dados)
        elif opcao == "5":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    menu()
