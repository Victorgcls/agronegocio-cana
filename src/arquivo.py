import json
import os
from datetime import datetime

PASTA_DADOS  = os.path.join(os.path.dirname(__file__), "dados")
ARQUIVO_JSON = os.path.join(PASTA_DADOS, "colheitas.json")
ARQUIVO_RELAT = os.path.join(PASTA_DADOS, "relatorio.txt")
ARQUIVO_LOG  = os.path.join(PASTA_DADOS, "log_operacoes.txt")


def _garantir_pasta():
    os.makedirs(PASTA_DADOS, exist_ok=True)


def salvar_json(talhoes, colheitas):
    _garantir_pasta()
    dados = {
        "exportado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "talhoes":      talhoes,
        "colheitas":    colheitas,
    }
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    registrar_log(f"Dados salvos em JSON: {len(talhoes)} talhão(ões), {len(colheitas)} colheita(s).")


def carregar_json():
    if not os.path.exists(ARQUIVO_JSON):
        return ([], [])

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        talhoes   = dados.get("talhoes",   [])
        colheitas = dados.get("colheitas", [])
        registrar_log(f"Dados carregados do JSON: {len(talhoes)} talhão(ões), {len(colheitas)} colheita(s).")
        return (talhoes, colheitas)
    except (json.JSONDecodeError, KeyError) as erro:
        registrar_log(f"ERRO ao carregar JSON: {erro}")
        return ([], [])


def exportar_relatorio_txt(tabela, resumos):
    _garantir_pasta()

    linha_sep = "=" * 90
    linha_div = "-" * 90

    with open(ARQUIVO_RELAT, "w", encoding="utf-8") as arq:
        arq.write(linha_sep + "\n")
        arq.write("  RELATÓRIO DE COLHEITA DE CANA-DE-AÇÚCAR\n")
        arq.write(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        arq.write(linha_sep + "\n\n")

        if len(tabela) > 1:
            arq.write("DETALHAMENTO DAS COLHEITAS\n")
            arq.write(linha_div + "\n")
            arq.write(_formatar_linha_tabela(tabela[0]) + "\n")
            arq.write(linha_div + "\n")
            for linha in tabela[1:]:
                arq.write(_formatar_linha_tabela([str(c) for c in linha]) + "\n")
        else:
            arq.write("Nenhuma colheita registrada.\n")

        arq.write("\n")
        arq.write(linha_sep + "\n")
        arq.write("PRODUTIVIDADE POR TALHÃO\n")
        arq.write(linha_sep + "\n")

        for r in resumos:
            arq.write(f"\nTalhão : {r['talhao']}\n")
            arq.write(f"  Área           : {r['area_ha']} ha\n")
            arq.write(f"  Colheitas      : {r['total_colheitas']}\n")
            arq.write(f"  Prod. Bruta    : {r['producao_bruta_ton']} t\n")
            arq.write(f"  Perda Total    : {r['perda_total_ton']} t\n")
            arq.write(f"  Prod. Líquida  : {r['producao_liquida_ton']} t\n")
            arq.write(f"  Produtividade  : {r['produtividade_t_ha']} t/ha\n")
            arq.write(linha_div + "\n")

        arq.write("\nFim do relatório.\n")

    registrar_log(f"Relatório TXT exportado para: {ARQUIVO_RELAT}")
    return ARQUIVO_RELAT


def _formatar_linha_tabela(colunas):
    larguras = [5, 16, 12, 10, 16, 12, 17, 9]
    linha = ""
    for i, col in enumerate(colunas):
        larg = larguras[i] if i < len(larguras) else 12
        linha += str(col).ljust(larg)
    return linha


def registrar_log(mensagem):
    _garantir_pasta()
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arq:
        arq.write(f"[{timestamp}] {mensagem}\n")


def ler_log(ultimas_n=10):
    if not os.path.exists(ARQUIVO_LOG):
        return []
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as arq:
        linhas = arq.readlines()
    return [l.rstrip() for l in linhas[-ultimas_n:]]
