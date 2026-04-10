# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

PASTA_DADOS   = os.path.join(os.path.dirname(__file__), "dados")
ARQUIVO_JSON  = os.path.join(PASTA_DADOS, "producoes.json")
ARQUIVO_RELAT = os.path.join(PASTA_DADOS, "relatorio.txt")
ARQUIVO_LOG   = os.path.join(PASTA_DADOS, "log.txt")


def garantir_pasta():
    os.makedirs(PASTA_DADOS, exist_ok=True)


def salvar_json(producoes):
    garantir_pasta()

    dados = {
        "salvo_em":  datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "producoes": producoes,
    }

    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    registrar_log(f"Dados salvos: {len(producoes)} registro(s).")


def carregar_json():
    if not os.path.exists(ARQUIVO_JSON):
        return []

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        lista = dados.get("producoes", [])
        registrar_log(f"Dados carregados: {len(lista)} registro(s).")
        return lista

    except Exception as e:
        registrar_log(f"Erro ao carregar JSON: {e}")
        return []


def exportar_relatorio(tabela, producoes):
    garantir_pasta()

    with open(ARQUIVO_RELAT, "w", encoding="utf-8") as arq:
        arq.write("=" * 70 + "\n")
        arq.write("  RELATORIO DE PRODUCAO AGRICOLA\n")
        arq.write(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        arq.write("=" * 70 + "\n\n")

        if len(tabela) > 1:
            cabecalho = tabela[0]
            arq.write("  ".join(str(c).ljust(18) for c in cabecalho) + "\n")
            arq.write("-" * 70 + "\n")

            for linha in tabela[1:]:
                arq.write("  ".join(str(c).ljust(18) for c in linha) + "\n")
        else:
            arq.write("Nenhum registro encontrado.\n")

        arq.write("\n" + "=" * 70 + "\n")
        arq.write("RESUMO\n")
        arq.write("=" * 70 + "\n")

        if producoes:
            total_area     = sum(p["area"]           for p in producoes)
            total_producao = sum(p["producao_total"] for p in producoes)
            total_receita  = sum(p["receita_total"]  for p in producoes)

            arq.write(f"  Total de registros : {len(producoes)}\n")
            arq.write(f"  Area total         : {total_area:.2f} ha\n")
            arq.write(f"  Producao total     : {total_producao:.2f} t\n")
            arq.write(f"  Receita total      : R$ {total_receita:.2f}\n")

        arq.write("\nFim do relatorio.\n")

    registrar_log(f"Relatorio exportado.")
    return ARQUIVO_RELAT


def registrar_log(mensagem):
    garantir_pasta()
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as arq:
        arq.write(f"[{timestamp}] {mensagem}\n")


def ler_log(ultimas_n=10):
    if not os.path.exists(ARQUIVO_LOG):
        return []
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as arq:
        linhas = arq.readlines()
    return [l.rstrip() for l in linhas[-ultimas_n:]]
