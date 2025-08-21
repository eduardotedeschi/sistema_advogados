import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
from sqlcipher3 import dbapi2 as sqlite

# -----------------------------
# Configurações
# -----------------------------
caminho_banco = os.path.join(os.path.expanduser("~"), "Documents", "CLIENTES WEB", "sistema_advogados", "Projeto", "selecionar_documentos_1.0", "documentos_db.db")
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS modelos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            arquivo BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()

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
def carregar_modelos():
    modelos = listar_modelos()
    nomes = [m[1] for m in modelos]
    combobox['values'] = nomes
    return modelos

def abrir_modelo():
    nome_escolhido = combobox.get()
    if not nome_escolhido:
        messagebox.showwarning("Atenção", "Selecione um modelo!")
        return

    modelos = listar_modelos()
    for m in modelos:
        if m[1] == nome_escolhido:
            arquivo_temp = exportar_modelo(m[0], os.path.join(os.path.expanduser("~"), "Documents", "CLIENTES WEB", "sistema_advogados", "Projeto", "selecionar_documentos_1.0", "temp"))
            if arquivo_temp and os.path.exists(arquivo_temp):
                try:
                    if os.name == "nt":
                        os.startfile(arquivo_temp)
                    elif os.name == "posix":
                        subprocess.call(["xdg-open", arquivo_temp])
                except Exception as e:
                    messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")
            else:
                messagebox.showerror("Erro", "Arquivo não encontrado!")
            break

def adicionar_modelo():
    # Cria a nova janela
    nome_janela = tk.Toplevel(root)
    nome_janela.title("Adicionar Modelo")
    nome_janela.geometry("1500x150")

    tk.Label(nome_janela, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_nome = tk.Entry(nome_janela, width=40)
    entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(nome_janela, text="Arquivo:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    label_caminho = tk.Label(nome_janela, text="", anchor="w")
    label_caminho.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Função para selecionar arquivo
    def escolher_arquivo():
        caminho = filedialog.askopenfilename(
            title="Selecione um documento",
            filetypes=[("Documentos Word", "*.docx"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            label_caminho.config(text=caminho)

    btn_escolher = tk.Button(nome_janela, text="Escolher Arquivo", command=escolher_arquivo)
    btn_escolher.grid(row=2, column=1, padx=5, pady=5, sticky="e")

    # Função para confirmar inserção
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
        nome_janela.destroy()

    btn_confirmar = tk.Button(nome_janela, text="Confirmar", command=confirmar)
    btn_confirmar.grid(row=3, column=1, padx=5, pady=10, sticky="e")

# -----------------------------
# Inicialização
# -----------------------------
init_db()

# GUI
root = tk.Tk()
root.title("Gerenciador de Modelos Jurídicos")
root.geometry("420x250")

tk.Label(root, text="Selecione um modelo:").pack(pady=10)
combobox = ttk.Combobox(root, state="readonly", width=40)
combobox.pack(pady=5)

frame_btns = tk.Frame(root)
frame_btns.pack(pady=15)

btn_abrir = tk.Button(frame_btns, text="Abrir Modelo", command=abrir_modelo, width=15)
btn_abrir.grid(row=0, column=0, padx=5)

btn_add = tk.Button(frame_btns, text="Adicionar Modelo", command=adicionar_modelo, width=15)
btn_add.grid(row=0, column=1, padx=5)

carregar_modelos()
root.mainloop()
