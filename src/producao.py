# -*- coding: utf-8 -*-

culturas = ("Soja", "Milho", "Cafe", "Cana")

rendimento_medio = {
    "Soja":  3.5,
    "Milho": 6.0,
    "Cafe":  1.5,
    "Cana":  80.0,
}

producoes = []


def calcular_producao(area, rendimento):
    producao = area * rendimento
    return producao


def calcular_receita(producao_total, preco_tonelada):
    receita = producao_total * preco_tonelada
    return receita


def registrar_producao(cultura, area, rendimento, preco):
    total  = calcular_producao(area, rendimento)
    receita = calcular_receita(total, preco)

    dados = {
        "cultura":        cultura,
        "area":           area,
        "rendimento":     rendimento,
        "producao_total": round(total,   2),
        "preco_tonelada": preco,
        "receita_total":  round(receita, 2),
    }

    producoes.append(dados)
    return dados


def gerar_tabela():
    cabecalho = ["Cultura", "Area (ha)", "Rendimento (t/ha)", "Producao (t)", "Preco (R$/t)", "Receita (R$)"]
    tabela = [cabecalho]

    for p in producoes:
        linha = [
            p["cultura"],
            p["area"],
            p["rendimento"],
            p["producao_total"],
            p["preco_tonelada"],
            p["receita_total"],
        ]
        tabela.append(linha)

    return tabela


def carregar_dados(lista):
    producoes.clear()
    producoes.extend(lista)
