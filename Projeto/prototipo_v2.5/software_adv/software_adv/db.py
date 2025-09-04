import sqlite3

DB_NAME = "bd_advogados.bd"

def conecta_bd():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor

def desconecta_bd(conn):
    if conn:
        conn.close()

def monta_tabelas():
    conn, cursor = conecta_bd()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            cli_id INTEGER PRIMARY KEY,
            cli_nome VARCHAR(100) NOT NULL,
            cli_nacionalidade VARCHAR(50) NOT NULL,
            cli_estado_civil VARCHAR(50),
            cli_profissao VARCHAR(50) NOT NULL,
            cli_rg VARCHAR(10) NOT NULL,
            cli_cpf CHAR(11) UNIQUE NOT NULL,
            cli_cep CHAR(8) NOT NULL,
            cli_uf CHAR(2) NOT NULL,
            cli_cidade VARCHAR(100) NOT NULL,
            cli_logradouro VARCHAR(200) NOT NULL,
            cli_n_rua VARCHAR(10) NOT NULL,
            cli_bairro VARCHAR(100) NOT NULL,
            cli_telefone VARCHAR(10),
            cli_email VARCHAR(100),
            cli_nome_reu VARCHAR(100),
            cli_cnpj_reu VARCHAR(14)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            doc_id INTEGER PRIMARY KEY,
            doc_nome VARCHAR(100) UNIQUE NOT NULL,
            doc_tipo VARCHAR(20) NOT NULL,
            doc_arquivo BLOB UNIQUE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documento_gerado (
            dg_id INTEGER PRIMARY KEY,
            fk_clientes_id INTEGER NOT NULL,
            fk_documentos_id INTEGER NOT NULL,
            dg_nome VARCHAR(100) UNIQUE NOT NULL,
            dg_data_criacao DATE NOT NULL,
            dg_arquivo BLOB UNIQUE NOT NULL,
            FOREIGN KEY (fk_clientes_id) REFERENCES clientes (cli_id),
            FOREIGN KEY (fk_documentos_id) REFERENCES documentos (doc_id)
        );
    """)

    conn.commit()
    desconecta_bd(conn)
