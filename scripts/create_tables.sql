CREATE TABLE talhoes (
    id         NUMBER        PRIMARY KEY,
    nome       VARCHAR2(100) NOT NULL,
    area_ha    NUMBER(10,2)  NOT NULL,
    variedade  VARCHAR2(50)  NOT NULL
);

CREATE TABLE colheitas (
    id                    NUMBER        PRIMARY KEY,
    id_talhao             NUMBER        NOT NULL,
    data_colheita         VARCHAR2(10)  NOT NULL,
    producao_bruta_ton    NUMBER(10,2)  NOT NULL,
    tipo_colheita         VARCHAR2(20)  NOT NULL,
    perda_percentual      NUMBER(5,2)   NOT NULL,
    perda_ton             NUMBER(10,2)  NOT NULL,
    producao_liquida_ton  NUMBER(10,2)  NOT NULL,
    CONSTRAINT fk_talhao FOREIGN KEY (id_talhao) REFERENCES talhoes(id)
);
