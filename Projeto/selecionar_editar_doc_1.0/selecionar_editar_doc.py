import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
from sqlcipher3 import dbapi2 as sqlite
from docx import Document
from datetime import datetime
import locale

# -----------------------------
# Configurações
# -----------------------------
caminho_banco = os.path.join(os.path.expanduser("~"), "Documents", "CLIENTES WEB", "sistema_advogados", "Projeto", "selecionar_editar_doc_1.0", "bd_advocacia_db.db")
os.makedirs(os.path.dirname(caminho_banco), exist_ok=True)

SENHA = "minha_senha_forte"  # pode depois usar Keyring

# -----------------------------
# Funções do banco
# -----------------------------
def conectar():
    conn = sqlite.connect(caminho_banco)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA key='{SENHA}';")
    return conn, cursor

def init_db():
    conn, cursor = conectar()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS modelos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE CHECK (length(nome) <= 100),
            arquivo BLOB NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL CHECK (length(nome) <= 100),
            nacionalidade TEXT NOT NULL CHECK (length(nacionalidade) <= 50),
            estado_civil TEXT NOT NULL CHECK (length(estado_civil) <= 50),
            profissao TEXT NOT NULL CHECK (length(profissao) <= 50),
            rg TEXT NOT NULL CHECK (length(rg) <= 20),
            cpf TEXT NOT NULL UNIQUE CHECK (length(cpf) <= 14),
            logradouro TEXT NOT NULL CHECK (length(logradouro) <= 200),
            numero_residencia TEXT NOT NULL CHECK (length(numero_residencia) <= 10),
            bairro TEXT NOT NULL CHECK (length(bairro) <= 100),
            cidade TEXT NOT NULL CHECK (length(cidade) <= 100),
            uf TEXT NOT NULL CHECK (length(uf) <= 2),
            cep TEXT NOT NULL CHECK (length(cep) <= 10),
            telefone TEXT CHECK (length(telefone) <= 20),
            email TEXT CHECK (length(email) <= 100),
            nomeReu TEXT CHECK (length(nomeReu) <= 100),
            cnpjReu TEXT CHECK (length(cnpjReu) <= 20)
        );
    """)
    conn.commit()
    conn.close()

def inserir_cliente(dados):
    try:
        conn, cursor = conectar()

        cursor.execute("""
            INSERT INTO clientes (
                nome, nacionalidade, estado_civil, profissao, rg, cpf, logradouro,
                numero_residencia, bairro, cidade, uf, cep, telefone, email, nomeReu, cnpjReu
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dados["Nome"], dados["Nacionalidade"], dados["Estado Civil"], dados["Profissão"],
            dados["RG"], dados["CPF"], dados["Logradouro"], dados["Número da Residência"],
            dados["Bairro"], dados["Cidade"], dados["UF"], dados["CEP"],
            dados.get("Telefone", ""), dados.get("Email", ""),
            dados.get("Nome do Réu", ""), dados.get("CNPJ do Réu", "")
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Cliente inserido com sucesso!")

    except sqlite.IntegrityError as e:
        messagebox.showerror("Erro", f"Erro de integridade (dado duplicado ou inválido): {e}")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao inserir o cliente: {e}")
        
    carregar_clientes()

def listar_clientes():
    conn, cursor = conectar()
    cursor.execute("SELECT id, nome FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def inserir_modelo(nome, caminho_arquivo):
    with open(caminho_arquivo, "rb") as f:
        blob = f.read()
    conn, cursor = conectar()
    try:
        cursor.execute("INSERT INTO modelos (nome, arquivo) VALUES (?, ?)", (nome, blob))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Modelo '{nome}' inserido com sucesso!")
    except sqlite.IntegrityError:
        messagebox.showwarning("Aviso", f"Já existe um documento com o nome '{nome}'")
    finally:
        conn.close()
    carregar_modelos()

def listar_modelos():
    conn, cursor = conectar()
    cursor.execute("SELECT id, nome FROM modelos")
    modelos = cursor.fetchall()
    conn.close()
    return modelos

def exportar_modelo(modelo_id, destino):
    conn, cursor = conectar()
    cursor.execute("SELECT nome, arquivo FROM modelos WHERE id=?", (modelo_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        nome, blob = row
        os.makedirs(destino, exist_ok=True)
        arquivo_destino = os.path.join(destino, f"{nome}.docx")
        with open(arquivo_destino, "wb") as f:
            f.write(blob)
        return arquivo_destino
    return None

# -----------------------------
# Funções da GUI
# -----------------------------
def carregar_clientes():
    clientes = listar_clientes()
    nomes = [m[1] for m in clientes]
    combobox_clientes['values'] = nomes
    return clientes

def carregar_modelos():
    modelos = listar_modelos()
    nomes = [m[1] for m in modelos]
    combobox_modelos['values'] = nomes
    return modelos

def adicionar_cliente():
    janela = tk.Toplevel(root)
    janela.title("Adicionar Cliente")
    janela.geometry("750x600")
    janela.resizable(False, False)

    frame = tk.Frame(janela, padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    campos = {
        "Nome": 100,
        "Nacionalidade": 50,
        "Estado Civil": 50,
        "Profissão": 50,
        "RG": 13,
        "CPF": 14,
        "Logradouro": 200,
        "Número da Residência": 10,
        "Bairro": 100,
        "Cidade": 100,
        "UF": 2,
        "CEP": 10,
        "Telefone": 20,
        "Email": 100,
        "Nome do Réu": 100,
        "CNPJ do Réu": 20
    }

    entradas = {}

    for i, (campo, limite) in enumerate(campos.items()):
        row = i % 8
        col = i // 8

        label = tk.Label(frame, text=campo + ":", anchor="w")
        label.grid(row=row, column=col*2, padx=5, pady=5, sticky="w")

        vcmd = (janela.register(lambda P, l=limite: len(P) <= l), "%P")
        entry = tk.Entry(frame, width=30, validate="key", validatecommand=vcmd)
        entry.grid(row=row, column=col*2 + 1, padx=5, pady=5, sticky="w")

        entradas[campo] = entry

    def formatar(campo, valor):
        if campo in ["Nome", "Nome do Réu"]:
            return valor.title().replace(" Da ", " da ").replace(" De ", " de ") \
                .replace(" Do ", " do ").replace(" Dos ", " dos ") \
                .replace(" Das ", " das ").replace(" E ", " e ").replace(" Em ", " em ")
        elif campo in ["Nacionalidade", "Estado Civil", "Email"]:
            return valor.lower()
        elif campo in ["Logradouro", "Bairro"]:
            return valor.capitalize()
        elif campo == "UF":
            return valor.upper()
        return valor

    def confirmar():
        dados = {}
        for campo, entry in entradas.items():
            valor = entry.get().strip()
            if not valor and campo not in ["Telefone", "Email", "Nome do Réu", "CNPJ do Réu"]:
                messagebox.showwarning("Aviso", f"O campo {campo} não pode estar vazio!")
                return
            dados[campo] = formatar(campo, valor)

        inserir_cliente(dados)
        janela.destroy()

    btn_adicionar = tk.Button(janela, text="Adicionar", command=confirmar)
    btn_adicionar.pack(pady=20)

def adicionar_modelo():
    janela = tk.Toplevel(root)
    janela.title("Adicionar Modelo")
    janela.geometry("450x150")

    tk.Label(janela, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(janela, text="Arquivo:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    label_caminho = tk.Label(janela, text="", anchor="w")
    label_caminho.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    def escolher_arquivo():
        caminho = filedialog.askopenfilename(
            title="Selecione um documento",
            filetypes=[("Documentos Word", "*.docx"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            label_caminho.config(text=caminho)

    btn_escolher = tk.Button(janela, text="Escolher Arquivo", command=escolher_arquivo)
    btn_escolher.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    def confirmar():
        nome = entry_nome.get().strip()
        caminho = label_caminho.cget("text")
        if not nome:
            messagebox.showwarning("Aviso", "O nome não pode estar vazio!")
            return
        if not caminho:
            messagebox.showwarning("Aviso", "Selecione um arquivo!")
            return
        inserir_modelo(nome, caminho)
        janela.destroy()

    btn_adicionar = tk.Button(janela, text="Adicionar", command=confirmar)
    btn_adicionar.grid(row=3, column=1, padx=5, pady=10, sticky="e")

# -----------------------------
# Inicialização
# -----------------------------
init_db()

# GUI
root = tk.Tk()
root.title("Gerenciador de Modelos Jurídicos")
root.geometry("420x250")

tk.Label(root, text="Selecione o cliente:").pack(pady=10)
combobox_clientes = ttk.Combobox(root, state="readonly", width=40)
combobox_clientes.pack(pady=5)

tk.Label(root, text="Selecione um modelo:").pack(pady=10)
combobox_modelos = ttk.Combobox(root, state="readonly", width=40)
combobox_modelos.pack(pady=5)

frame_btns = tk.Frame(root)
frame_btns.pack(pady=15)

btn_add_modelo = tk.Button(frame_btns, text="Adicionar Modelo", command=adicionar_modelo, width=15)
btn_add_modelo.grid(row=0, column=0, padx=5)

btn_add_cliente = tk.Button(frame_btns, text="Adicionar Cliente", command=adicionar_cliente, width=15)
btn_add_cliente.grid(row=0, column=1, padx=5)

carregar_clientes()
carregar_modelos()
root.mainloop()
