import os
from datetime import datetime

import colheita as col
import arquivo  as arq
import banco    as bco


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\n  Pressione ENTER para continuar...")


def titulo(texto):
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)


def erro(texto):
    print(f"\n  [!] {texto}")


def ok(texto):
    print(f"\n  [OK] {texto}")


def ler_inteiro(prompt, minimo=None, maximo=None):
    while True:
        entrada = input(prompt).strip()
        if not entrada.lstrip("-").isdigit():
            erro("Entrada inválida. Digite um número inteiro.")
            continue
        valor = int(entrada)
        if minimo is not None and valor < minimo:
            erro(f"O valor mínimo permitido é {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            erro(f"O valor máximo permitido é {maximo}.")
            continue
        return valor


def ler_float(prompt, minimo=0.0):
    while True:
        entrada = input(prompt).strip().replace(",", ".")
        try:
            valor = float(entrada)
        except ValueError:
            erro("Entrada inválida. Digite um número (ex: 123.45).")
            continue
        if valor < minimo:
            erro(f"O valor deve ser maior ou igual a {minimo}.")
            continue
        return valor


def ler_texto(prompt, minimo_chars=1):
    while True:
        entrada = input(prompt).strip()
        if len(entrada) < minimo_chars:
            erro(f"O campo deve ter pelo menos {minimo_chars} caractere(s).")
            continue
        return entrada


def ler_data(prompt):
    while True:
        entrada = input(prompt).strip()
        try:
            datetime.strptime(entrada, "%d/%m/%Y")
            return entrada
        except ValueError:
            erro("Data inválida. Use o formato DD/MM/AAAA (ex: 15/03/2024).")


def ler_opcao_lista(prompt, opcoes):
    print(f"\n  {prompt}")
    for i, op in enumerate(opcoes, start=1):
        print(f"    {i}. {op}")
    escolha = ler_inteiro("  Opção: ", minimo=1, maximo=len(opcoes))
    return opcoes[escolha - 1]


def tela_cadastrar_talhao():
    titulo("CADASTRAR TALHÃO")

    nome      = ler_texto("  Nome do talhão  : ", minimo_chars=2)
    area      = ler_float("  Área (ha)        : ", minimo=0.01)
    variedade = ler_opcao_lista("Variedade da cana :", col.VARIEDADES_CANA)

    talhao = col.cadastrar_talhao(nome, area, variedade)
    ok(f"Talhão '{talhao['nome']}' cadastrado com ID {talhao['id']}.")
    arq.registrar_log(f"Talhão cadastrado: ID={talhao['id']}, nome={talhao['nome']}")


def tela_listar_talhoes():
    titulo("TALHÕES CADASTRADOS")

    if not col.talhoes:
        print("  Nenhum talhão cadastrado.")
        return

    print(f"  {'ID':<5} {'Nome':<20} {'Área (ha)':<12} {'Variedade'}")
    print("  " + "-" * 55)
    for t in col.talhoes:
        print(f"  {t['id']:<5} {t['nome']:<20} {t['area_ha']:<12} {t['variedade']}")


def tela_consultar_talhao():
    titulo("CONSULTAR TALHÃO")

    if not col.talhoes:
        print("  Nenhum talhão cadastrado.")
        return

    id_tal = ler_inteiro("  ID do talhão: ", minimo=1)
    talhao = col.buscar_talhao(id_tal)

    if talhao is None:
        erro(f"Talhão ID {id_tal} não encontrado.")
        return

    print(f"\n  ID        : {talhao['id']}")
    print(f"  Nome      : {talhao['nome']}")
    print(f"  Área      : {talhao['area_ha']} ha")
    print(f"  Variedade : {talhao['variedade']}")

    prod = col.calcular_produtividade_talhao(id_tal)
    print(f"\n  --- Produtividade acumulada ---")
    print(f"  Colheitas registradas : {prod['total_colheitas']}")
    print(f"  Produção bruta total  : {prod['producao_bruta_ton']} t")
    print(f"  Perda total estimada  : {prod['perda_total_ton']} t")
    print(f"  Produção líquida      : {prod['producao_liquida_ton']} t")
    print(f"  Produtividade         : {prod['produtividade_t_ha']} t/ha")


def tela_registrar_colheita():
    titulo("REGISTRAR COLHEITA")

    if not col.talhoes:
        erro("Cadastre pelo menos um talhão antes de registrar uma colheita.")
        return

    tela_listar_talhoes()
    id_tal = ler_inteiro("\n  ID do talhão colhido : ", minimo=1)

    if col.buscar_talhao(id_tal) is None:
        erro(f"Talhão ID {id_tal} não encontrado.")
        return

    data     = ler_data("  Data da colheita (DD/MM/AAAA): ")
    producao = ler_float("  Produção bruta (toneladas)   : ", minimo=0.01)
    tipo     = ler_opcao_lista("Tipo de colheita:", col.TIPOS_COLHEITA)

    try:
        registro = col.registrar_colheita(id_tal, data, producao, tipo)
    except ValueError as e:
        erro(str(e))
        return

    print(f"\n  Colheita registrada com sucesso!")
    print(f"  ID da colheita         : {registro['id']}")
    print(f"  Tipo                   : {registro['tipo_colheita']}")
    print(f"  Produção bruta         : {registro['producao_bruta_ton']} t")
    print(f"  Perda estimada ({registro['perda_percentual']:.0f}%)  : {registro['perda_ton']} t")
    print(f"  Produção líquida       : {registro['producao_liquida_ton']} t")

    arq.registrar_log(
        f"Colheita registrada: ID={registro['id']}, "
        f"Talhão={id_tal}, {tipo}, {producao}t"
    )


def tela_listar_colheitas():
    titulo("COLHEITAS REGISTRADAS")

    tabela = col.gerar_tabela_colheitas()

    if len(tabela) == 1:
        print("  Nenhuma colheita registrada.")
        return

    cabecalho = tabela[0]
    larguras  = [5, 16, 12, 10, 16, 12, 17, 9]

    linha_cab = "  "
    for i, col_nome in enumerate(cabecalho):
        larg = larguras[i] if i < len(larguras) else 12
        linha_cab += str(col_nome).ljust(larg)
    print(linha_cab)
    print("  " + "-" * 100)

    for linha in tabela[1:]:
        linha_fmt = "  "
        for i, cel in enumerate(linha):
            larg = larguras[i] if i < len(larguras) else 12
            linha_fmt += str(cel).ljust(larg)
        print(linha_fmt)


def tela_remover_colheita():
    titulo("REMOVER COLHEITA")

    if not col.colheitas:
        print("  Nenhuma colheita registrada.")
        return

    tela_listar_colheitas()
    id_col = ler_inteiro("\n  ID da colheita a remover: ", minimo=1)

    confirmacao = input(f"  Confirma remoção da colheita {id_col}? (s/N): ").strip().lower()
    if confirmacao != "s":
        print("  Operação cancelada.")
        return

    if col.remover_colheita(id_col):
        ok(f"Colheita ID {id_col} removida.")
        arq.registrar_log(f"Colheita removida: ID={id_col}")
    else:
        erro(f"Colheita ID {id_col} não encontrada.")


def tela_relatorio_perdas():
    titulo("RELATÓRIO DE PERDAS")

    if not col.colheitas:
        print("  Nenhuma colheita registrada.")
        return

    total_bruta = sum(c["producao_bruta_ton"]  for c in col.colheitas)
    total_perda = sum(c["perda_ton"]            for c in col.colheitas)
    total_liq   = sum(c["producao_liquida_ton"] for c in col.colheitas)

    mecanicas = [c for c in col.colheitas if c["tipo_colheita"] == "Mecanica"]
    manuais   = [c for c in col.colheitas if c["tipo_colheita"] == "Manual"]

    print(f"\n  Total de colheitas      : {len(col.colheitas)}")
    print(f"  Colheitas mecânicas     : {len(mecanicas)}")
    print(f"  Colheitas manuais       : {len(manuais)}")
    print(f"\n  Produção bruta total    : {total_bruta:.2f} t")
    print(f"  Perda total estimada    : {total_perda:.2f} t")
    print(f"  Produção líquida total  : {total_liq:.2f} t")

    if total_bruta > 0:
        pct_geral = (total_perda / total_bruta) * 100
        print(f"  Percentual de perda     : {pct_geral:.2f}%")

        economia = total_bruta * (0.15 - (total_perda / total_bruta))
        if economia > 0:
            print(f"\n  [Dica] Migrar para colheita manual poderia reduzir perdas")
            print(f"         em aproximadamente {economia:.2f} t neste ciclo.")


def tela_produtividade():
    titulo("PRODUTIVIDADE POR TALHÃO")

    if not col.talhoes:
        print("  Nenhum talhão cadastrado.")
        return

    for t in col.talhoes:
        prod = col.calcular_produtividade_talhao(t["id"])
        print(f"\n  Talhão: {prod['talhao']}  |  {prod['area_ha']} ha  |  Var.: {t['variedade']}")
        print(f"    Colheitas     : {prod['total_colheitas']}")
        print(f"    Prod. Bruta   : {prod['producao_bruta_ton']} t")
        print(f"    Perda Total   : {prod['perda_total_ton']} t")
        print(f"    Prod. Líquida : {prod['producao_liquida_ton']} t")
        print(f"    Produtividade : {prod['produtividade_t_ha']} t/ha")
        print("    " + "-" * 40)


def tela_exportar_relatorio():
    titulo("EXPORTAR RELATÓRIO TXT")

    tabela  = col.gerar_tabela_colheitas()
    resumos = [col.calcular_produtividade_talhao(t["id"]) for t in col.talhoes]

    caminho = arq.exportar_relatorio_txt(tabela, resumos)
    ok(f"Relatório exportado:\n  {caminho}")


def tela_salvar_json():
    titulo("SALVAR DADOS EM JSON")
    arq.salvar_json(col.talhoes, col.colheitas)
    ok("Dados salvos com sucesso no arquivo JSON.")


def tela_carregar_json():
    titulo("CARREGAR DADOS DO JSON")
    talhoes_json, colheitas_json = arq.carregar_json()

    if not talhoes_json and not colheitas_json:
        erro("Nenhum dado encontrado no arquivo JSON.")
        return

    col.carregar_dados(talhoes_json, colheitas_json)
    ok(f"Carregados: {len(col.talhoes)} talhão(ões) e {len(col.colheitas)} colheita(s).")


def tela_sincronizar_oracle():
    titulo("SINCRONIZAR COM ORACLE")

    if not bco.ORACLE_DISPONIVEL:
        erro("Driver 'oracledb' não instalado.\n  Execute no terminal: pip install oracledb")
        return

    print("  Testando conexão com o banco...")
    if not bco.testar_conexao():
        erro("Não foi possível conectar ao Oracle. Verifique as configurações em banco.py.")
        return

    ok("Conexão estabelecida.")
    resultado = bco.sincronizar_tudo(col.talhoes, col.colheitas)

    print(f"\n  Talhões inseridos  : {resultado['talhoes_ok']}")
    print(f"  Talhões c/ erro    : {resultado['talhoes_err']}")
    print(f"  Colheitas inseridas: {resultado['colheitas_ok']}")
    print(f"  Colheitas c/ erro  : {resultado['colheitas_err']}")

    arq.registrar_log(
        f"Sincronização Oracle: {resultado['talhoes_ok']} talhões, "
        f"{resultado['colheitas_ok']} colheitas."
    )


def tela_carregar_oracle():
    titulo("CARREGAR DADOS DO ORACLE")

    if not bco.ORACLE_DISPONIVEL:
        erro("Driver 'oracledb' não instalado.")
        return

    if not bco.testar_conexao():
        erro("Não foi possível conectar ao Oracle.")
        return

    tals = bco.buscar_talhoes_banco()
    cols = bco.buscar_colheitas_banco()
    col.carregar_dados(tals, cols)
    ok(f"Carregados do Oracle: {len(tals)} talhão(ões) e {len(cols)} colheita(s).")


def tela_ver_log():
    titulo("LOG DE OPERAÇÕES (últimas 15 entradas)")
    linhas = arq.ler_log(ultimas_n=15)
    if not linhas:
        print("  Log vazio.")
    for linha in linhas:
        print(f"  {linha}")


def menu_talhoes():
    while True:
        titulo("GERENCIAR TALHÕES")
        print("  1. Cadastrar talhão")
        print("  2. Listar talhões")
        print("  3. Consultar talhão / produtividade")
        print("  0. Voltar")

        op = ler_inteiro("\n  Opção: ", minimo=0, maximo=3)

        if   op == 1: tela_cadastrar_talhao()
        elif op == 2: tela_listar_talhoes()
        elif op == 3: tela_consultar_talhao()
        elif op == 0: break

        pausar()


def menu_colheitas():
    while True:
        titulo("GERENCIAR COLHEITAS")
        print("  1. Registrar colheita")
        print("  2. Listar colheitas")
        print("  3. Remover colheita")
        print("  0. Voltar")

        op = ler_inteiro("\n  Opção: ", minimo=0, maximo=3)

        if   op == 1: tela_registrar_colheita()
        elif op == 2: tela_listar_colheitas()
        elif op == 3: tela_remover_colheita()
        elif op == 0: break

        pausar()


def menu_relatorios():
    while True:
        titulo("RELATÓRIOS")
        print("  1. Relatório de perdas")
        print("  2. Produtividade por talhão")
        print("  3. Exportar relatório (.txt)")
        print("  0. Voltar")

        op = ler_inteiro("\n  Opção: ", minimo=0, maximo=3)

        if   op == 1: tela_relatorio_perdas()
        elif op == 2: tela_produtividade()
        elif op == 3: tela_exportar_relatorio()
        elif op == 0: break

        pausar()


def menu_banco():
    while True:
        titulo("BANCO DE DADOS ORACLE")
        print("  1. Sincronizar dados para o Oracle")
        print("  2. Carregar dados do Oracle")
        print("  0. Voltar")

        op = ler_inteiro("\n  Opção: ", minimo=0, maximo=2)

        if   op == 1: tela_sincronizar_oracle()
        elif op == 2: tela_carregar_oracle()
        elif op == 0: break

        pausar()


def menu_principal():
    arq.registrar_log("Sistema iniciado.")

    while True:
        limpar_tela()
        print("=" * 60)
        print("   SISTEMA DE GESTÃO DE COLHEITA DE CANA-DE-AÇÚCAR")
        print("   Agronegócio — Redução de Perdas na Colheita")
        print("=" * 60)
        print(f"  Talhões em memória  : {len(col.talhoes)}")
        print(f"  Colheitas em memória: {len(col.colheitas)}")
        print("-" * 60)
        print("  1. Gerenciar Talhões")
        print("  2. Gerenciar Colheitas")
        print("  3. Relatórios")
        print("  4. Banco de Dados Oracle")
        print("  5. Salvar dados em JSON")
        print("  6. Carregar dados do JSON")
        print("  7. Ver log de operações")
        print("  0. Sair")
        print("=" * 60)

        op = ler_inteiro("\n  Opção: ", minimo=0, maximo=7)

        if   op == 1: menu_talhoes()
        elif op == 2: menu_colheitas()
        elif op == 3: menu_relatorios()
        elif op == 4: menu_banco()
        elif op == 5:
            tela_salvar_json()
            pausar()
        elif op == 6:
            tela_carregar_json()
            pausar()
        elif op == 7:
            tela_ver_log()
            pausar()
        elif op == 0:
            print("\n  Encerrando o sistema...")
            arq.registrar_log("Sistema encerrado.")
            break


if __name__ == "__main__":
    menu_principal()
