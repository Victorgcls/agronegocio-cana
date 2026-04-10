# -*- coding: utf-8 -*-

try:
    import oracledb
    ORACLE_DISPONIVEL = True
except ImportError:
    ORACLE_DISPONIVEL = False

import config


def conectar():
    if not ORACLE_DISPONIVEL:
        raise RuntimeError("Driver nao instalado. Execute: pip install oracledb")
    conexao = oracledb.connect(
        user=config.ORACLE_USER,
        password=config.ORACLE_PASSWORD,
        dsn=config.ORACLE_DSN,
    )
    return conexao


def testar_conexao():
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM DUAL")
        return True
    except Exception as e:
        print(f"  [Banco] Falha na conexao: {e}")
        return False


def sincronizar(producoes):
    inseridos = 0
    erros     = 0

    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM producoes")

                for p in producoes:
                    try:
                        cur.execute(
                            "INSERT INTO producoes (cultura, area, rendimento, producao_total, preco_tonelada, receita_total) "
                            "VALUES (:1, :2, :3, :4, :5, :6)",
                            (
                                p["cultura"],
                                p["area"],
                                p["rendimento"],
                                p["producao_total"],
                                p["preco_tonelada"],
                                p["receita_total"],
                            ),
                        )
                        inseridos += 1
                    except Exception:
                        erros += 1

            conn.commit()
    except Exception as e:
        print(f"  [Banco] Erro na sincronizacao: {e}")

    return inseridos, erros


def buscar_producoes():
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT cultura, area, rendimento, producao_total, preco_tonelada, receita_total "
                    "FROM producoes"
                )
                rows = cur.fetchall()

        lista = []
        for r in rows:
            lista.append({
                "cultura":        r[0],
                "area":           float(r[1]),
                "rendimento":     float(r[2]),
                "producao_total": float(r[3]),
                "preco_tonelada": float(r[4]),
                "receita_total":  float(r[5]),
            })
        return lista

    except Exception as e:
        print(f"  [Banco] Erro ao buscar dados: {e}")
        return []
