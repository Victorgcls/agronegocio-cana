# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Sistema de Gestão de Colheita de Cana-de-Açúcar

## Gestão do Agronegócio em Python

## 👨‍🎓 Integrantes:
- João Victor do Nascimento Gonçalves

## 👩‍🏫 Professores:
### Tutor(a)
- Nicolly Candida Rodrigues de Souza
### Coordenador(a)
- Andre Godoi Chiovato

---

## 📜 Descrição

O Brasil é o maior produtor mundial de cana-de-açúcar, colhendo cerca de 620 milhões de toneladas por safra. Apesar do volume expressivo, as perdas durante a colheita são um problema sério para o setor: segundo a SOCICANA, chegam a até 5% na colheita manual e até 15% na colheita mecânica. Considerando a área plantada no estado de São Paulo, esse percentual representa uma perda anual de aproximadamente R$ 20 milhões.

Para enfrentar esse problema, este projeto desenvolve um **sistema de gestão de colheita de cana-de-açúcar** em Python, voltado ao pequeno e médio produtor rural. O sistema permite:

- Cadastrar talhões (áreas de plantio) com variedade e tamanho em hectares
- Registrar colheitas por talhão informando tipo (manual ou mecânica) e produção
- Calcular automaticamente a perda estimada e a produção líquida de cada colheita
- Visualizar a produtividade acumulada por talhão (toneladas por hectare)
- Gerar relatório consolidado de perdas com dica de melhoria
- Exportar relatório em arquivo de texto
- Salvar e carregar todos os dados em arquivo JSON
- Sincronizar os dados com banco de dados Oracle

O projeto aplica os conteúdos estudados nos **capítulos 3 ao 6** da disciplina:

| Capítulo | Conteúdo | Aplicação no projeto |
|----------|----------|----------------------|
| 3 | Funções com parâmetros | `calcular_perda()`, `buscar_talhao()`, `ler_inteiro()` |
| 3 | Procedimentos com parâmetros | `cadastrar_talhao()`, `registrar_colheita()`, `carregar_dados()` |
| 4 | Lista | `talhoes` e `colheitas` — listas de dicionários em memória |
| 4 | Tupla | `TIPOS_COLHEITA`, `VARIEDADES_CANA`, retorno de `calcular_perda()` |
| 4 | Dicionário | cada talhão e cada colheita é representado por um dicionário |
| 4 | Tabela de memória | `gerar_tabela_colheitas()` retorna uma lista de listas |
| 5 | Arquivo JSON | `salvar_json()` e `carregar_json()` em `arquivo.py` |
| 5 | Arquivo texto | `exportar_relatorio_txt()` e `registrar_log()` em `arquivo.py` |
| 6 | Banco Oracle | todas as funções de `banco.py` utilizando `oracledb` |

---

## 📁 Estrutura de pastas

```
agronegocio_cana/
├── assets/
│   └── logo-fiap.png
├── config/
│   └── config.exemplo.py       — modelo de configuração do banco
├── document/                   — documentos complementares
├── scripts/
│   └── create_tables.sql       — script de criação das tabelas no Oracle
├── src/
│   ├── main.py                 — menu principal e validações de entrada
│   ├── colheita.py             — lógica de negócio e dados em memória
│   ├── arquivo.py              — manipulação de arquivos JSON e texto
│   ├── banco.py                — conexão e operações com o Oracle
│   └── config.exemplo.py       — modelo de configuração (não contém credenciais)
├── .gitignore
└── README.md
```

---

## 🔧 Como executar o código

### Pré-requisitos

- Python 3.10 ou superior
- Biblioteca `oracledb`:

```bash
pip install oracledb
```

### Configuração do banco de dados

1. Execute o script `scripts/create_tables.sql` no seu banco Oracle para criar as tabelas.

2. Dentro da pasta `src/`, copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp src/config.exemplo.py src/config.py
```

```python
# src/config.py
ORACLE_USER     = "seu_usuario"
ORACLE_PASSWORD = "sua_senha"
ORACLE_DSN      = "host:porta/service_name"
```

> O arquivo `config.py` está listado no `.gitignore` e não será enviado ao GitHub.

### Executando

```bash
cd src
python main.py
```

> O sistema funciona normalmente sem Oracle. As opções de salvar/carregar JSON e exportar relatório TXT estão sempre disponíveis.

---

## 🗃 Histórico de lançamentos

* 0.1.0 - 10/04/2025
    * Versão inicial: cadastro de talhões, registro de colheitas, cálculo de perdas, relatórios, persistência em JSON e texto, e sincronização com Oracle.

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
