CREATE TABLE producoes (
    id             NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cultura        VARCHAR2(50)  NOT NULL,
    area           NUMBER(10,2)  NOT NULL,
    rendimento     NUMBER(10,2)  NOT NULL,
    producao_total NUMBER(10,2)  NOT NULL,
    preco_tonelada NUMBER(10,2)  NOT NULL,
    receita_total  NUMBER(12,2)  NOT NULL
);
