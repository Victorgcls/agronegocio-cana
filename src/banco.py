try:
    import oracledb
    ORACLE_DISPONIVEL = True
except ImportError:
    ORACLE_DISPONIVEL = False

import config


def _conectar():
    if not ORACLE_DISPONIVEL:
        raise RuntimeError("Driver 'oracledb' não instalado. Execute: pip install oracledb")
    conexao = oracledb.connect(
        user=config.ORACLE_USER,
        password=config.ORACLE_PASSWORD,
        dsn=config.ORACLE_DSN,
    )
    return conexao


def inserir_talhao(talhao):
    sql = """
        INSERT INTO talhoes (id, nome, area_ha, variedade)
        VALUES (:id, :nome, :area_ha, :variedade)
    """
    try:
        with _conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, {
                    "id":        talhao["id"],
                    "nome":      talhao["nome"],
                    "area_ha":   talhao["area_ha"],
                    "variedade": talhao["variedade"],
                })
            conn.commit()
        return True
    except Exception as e:
        print(f"  [Banco] Erro ao inserir talhao: {e}")
        return False


def inserir_colheita(colheita):
    sql = """
        INSERT INTO colheitas (
            id, id_talhao, data_colheita, producao_bruta_ton,
            tipo_colheita, perda_percentual, perda_ton, producao_liquida_ton
        ) VALUES (
            :id, :id_talhao, :data_colheita, :producao_bruta_ton,
            :tipo_colheita, :perda_percentual, :perda_ton, :producao_liquida_ton
        )
    """
    try:
        with _conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, {
                    "id":                   colheita["id"],
                    "id_talhao":            colheita["id_talhao"],
                    "data_colheita":        colheita["data"],
                    "producao_bruta_ton":   colheita["producao_bruta_ton"],
                    "tipo_colheita":        colheita["tipo_colheita"],
                    "perda_percentual":     colheita["perda_percentual"],
                    "perda_ton":            colheita["perda_ton"],
                    "producao_liquida_ton": colheita["producao_liquida_ton"],
                })
            conn.commit()
        return True
    except Exception as e:
        print(f"  [Banco] Erro ao inserir colheita: {e}")
        return False


def sincronizar_tudo(talhoes, colheitas):
    resultado = {"talhoes_ok": 0, "talhoes_err": 0,
                 "colheitas_ok": 0, "colheitas_err": 0}

    try:
        with _conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM colheitas")
                cur.execute("DELETE FROM talhoes")

                for t in talhoes:
                    try:
                        cur.execute(
                            "INSERT INTO talhoes (id, nome, area_ha, variedade) "
                            "VALUES (:1, :2, :3, :4)",
                            (t["id"], t["nome"], t["area_ha"], t["variedade"]),
                        )
                        resultado["talhoes_ok"] += 1
                    except Exception:
                        resultado["talhoes_err"] += 1

                for c in colheitas:
                    try:
                        cur.execute(
                            "INSERT INTO colheitas (id, id_talhao, data_colheita, "
                            "producao_bruta_ton, tipo_colheita, perda_percentual, "
                            "perda_ton, producao_liquida_ton) "
                            "VALUES (:1, :2, :3, :4, :5, :6, :7, :8)",
                            (
                                c["id"], c["id_talhao"], c["data"],
                                c["producao_bruta_ton"], c["tipo_colheita"],
                                c["perda_percentual"], c["perda_ton"],
                                c["producao_liquida_ton"],
                            ),
                        )
                        resultado["colheitas_ok"] += 1
                    except Exception:
                        resultado["colheitas_err"] += 1

            conn.commit()
    except Exception as e:
        print(f"  [Banco] Erro na sincronização: {e}")

    return resultado


def buscar_talhoes_banco():
    try:
        with _conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nome, area_ha, variedade FROM talhoes ORDER BY id")
                rows = cur.fetchall()
        return [
            {"id": r[0], "nome": r[1], "area_ha": float(r[2]), "variedade": r[3]}
            for r in rows
        ]
    except Exception as e:
        print(f"  [Banco] Erro ao buscar talhões: {e}")
        return []


def buscar_colheitas_banco():
    try:
        with _conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, id_talhao, data_colheita, producao_bruta_ton, "
                    "tipo_colheita, perda_percentual, perda_ton, producao_liquida_ton "
                    "FROM colheitas ORDER BY id"
                )
                rows = cur.fetchall()
        return [
            {
                "id":                   r[0],
                "id_talhao":            r[1],
                "data":                 r[2],
                "producao_bruta_ton":   float(r[3]),
                "tipo_colheita":        r[4],
                "perda_percentual":     float(r[5]),
                "perda_ton":            float(r[6]),
                "producao_liquida_ton": float(r[7]),
            }
            for r in rows
        ]
    except Exception as e:
        print(f"  [Banco] Erro ao buscar colheitas: {e}")
        return []


def testar_conexao():
    try:
        with _conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM DUAL")
        return True
    except Exception as e:
        print(f"  [Banco] Falha na conexão: {e}")
        return False
