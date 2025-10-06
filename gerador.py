import json
import os

ARQUIVO_JSON = "historico.json"


def carregar_dados():
    """Carrega os dados do arquivo JSON se existir."""
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"filmes": {}, "turmas": {}}


def salvar_dados(dados):
    """Salva os dados no arquivo JSON."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def listar_filmes(dados):
    """Lista os filmes cadastrados e retorna a lista."""
    filmes = list(dados["filmes"].keys())
    if not filmes:
        print("🎬 Nenhum filme cadastrado ainda.\n")
        return []
    print("\n=== FILMES CADASTRADOS ===")
    for i, filme in enumerate(filmes, start=1):
        print(f"{i}. {filme}")
    print()
    return filmes


def cadastrar_filme(dados):
    """Adiciona um novo filme."""
    nome = input("Digite o nome do novo filme: ").strip()
    if not nome:
        print("⚠️ Nome inválido.\n")
        return
    if nome in dados["filmes"]:
        print("⚠️ Esse filme já está cadastrado.\n")
        return

    dados["filmes"][nome] = True
    salvar_dados(dados)
    print(f"✅ Filme '{nome}' cadastrado com sucesso!\n")


def excluir_filme(dados):
    """Remove um filme e todas as avaliações associadas."""
    filmes = listar_filmes(dados)
    if not filmes:
        return

    try:
        escolha = int(input("Digite o número do filme que deseja remover: ")) - 1
        if 0 <= escolha < len(filmes):
            filme_removido = filmes[escolha]

            # Remover o filme do dicionário de filmes
            del dados["filmes"][filme_removido]

            # Remover o filme das turmas
            for serie in list(dados["turmas"].keys()):
                if filme_removido in dados["turmas"][serie]:
                    del dados["turmas"][serie][filme_removido]
                    if not dados["turmas"][serie]:
                        del dados["turmas"][serie]

            salvar_dados(dados)
            print(f"✅ Filme '{filme_removido}' e suas avaliações foram removidos.\n")
        else:
            print("⚠️ Escolha inválida.\n")
    except ValueError:
        print("⚠️ Entrada inválida.\n")


def atualizar_media(dados, filme, serie):
    """Atualiza a média da turma para o filme."""
    turma = dados["turmas"][serie][filme]
    notas = [a["nota"] for a in turma["alunos"]]
    turma["media"] = round(sum(notas) / len(notas), 2) if notas else 0.0


def cadastrar_aluno(dados):
    """Cadastra um novo aluno e sua nota para um filme existente."""
    filmes = listar_filmes(dados)
    if not filmes:
        print("⚠️ Cadastre um filme antes de adicionar alunos.\n")
        return

    try:
        escolha = int(input("Escolha o número do filme: ")) - 1
        filme = filmes[escolha]
    except (ValueError, IndexError):
        print("⚠️ Escolha inválida.\n")
        return

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

    if serie not in dados["turmas"]:
        dados["turmas"][serie] = {}

    if filme not in dados["turmas"][serie]:
        dados["turmas"][serie][filme] = {"alunos": [], "media": 0.0}

    dados["turmas"][serie][filme]["alunos"].append({"nome": nome, "nota": nota})
    atualizar_media(dados, filme, serie)
    salvar_dados(dados)
    print(f"✅ Aluno {nome} da turma {serie} cadastrado para o filme '{filme}'.\n")


def mostrar_historico(dados):
    """Mostra as médias das turmas para cada filme."""
    if not dados["turmas"]:
        print("Nenhum aluno cadastrado ainda.\n")
        return

    print("\n=== HISTÓRICO DE AVALIAÇÕES ===")
    for serie, filmes in dados["turmas"].items():
        print(f"\n📚 Turma {serie}:")
        for filme, info in filmes.items():
            print(f"  🎬 Filme: {filme} — média {info['media']}")
            print("  Alunos:")
            for aluno in info["alunos"]:
                print(f"    - {aluno['nome']}: nota {aluno['nota']}")
            print("  --------------------------")
    print()


def editar_aluno(dados):
    """Edita nome ou nota de um aluno."""
    if not dados["turmas"]:
        print("Nenhum dado cadastrado.\n")
        return

    mostrar_historico(dados)
    serie = input("Digite a série do aluno: ").strip()
    if serie not in dados["turmas"]:
        print("⚠️ Turma não encontrada.\n")
        return

    filmes = list(dados["turmas"][serie].keys())
    for i, filme in enumerate(filmes, start=1):
        print(f"{i}. {filme}")
    try:
        escolha = int(input("Escolha o número do filme: ")) - 1
        filme = filmes[escolha]
    except (ValueError, IndexError):
        print("⚠️ Escolha inválida.\n")
        return

    alunos = dados["turmas"][serie][filme]["alunos"]
    for i, aluno in enumerate(alunos, start=1):
        print(f"{i}. {aluno['nome']} - nota {aluno['nota']}")

    try:
        indice = int(input("Digite o número do aluno que deseja editar: ")) - 1
        if 0 <= indice < len(alunos):
            novo_nome = input(f"Novo nome ({alunos[indice]['nome']}): ").strip()
            if novo_nome:
                alunos[indice]["nome"] = novo_nome

            nova_nota = input(f"Nova nota ({alunos[indice]['nota']}): ").strip()
            if nova_nota:
                try:
                    nova_nota = int(nova_nota)
                    if 1 <= nova_nota <= 8:
                        alunos[indice]["nota"] = nova_nota
                    else:
                        print("⚠️ Nota fora do intervalo. Mantida a anterior.")
                except ValueError:
                    print("⚠️ Valor inválido. Mantida a nota anterior.")
            atualizar_media(dados, filme, serie)
            salvar_dados(dados)
            print("✅ Aluno atualizado com sucesso!\n")
        else:
            print("⚠️ Número inválido.\n")
    except ValueError:
        print("⚠️ Entrada inválida.\n")


def excluir_aluno(dados):
    """Exclui um aluno."""
    if not dados["turmas"]:
        print("Nenhum dado cadastrado.\n")
        return

    mostrar_historico(dados)
    serie = input("Digite a série do aluno: ").strip()
    if serie not in dados["turmas"]:
        print("⚠️ Turma não encontrada.\n")
        return

    filmes = list(dados["turmas"][serie].keys())
    for i, filme in enumerate(filmes, start=1):
        print(f"{i}. {filme}")
    try:
        escolha = int(input("Escolha o número do filme: ")) - 1
        filme = filmes[escolha]
    except (ValueError, IndexError):
        print("⚠️ Escolha inválida.\n")
        return

    alunos = dados["turmas"][serie][filme]["alunos"]
    for i, aluno in enumerate(alunos, start=1):
        print(f"{i}. {aluno['nome']} - nota {aluno['nota']}")

    try:
        indice = int(input("Digite o número do aluno que deseja excluir: ")) - 1
        if 0 <= indice < len(alunos):
            removido = alunos.pop(indice)
            atualizar_media(dados, filme, serie)
            if not alunos:
                del dados["turmas"][serie][filme]
                if not dados["turmas"][serie]:
                    del dados["turmas"][serie]
            salvar_dados(dados)
            print(f"✅ Aluno {removido['nome']} removido com sucesso!\n")
        else:
            print("⚠️ Número inválido.\n")
    except ValueError:
        print("⚠️ Entrada inválida.\n")


def menu():
    """Menu principal da aplicação."""
    dados = carregar_dados()

    while True:
        print("=== SISTEMA DE AVALIAÇÃO DE FILMES ===")
        print("1. Cadastrar novo filme")
        print("2. Remover filme")
        print("3. Cadastrar novo aluno")
        print("4. Mostrar histórico e médias")
        print("5. Editar aluno")
        print("6. Excluir aluno")
        print("7. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_filme(dados)
        elif opcao == "2":
            excluir_filme(dados)
        elif opcao == "3":
            cadastrar_aluno(dados)
        elif opcao == "4":
            mostrar_historico(dados)
        elif opcao == "5":
            editar_aluno(dados)
        elif opcao == "6":
            excluir_aluno(dados)
        elif opcao == "7":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("⚠️ Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    menu()
