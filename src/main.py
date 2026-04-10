# -*- coding: utf-8 -*-

import os
import producao as prod
import arquivo  as arq
import banco    as bco


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\n  Pressione ENTER para continuar...")


# -------------------------------------------------------
# VALIDACOES DE ENTRADA
# -------------------------------------------------------

def ler_float(mensagem, minimo=0.0):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if valor <= minimo:
                print(f"  Digite um valor maior que {minimo}.")
            else:
                return valor
        except ValueError:
            print("  Entrada invalida. Digite um numero.")


def ler_cultura():
    print("\n  Culturas disponiveis:")
    for c in prod.culturas:
        print(f"  - {c}")

    while True:
        entrada = input("\n  Digite o nome da cultura: ").strip().capitalize()
        if entrada in prod.culturas:
            return entrada
        print("  Cultura inexistente. Digite uma opcao valida.")


# -------------------------------------------------------
# TELAS
# -------------------------------------------------------

def tela_registrar():
    print("\n" + "=" * 50)
    print("  REGISTRAR PRODUCAO")
    print("=" * 50)

    cultura    = ler_cultura()
    rendimento = prod.rendimento_medio[cultura]

    print(f"\n  Rendimento medio de {cultura}: {rendimento} t/ha")
    usar_medio = input("  Usar rendimento medio? (s/n): ").strip().lower()

    if usar_medio != "s":
        rendimento = ler_float("  Digite o rendimento (t/ha): ")

    area  = ler_float("  Digite a area plantada (ha): ")
    preco = ler_float("  Digite o preco por tonelada (R$): ")

    dados = prod.registrar_producao(cultura, area, rendimento, preco)

    print(f"\n  --- Dados Salvos com Sucesso! ---")
    print(f"  Cultura          : {dados['cultura']}")
    print(f"  Area             : {dados['area']} ha")
    print(f"  Rendimento       : {dados['rendimento']} t/ha")
    print(f"  Producao Total   : {dados['producao_total']:.2f} t")
    print(f"  Preco por Ton    : R$ {dados['preco_tonelada']:.2f}")
    print(f"  Receita Total    : R$ {dados['receita_total']:.2f}")

    print("\n  Estrutura do dicionario salvo na lista:")
    print(" ", dados)

    arq.registrar_log(f"Registro adicionado: {dados['cultura']}, {dados['area']} ha.")


def tela_listar():
    print("\n" + "=" * 50)
    print("  PRODUCOES REGISTRADAS")
    print("=" * 50)

    tabela = prod.gerar_tabela()

    if len(tabela) == 1:
        print("  Nenhum registro encontrado.")
        return

    cabecalho = tabela[0]
    print("  " + "  ".join(str(c).ljust(18) for c in cabecalho))
    print("  " + "-" * 100)

    for linha in tabela[1:]:
        print("  " + "  ".join(str(c).ljust(18) for c in linha))

    total_area     = sum(p["area"]           for p in prod.producoes)
    total_producao = sum(p["producao_total"] for p in prod.producoes)
    total_receita  = sum(p["receita_total"]  for p in prod.producoes)

    print("\n  --- Resumo ---")
    print(f"  Registros      : {len(prod.producoes)}")
    print(f"  Area Total     : {total_area:.2f} ha")
    print(f"  Producao Total : {total_producao:.2f} t")
    print(f"  Receita Total  : R$ {total_receita:.2f}")


def tela_salvar_json():
    print("\n" + "=" * 50)
    print("  SALVAR EM JSON")
    print("=" * 50)

    arq.salvar_json(prod.producoes)
    print("  Dados salvos com sucesso!")


def tela_carregar_json():
    print("\n" + "=" * 50)
    print("  CARREGAR DO JSON")
    print("=" * 50)

    lista = arq.carregar_json()

    if not lista:
        print("  Nenhum dado encontrado no arquivo JSON.")
        return

    prod.carregar_dados(lista)
    print(f"  {len(lista)} registro(s) carregado(s).")


def tela_exportar_relatorio():
    print("\n" + "=" * 50)
    print("  EXPORTAR RELATORIO TXT")
    print("=" * 50)

    tabela  = prod.gerar_tabela()
    caminho = arq.exportar_relatorio(tabela, prod.producoes)
    print(f"  Relatorio exportado:\n  {caminho}")


def tela_banco():
    print("\n" + "=" * 50)
    print("  BANCO DE DADOS ORACLE")
    print("=" * 50)

    if not bco.ORACLE_DISPONIVEL:
        print("  Driver nao instalado. Execute: pip install oracledb")
        return

    print("  Testando conexao...")
    if not bco.testar_conexao():
        print("  Nao foi possivel conectar ao Oracle.")
        return

    print("  Conexao OK!")
    print("\n  1. Sincronizar dados para o Oracle")
    print("  2. Carregar dados do Oracle")
    print("  0. Voltar")

    opcao = input("\n  Opcao: ").strip()

    if opcao == "1":
        inseridos, erros = bco.sincronizar(prod.producoes)
        print(f"\n  Inseridos : {inseridos}")
        print(f"  Erros     : {erros}")
        arq.registrar_log(f"Sincronizacao Oracle: {inseridos} inseridos.")

    elif opcao == "2":
        lista = bco.buscar_producoes()
        if lista:
            prod.carregar_dados(lista)
            print(f"  {len(lista)} registro(s) carregado(s) do Oracle.")
        else:
            print("  Nenhum dado encontrado no banco.")


def tela_log():
    print("\n" + "=" * 50)
    print("  LOG DE OPERACOES")
    print("=" * 50)

    linhas = arq.ler_log(ultimas_n=15)
    if not linhas:
        print("  Log vazio.")
    for linha in linhas:
        print(f"  {linha}")


# -------------------------------------------------------
# MENU PRINCIPAL
# -------------------------------------------------------

def menu():
    arq.registrar_log("Sistema iniciado.")

    while True:
        limpar_tela()
        print("=" * 50)
        print("  SISTEMA DE PRODUCAO AGRICOLA")
        print("  Agronegocio em Python")
        print("=" * 50)
        print(f"  Registros em memoria: {len(prod.producoes)}")
        print("-" * 50)
        print("  1. Registrar producao")
        print("  2. Listar producoes")
        print("  3. Exportar relatorio (.txt)")
        print("  4. Salvar dados em JSON")
        print("  5. Carregar dados do JSON")
        print("  6. Banco de Dados Oracle")
        print("  7. Ver log de operacoes")
        print("  0. Sair")
        print("=" * 50)

        opcao = input("\n  Opcao: ").strip()

        if   opcao == "1": tela_registrar()
        elif opcao == "2": tela_listar()
        elif opcao == "3": tela_exportar_relatorio()
        elif opcao == "4": tela_salvar_json()
        elif opcao == "5": tela_carregar_json()
        elif opcao == "6": tela_banco()
        elif opcao == "7": tela_log()
        elif opcao == "0":
            print("\n  Encerrando o sistema...")
            arq.registrar_log("Sistema encerrado.")
            break
        else:
            print("  Opcao invalida.")

        pausar()


if __name__ == "__main__":
    menu()
