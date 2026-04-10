from datetime import datetime

TIPOS_COLHEITA = ("Manual", "Mecanica")

VARIEDADES_CANA = (
    "RB867515",
    "CTC4",
    "SP803280",
    "RB92579",
    "CTC9001",
    "RB966928",
    "Outra",
)

PERDA_REFERENCIA = {
    "Manual":   5.0,
    "Mecanica": 15.0,
}

talhoes = []
colheitas = []


def proximo_id(lista):
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


def buscar_talhao(id_talhao):
    for talhao in talhoes:
        if talhao["id"] == id_talhao:
            return talhao
    return None


def buscar_colheita(id_colheita):
    for colheita in colheitas:
        if colheita["id"] == id_colheita:
            return colheita
    return None


def calcular_perda(producao_bruta, tipo_colheita):
    percentual = PERDA_REFERENCIA.get(tipo_colheita, 0.0)
    perda_ton  = round(producao_bruta * (percentual / 100), 2)
    liquida    = round(producao_bruta - perda_ton, 2)
    return (percentual, perda_ton, liquida)


def calcular_produtividade_talhao(id_talhao):
    talhao = buscar_talhao(id_talhao)
    if talhao is None:
        raise ValueError(f"Talhão ID {id_talhao} não encontrado.")

    registros = [c for c in colheitas if c["id_talhao"] == id_talhao]

    if not registros:
        return {
            "talhao": talhao["nome"],
            "area_ha": talhao["area_ha"],
            "total_colheitas": 0,
            "producao_bruta_ton": 0.0,
            "perda_total_ton": 0.0,
            "producao_liquida_ton": 0.0,
            "produtividade_t_ha": 0.0,
        }

    prod_bruta  = sum(c["producao_bruta_ton"]   for c in registros)
    perda_total = sum(c["perda_ton"]             for c in registros)
    prod_liq    = sum(c["producao_liquida_ton"]  for c in registros)

    return {
        "talhao":               talhao["nome"],
        "area_ha":              talhao["area_ha"],
        "total_colheitas":      len(registros),
        "producao_bruta_ton":   round(prod_bruta,  2),
        "perda_total_ton":      round(perda_total, 2),
        "producao_liquida_ton": round(prod_liq,    2),
        "produtividade_t_ha":   round(prod_liq / talhao["area_ha"], 2),
    }


def gerar_tabela_colheitas():
    cabecalho = [
        "ID", "Talhão", "Data", "Tipo",
        "Prod. Bruta (t)", "Perda (t)", "Prod. Líquida (t)", "% Perda"
    ]
    tabela = [cabecalho]

    for c in colheitas:
        talhao   = buscar_talhao(c["id_talhao"])
        nome_tal = talhao["nome"] if talhao else "N/A"
        linha = [
            c["id"],
            nome_tal,
            c["data"],
            c["tipo_colheita"],
            c["producao_bruta_ton"],
            c["perda_ton"],
            c["producao_liquida_ton"],
            f'{c["perda_percentual"]:.1f}%',
        ]
        tabela.append(linha)

    return tabela


def cadastrar_talhao(nome, area_ha, variedade):
    novo_id = proximo_id(talhoes)
    talhao  = {
        "id":        novo_id,
        "nome":      nome.strip(),
        "area_ha":   area_ha,
        "variedade": variedade,
    }
    talhoes.append(talhao)
    return talhao


def registrar_colheita(id_talhao, data, producao_bruta_ton, tipo_colheita):
    if buscar_talhao(id_talhao) is None:
        raise ValueError(f"Talhão ID {id_talhao} não encontrado.")
    if tipo_colheita not in TIPOS_COLHEITA:
        raise ValueError(f"Tipo inválido. Use: {TIPOS_COLHEITA}")

    percentual, perda_ton, prod_liq = calcular_perda(producao_bruta_ton, tipo_colheita)

    novo_id  = proximo_id(colheitas)
    colheita = {
        "id":                   novo_id,
        "id_talhao":            id_talhao,
        "data":                 data,
        "producao_bruta_ton":   producao_bruta_ton,
        "tipo_colheita":        tipo_colheita,
        "perda_percentual":     percentual,
        "perda_ton":            perda_ton,
        "producao_liquida_ton": prod_liq,
    }
    colheitas.append(colheita)
    return colheita


def remover_colheita(id_colheita):
    for i, c in enumerate(colheitas):
        if c["id"] == id_colheita:
            colheitas.pop(i)
            return True
    return False


def carregar_dados(lista_talhoes, lista_colheitas):
    talhoes.clear()
    talhoes.extend(lista_talhoes)
    colheitas.clear()
    colheitas.extend(lista_colheitas)
