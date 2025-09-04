import sqlite3
import os
import tempfile
from datetime import datetime
from tkinter import END, messagebox
from docx import Document
from docx2pdf import convert
import subprocess
import sys
import unicodedata
import re
import time

from software_adv.db import conecta_bd, desconecta_bd
from software_adv import utils


# ==============================
# CLIENTES
# ==============================
def add_cliente(cliente: dict):
    conn, cursor = conecta_bd()
    try:
        cursor.execute("""
            INSERT INTO clientes (
                cli_nome, cli_nacionalidade, cli_estado_civil, cli_profissao,
                cli_rg, cli_cpf, cli_cep, cli_uf, cli_cidade, cli_logradouro,
                cli_n_rua, cli_bairro, cli_telefone, cli_email,
                cli_nome_reu, cli_cnpj_reu
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cliente["nome"], cliente["nacionalidade"], cliente["estado_civil"],
            cliente["profissao"], cliente["rg"], cliente["cpf"], cliente["cep"],
            cliente["uf"], cliente["cidade"], cliente["logradouro"],
            cliente["n_rua"], cliente["bairro"], cliente["telefone"],
            cliente["email"], cliente["nome_reu"], cliente["cnpj_reu"]
        ))
        conn.commit()
        return True, "Cliente adicionado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: CPF ou CNPJ já cadastrado."
    finally:
        desconecta_bd(conn)


def select_listaClientes(lista_treeview):
        lista_treeview.delete(*lista_treeview.get_children())
        conn, cursor = conecta_bd()
        lista = cursor.execute(""" SELECT * FROM clientes ORDER BY cli_nome ASC""")

        for i in lista:
            lista_treeview.insert("", END, values=i)
        desconecta_bd(conn)


def atualizar_cliente(cli_id: int, dados: dict):
    conn, cursor = conecta_bd()
    try:
        campos = ", ".join([f"{k} = ?" for k in dados.keys()])
        valores = list(dados.values()) + [cli_id]
        cursor.execute(f"UPDATE clientes SET {campos} WHERE cli_id = ?", valores)
        conn.commit()
        return True, "Cliente atualizado com sucesso!"
    except Exception as e:
        return False, f"Erro: {e}"
    finally:
        desconecta_bd(conn)


def del_cliente(self, event):
        id_para_deletar = None
        
        # 1. Tenta obter o ID do campo id_entry (se estiver preenchido)
        id_da_entry = self.id_entry.get().strip()
        
        # 2. Tenta obter o ID da linha selecionada na Treeview
        selecao_treeview = self.listaCli.selection()
        
        try:
            if id_da_entry and selecao_treeview:
                # Caso 1: Ambos estão preenchidos, verifica se são iguais
                id_da_linha = self.listaCli.item(selecao_treeview[0], 'values')[0]
                if str(id_da_entry) != str(id_da_linha):
                    messagebox.showwarning("Aviso de Conflito", 
                                        "O ID no campo (digitado) é diferente do ID da linha selecionada.\n"
                                        "Por favor, use apenas um dos métodos para exclusão.")
                    return
                else:
                    id_para_deletar = id_da_entry

            elif id_da_entry:
                # Caso 2: Somente o campo id_entry está preenchido
                if not id_da_entry.isdigit():
                    messagebox.showerror("Erro de ID", "O ID deve ser um número inteiro.")
                    return
                id_para_deletar = id_da_entry

            elif selecao_treeview:
                # Caso 3: Somente a linha da Treeview está selecionada
                id_para_deletar = self.listaCli.item(selecao_treeview[0], 'values')[0]

            else:
                # Caso 4: Nenhum método de exclusão foi fornecido
                messagebox.showwarning("Erro de Seleção", 
                                    "Por favor, digite um ID ou selecione uma linha para exclusão.")
                return

            # Busca o nome do cliente no banco de dados usando o ID
            conn, cursor = conecta_bd()
            cursor.execute("SELECT cli_nome FROM clientes WHERE cli_id = ?", (id_para_deletar,))
            resultado_busca = cursor.fetchone()
            
            if resultado_busca is None:
                messagebox.showerror("Erro", f"O cliente com o ID: {id_para_deletar} não foi encontrado.")
                return

            nome_cliente = resultado_busca[0]
            
            # Confirmação com o nome e o ID do cliente
            confirmacao = messagebox.askyesno("Confirmar Exclusão", 
                                            f"Tem certeza que deseja excluir o cliente?\n\nNome: {nome_cliente}\nID: {id_para_deletar}?")
            
            if not confirmacao:
                return

            # Executa a exclusão no banco de dados
            cursor.execute("DELETE FROM clientes WHERE cli_id = ?", (id_para_deletar,))
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
            select_listaClientes(self.listaCli)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir o cliente.\n\nErro: {e}")
            
        finally:
            desconecta_bd(conn)


# ==============================
# DOCUMENTOS
# ==============================
def add_documento(nome, tipo, caminho):
    if not os.path.exists(caminho):
        return False, "Arquivo não encontrado."

    with open(caminho, "rb") as f:
        conteudo = f.read()

    conn, cursor = conecta_bd()
    try:
        cursor.execute("""
            INSERT INTO documentos (doc_nome, doc_tipo, doc_arquivo)
            VALUES (?, ?, ?)
        """, (nome, tipo, conteudo))
        conn.commit()
        return True, "Documento adicionado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: Nome ou arquivo já existe."
    finally:
        desconecta_bd(conn)


def listar_documentos():
    conn, cursor = conecta_bd()
    cursor.execute("SELECT doc_id, doc_nome, doc_tipo FROM documentos ORDER BY doc_nome ASC")
    docs = cursor.fetchall()
    desconecta_bd(conn)
    return docs


def deletar_documento(doc_id):
    conn, cursor = conecta_bd()
    try:
        cursor.execute("DELETE FROM documentos WHERE doc_id = ?", (doc_id,))
        conn.commit()
        return True, "Documento excluído com sucesso!"
    except Exception as e:
        return False, f"Erro: {e}"
    finally:
        desconecta_bd(conn)


# ==============================
# DOCUMENTOS GERADOS
# ==============================
def gerar_documento(cli_id, doc_id, nome_gerado):
    conn, cursor = conecta_bd()
    try:
        cursor.execute("SELECT * FROM clientes WHERE cli_id = ?", (cli_id,))
        cliente = cursor.fetchone()
        cursor.execute("SELECT doc_arquivo FROM documentos WHERE doc_id = ?", (doc_id,))
        doc_bin = cursor.fetchone()[0]

        if not cliente or not doc_bin:
            return False, "Cliente ou documento não encontrado."

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(doc_bin)
            caminho_tmp = tmp.name

        doc_modelo = Document(caminho_tmp)
        os.remove(caminho_tmp)

        # Substitui variáveis {{NOME}}, {{CPF}}, etc.
        mapa = {
            "{{NOME}}": cliente[1],
            "{{CPF}}": utils.formatar_cpf(cliente[6]),
            "{{CIDADE}}": cliente[9],
            "{{ANO}}": str(datetime.now().year)
        }

        for p in doc_modelo.paragraphs:
            for chave, valor in mapa.items():
                if chave in p.text:
                    p.text = p.text.replace(chave, valor)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as novo:
            doc_modelo.save(novo.name)
            novo.seek(0)
            novo_bin = novo.read()
            caminho_novo = novo.name

        cursor.execute("""
            INSERT INTO documento_gerado (fk_clientes_id, fk_documentos_id, dg_nome, dg_data_criacao, dg_arquivo)
            VALUES (?, ?, ?, ?, ?)
        """, (cli_id, doc_id, nome_gerado, datetime.now().strftime("%d-%m-%Y"), novo_bin))
        conn.commit()

        return True, f"Documento '{nome_gerado}' gerado e salvo."
    except Exception as e:
        return False, f"Erro: {e}"
    finally:
        desconecta_bd(conn)
