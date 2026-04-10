# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Sistema de Producao Agricola

## Gestao do Agronegocio em Python

## 👨‍🎓 Integrantes:
- João Victor do Nascimento Gonçalves

## 👩‍🏫 Professores:
### Tutor(a)
- Nicolly Candida Rodrigues de Souza
### Coordenador(a)
- Andre Godoi Chiovato

---

## 📜 Descrição

O agronegocio e um dos setores que mais gera empregos e riqueza no Brasil. Para que o produtor rural tome boas decisoes, e fundamental ter controle sobre o que planta, o quanto produz e qual e o retorno financeiro de cada cultura.

Este projeto e um sistema de gestao de producao agricola desenvolvido em Python, onde o usuario pode registrar producoes de diferentes culturas (Soja, Milho, Cafe e Cana), informando a area plantada e o preco por tonelada. O sistema calcula automaticamente a producao estimada e a receita total, e permite salvar, carregar e exportar esses dados.

O projeto aplica os conteudos dos **capitulos 3 ao 6** da disciplina:

| Capitulo | Conteudo | Aplicacao no projeto |
|----------|----------|----------------------|
| 3 | Funcoes com parametros | `calcular_producao()`, `calcular_receita()`, `ler_float()` |
| 3 | Procedimentos com parametros | `registrar_producao()`, `carregar_dados()` |
| 4 | Lista | `producoes` — lista de dicionarios em memoria |
| 4 | Tupla | `culturas` com as opcoes disponiveis |
| 4 | Dicionario | cada registro de producao e um dicionario |
| 4 | Tabela de memoria | `gerar_tabela()` retorna uma lista de listas |
| 5 | Arquivo JSON | `salvar_json()` e `carregar_json()` em `arquivo.py` |
| 5 | Arquivo texto | `exportar_relatorio()` e `registrar_log()` em `arquivo.py` |
| 6 | Banco Oracle | funcoes de `banco.py` usando `oracledb` |

---

## 📁 Estrutura de pastas

```
agronegocio-cana/
├── assets/
│   └── logo-fiap.png
├── config/
│   └── config.exemplo.py       — modelo de configuracao do banco
├── document/
├── scripts/
│   └── create_tables.sql       — script SQL para criar a tabela no Oracle
├── src/
│   ├── main.py                 — menu principal e validacoes de entrada
│   ├── producao.py             — logica de negocio e dados em memoria
│   ├── arquivo.py              — manipulacao de arquivos JSON e texto
│   ├── banco.py                — conexao e operacoes com o Oracle
│   └── config.exemplo.py      — modelo de configuracao (sem credenciais)
├── .gitignore
└── README.md
```

---

## 🔧 Como executar o código

### Pre-requisitos

- Python 3.10 ou superior
- Biblioteca `oracledb` (opcional, apenas para uso com Oracle):

```bash
pip install oracledb
```

### Configuracao do banco de dados (opcional)

1. Execute o script `scripts/create_tables.sql` no seu banco Oracle.

2. Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp src/config.exemplo.py src/config.py
```

```python
ORACLE_USER     = "seu_usuario"
ORACLE_PASSWORD = "sua_senha"
ORACLE_DSN      = "host:porta/service_name"
```

### Executando

```bash
cd src
python main.py
```

> O sistema funciona sem Oracle. Salvar/carregar JSON e exportar relatorio TXT estao sempre disponiveis.

---

## 🗃 Histórico de lançamentos

* 0.1.0 - 10/04/2025
    * Versao inicial: registro de producoes por cultura, calculo de producao e receita, persistencia em JSON e texto, e conexao com Oracle.

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
