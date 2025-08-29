from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import sqlite3
import pandas as pd
import sv_ttk
import darkdetect

root = Tk()

class SearchableComboBox():
    def __init__(self, parent, options, x, y, w) -> None:
        #Configuração de estilo para as Entrys
        self.style = ttk.Style()
        self.style.configure("Big.TEntry", font=("Helvetica", 20))

        self.dropdown_id = None
        self.options = options

        # Create a Text widget for the entry field
        wrapper = ttk.Frame(parent, style="Big.TEntry")
        wrapper.place(relx=x, rely=y, relwidth=w)

        self.entry = ttk.Entry(wrapper, width=14)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.pack(side=LEFT, fill=X, expand=True)

        # Create a Listbox widget for the dropdown menu
        self.listbox = Listbox(parent, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        for option in self.options:
            self.listbox.insert(END, option)

    def on_entry_key(self, event):
        typed_value = event.widget.get().strip().lower()
        self.listbox.delete(0, END)
        if not typed_value:
            filtered_options = self.options
        else:
            filtered_options = [option for option in self.options if option.lower().startswith(typed_value)]

        for option in filtered_options:
            self.listbox.insert(END, option)

        self.show_dropdown()

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_option = self.listbox.get(selected_index)
            self.entry.delete(0, END)
            self.entry.insert(0, selected_option)

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0, anchor="nw")
        self.listbox.lift()

        if self.dropdown_id:
            self.listbox.after_cancel(self.dropdown_id)
        self.dropdown_id = self.listbox.after(2000, self.hide_dropdown)

    def hide_dropdown(self):
        self.listbox.place_forget()

class Funcs():
    def limpa_tela(self):
        self.nome_entry.delete(0, END)
        self.nacionalidade_combo.entry.delete(0, END)
        self.estado_civil_combo.entry.delete(0, END)
        self.profissao_entry.delete(0, END)
        self.rg_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.cep_entry.delete(0, END)
        self.uf_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.rua_entry.delete(0, END)
        self.n_rua_entry.delete(0, END)
        self.bairro_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.nome_reu_entry.delete(0, END)
        self.cnpj_reu_entry.delete(0, END)
        self.cpf_busca_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("bd_advogados.bd")
        self.cursor =self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conecta_bd()

        # Cria a tabela de clientes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cli_id INTEGER PRIMARY KEY,
                cli_nome VARCHAR(100) UNIQUE NOT NULL,
                cli_nacionalidade VARCHAR(50) NOT NULL,
                cli_estado_civil VARCHAR(50) CHECK (cli_estado_civil IN ('solteiro', 'solteira', 'casado', 'casada', 'divorciado', 'divorciada', 'viúvo', 'viúva', 'separado', 'separada', 'união estável', 'separação judicial')),
                cli_rg VARCHAR(14) NOT NULL,
                cli_cpf VARCHAR(14) NOT NULL,
                cli_cep VARCHAR(10) NOT NULL,
                cli_uf VARCHAR(2) NOT NULL,
                cli_cidade VARCHAR(100) NOT NULL,
                cli_logradouro VARCHAR(200) NOT NULL,
                cli_n_rua VARCHAR(10) NOT NULL,
                cli_bairro VARCHAR(100) NOT NULL,
                cli_telefone VARCHAR(20),
                cli_email VARCHAR(100),
                cli_nome_reu VARCHAR(100),
                cli_cnpj_reu VARCHAR(20)
            );
        """)

        # Cria a tabela de documentos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS documentos (
                doc_id INTEGER PRIMARY KEY,
                doc_nome VARCHAR(100) UNIQUE NOT NULL,
                doc_tipo VARCHAR(20) NOT NULL,
                doc_arquivo BLOB NOT NULL
            );
        """)
                            
        # Cria a tabela de documentos gerados
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS documento_gerado (
                dg_id INTEGER PRIMARY KEY,
                fk_clientes_id INTEGER NOT NULL,
                fk_documentos_id INTEGER NOT NULL,
                dg_nome VARCHAR(100) NOT NULL,
                dg_data_criacao DATE NOT NULL,
                dg_arquivo BLOB NOT NULL,
                FOREIGN KEY (fk_clientes_id) REFERENCES clientes (cli_id),
                FOREIGN KEY (fk_documentos_id) REFERENCES documentos (doc_id)
            );
        """)

        self.conn.commit()
        self.desconecta_bd()
    
    def add_cliente(self):
        # Coletando dados dos campos
        self.nome_completo = self.nome_entry.get().title() \
                              .replace(" Da ", " da ") \
                              .replace(" De ", " de ") \
                              .replace(" Do ", " do ") \
                              .replace(" Dos ", " dos ") \
                              .replace(" Das ", " das ") \
                              .replace(" E ", " e ")
        self.nacionalidade = self.nacionalidade_combo.get().lower()
        self.estado_civil = self.estado_civil_combo.get().lower()
        self.profissao = self.profissao_entry.get().lower()
        self.rg = self.rg_entry.get()
        self.cpf = self.cpf_entry.get()
        self.cep = self.cep_entry.get()
        self.uf = self.uf_entry.get().upper()
        self.cidade = self.cidade_entry.get().title() \
                                     .replace(" Da ", " da ") \
                                     .replace(" De ", " de ") \
                                     .replace(" Do ", " do ") \
                                     .replace(" Dos ", " dos ") \
                                     .replace(" Das ", " das ") \
                                     .replace(" Em ", " em ")
        self.logradouro = self.rua_entry.get().title() \
                                     .replace(" Da ", " da ") \
                                     .replace(" De ", " de ") \
                                     .replace(" Do ", " do ") \
                                     .replace(" Dos ", " dos ") \
                                     .replace(" Das ", " das ") \
                                     .replace(" Em ", " em ")
        self.n_rua = self.n_rua_entry.get()
        self.bairro = self.bairro_entry.get().title() \
                                     .replace(" Da ", " da ") \
                                     .replace(" De ", " de ") \
                                     .replace(" Do ", " do ") \
                                     .replace(" Dos ", " dos ") \
                                     .replace(" Das ", " das ") \
                                     .replace(" Em ", " em ")
        self.telefone = self.telefone_entry.get()
        self.email = self.email_entry.get().lower()
        self.nome_reu = self.nome_reu_entry.get().title() \
                              .replace(" Da ", " da ") \
                              .replace(" De ", " de ") \
                              .replace(" Do ", " do ") \
                              .replace(" Dos ", " dos ") \
                              .replace(" Das ", " das ") \
                              .replace(" E ", " e ")
        self.cnpj_reu = self.cnpj_reu_entry.get()

        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes ()""")

    
    def escolher_arquivo(self):
        #Abre o explorer
        caminho = filedialog.askopenfilename(
            title="Selecione um documento",
            filetypes=[("Documentos Word", "*.docx"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.caminho_doc_entry.delete(0, END)
            self.caminho_doc_entry.insert(0, caminho)
    
    def criar_treeview_generica(self, pai, colunas, cabecalhos, larguras_colunas, relx, rely, relwidth, relheight):
        # Cria a Treeview
        treeview = ttk.Treeview(pai, height=3, columns=colunas, show="headings")

        # Configura os cabeçalhos e larguras das colunas
        for i, (cabecalho, largura) in enumerate(zip(cabecalhos, larguras_colunas)):
            treeview.heading(f"#{i+1}", text=cabecalho)
            treeview.column(f"#{i+1}", width=largura)

        # Posiciona a Treeview
        treeview.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)

        # Cria e configura a barra de rolagem vertical
        scroll_y = ttk.Scrollbar(pai, orient='vertical', command=treeview.yview)
        treeview.configure(yscrollcommand=scroll_y.set)
        scroll_y.place(relx=relx + relwidth, rely=rely, relwidth=0.02, relheight=relheight)

        # Cria e configura a barra de rolagem horizontal
        scroll_x = ttk.Scrollbar(pai, orient='horizontal', command=treeview.xview)
        treeview.configure(xscrollcommand=scroll_x.set)
        scroll_x.place(relx=relx, rely=rely + relheight, relwidth=relwidth, relheight=0.02)

        # Lógica de scroll com o mouse
        def _on_mousewheel_vertical(event):
            treeview.yview_scroll(-3 * int(event.delta / 120), "units")

        def _on_mousewheel_horizontal(event):
            treeview.xview_scroll(-1 * int(event.delta / 120), "units")

        treeview.bind("<MouseWheel>", _on_mousewheel_vertical)
        treeview.bind("<Shift-MouseWheel>", _on_mousewheel_horizontal)
        
        return treeview

    def lista_documentos(self):
        #Declaração dos parâmetros
        colunas = ("col1", "col2", "col3")
        cabecalhos = ("Código", "Nome", "Tipo")
        larguras = (50, 350, 100)
        relx, rely, relwidth, relheight = 0.02, 0.27, 0.95, 0.7
        
        self.listaDoc = self.criar_treeview_generica(self.frame_documento, colunas, cabecalhos, larguras, relx, rely, relwidth, relheight)

    def lista_clientes(self):
        #Declaração dos parâmetros
        colunas = ("col1","col2","col3","col4","col5","col6","col7","col8","col9","col10","col11","col12","col13","col14","col15","col16","col17")
        cabecalhos = ("Código", "Nome Completo", "Nacionalidade", "Estado Civil", "Profissão", "RG", "CPF", "CEP", "UF", "Cidade", "Rua", "Nº Rua", "Bairro", "Telefone", "Email", "Nome Completo Réu", "CNPJ Réu")
        larguras = (100, 250, 150, 150, 200, 125, 125, 100, 75, 200, 200, 100, 200, 125, 150, 250, 200)
        relx, rely, relwidth, relheight = 0.02, 0.51, 0.95, 0.46
        
        self.listaCli = self.criar_treeview_generica(self.frame_cliente, colunas, cabecalhos, larguras, relx, rely, relwidth, relheight)

    def lista_clientes_doc(self):
        #Declaração dos parâmetros
        colunas = ("col1","col2","col3", "col4", "col5", "col6")
        cabecalhos = ("Código", "Nome Cliente", "CPF Cliente", "Nome Documento", "Tipo Documento", "Data Gerada")
        larguras = (25, 150, 100, 150, 75, 75)
        relx, rely, relwidth, relheight = 0.02, 0.1, 0.95, 0.6
        
        self.listCliDoc = self.criar_treeview_generica(self.frame_clientes_doc, colunas, cabecalhos, larguras, relx, rely, relwidth, relheight)

    def gerenciar_clientes(self):
        #Configuração de estilo para as Entrys
        self.style = ttk.Style()
        self.style.configure("Big.TEntry", font=("Helvetica", 20))

        #Label e Entry do id
        self.lb_id = ttk.Label(self.frame_cliente, text = "ID")
        self.lb_id.place(relx= 0.04, rely=0.02)
        self.id_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.id_entry.place(relx= 0.03, rely=0.05, relwidth=0.05)

        #Label e Entry do nome
        self.lb_nome = ttk.Label(self.frame_cliente, text = "Nome Completo*")
        self.lb_nome.place(relx= 0.12, rely=0.02)
        self.nome_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.nome_entry.place(relx= 0.11, rely=0.05, relwidth=0.30)

        #Label e Combobox da nacionalidade
        self.lb_nacionalidade = ttk.Label(self.frame_cliente, text = "Nacionalidade*")
        self.lb_nacionalidade.place(relx= 0.45, rely=0.02)
        opc_nacionalidade = ["afegão", "afegã", "albanês", "albanesa", "alemão", "alemã", "americano", "americana", "andorrano", "andorrana", "angolano", "angolana", "antiguano", "antiguana", "argentino", "argentina", "armênio", "armênia", "australiano", "australiana", "austríaco", "austríaca", "azerbaijano", "azerbaijana", "bahamense", "bangladeshiano", "bangladeshiana", "barbadiano", "barbadiana", "belga", "belizenho", "belizenha", "beninense", "bielorrusso", "bielorrussa", "boliviano", "boliviana", "bósnio", "bósnia", "botsuanês", "botsuanesa", "brasileiro", "brasileira", "britânico", "britânica", "búlgaro", "búlgara", "burquinense", "burundês", "burundesa", "butanês", "butanesa", "cabo-verdiano", "cabo-verdiana", "camaronês", "camaronesa", "cambojano", "cambojana", "canadense", "catariano", "catarina", "chileno", "chilena", "chinês", "chinesa", "cingapuriano", "cingapuriana", "colombiano", "colombiana", "congolês", "congolesa", "coreano do norte", "coreana do norte", "coreano do sul", "coreana do sul", "costarriquenho", "costarriquenha", "croata", "cubano", "cubana", "dinamarquês", "dinamarquesa", "dominicano", "dominicana", "egípcio", "egípcia", "equatoriano", "equatoriana", "eritreu", "eritreia", "escocês", "escocesa", "eslovaco", "eslovaca", "esloveno", "eslovena", "espanhol", "espanhola", "estoniano", "estoniana", "etíope", "filipino", "filipina", "finlandês", "finlandesa", "francês", "francesa", "gabonês", "gabonesa", "galês", "galesa", "ganês", "ganesa", "georgiano", "georgiana", "grego", "grega", "guatemalteco", "guatemalteca", "guianês", "guianesa", "guineense", "haitiano", "haitiana", "holandês", "holandesa", "hondurenho", "hondurenha", "húngaro", "húngara", "iemenita", "indiano", "indiana", "indonésio", "indonésia", "inglês", "inglesa", "iraquiano", "iraquiana", "iraniano", "iraniana", "irlandês", "irlandesa", "islandês", "islandesa", "israelense", "italiano", "italiana", "jamaicano", "jamaicana", "japonês", "japonesa", "jordano", "jordana", "kazakhstanês", "kazakhstanesa", "keniano", "keniana", "kiribati", "kuwaitiano", "kuwaitiana", "letão", "letona", "libanês", "libanesa", "liberiano", "liberiana", "líbio", "líbia", "liechtensteiniano", "liechtensteiniana", "lituano", "lituana", "luxemburguês", "luxemburguesa", "macedônio", "macedônia", "malaio", "malaia", "malawiano", "malawiana", "maliano", "maliana", "maltês", "maltesa", "marroquino", "marroquina", "mauriciano", "mauriciana", "mexicano", "mexicana", "moçambicano", "moçambicana", "moldávio", "moldávia", "monegasco", "monegasca", "mongol", "montenegrino", "montenegrina", "namibiano", "namibiana", "nepalês", "nepalesa", "nicaraguense", "nigeriano", "nigeriana", "norueguês", "norueguesa", "neozelandês", "neozelandesa", "omanês", "omanesa", "paquistanês", "paquistanesa", "palestino", "palestina", "panamenho", "panamenha", "papua nova guiné", "paraguaio", "paraguaia", "peruano", "peruana", "polonês", "polonesa", "portorriquenho", "portorriquenha", "português", "portuguesa", "qatari", "qatari", "queniano", "queniana", "quirguiz", "quirguiz", "romeno", "romena", "ruandês", "ruandesa", "russo", "russa", "salvadorenho", "salvadorenha", "samoano", "samoana", "sanmarinense", "sanmarinense", "saudita", "saudita", "senegalês", "senegalesa", "sérvio", "sérvia", "somaliano", "somaliana", "sudanês", "sudanesa", "sueco", "sueca", "suíço", "suíça", "surinamês", "surinamesa", "tailandês", "tailandesa", "tanzaniano", "tanzaniana", "timorense", "timorense", "togolês", "togolesa", "turco", "turca", "turcomano", "turcomana", "ucraniano", "ucraniana", "ugandês", "ugandesa", "uruguaio", "uruguaia", "uzbeque", "uzbeque", "venezuelano", "venezuelana", "vietnamita", "vietnamita", "zambiano", "zambiana", "zimbabuano", "zimbabuana"]
        self.nacionalidade_combo = SearchableComboBox(self.frame_cliente, opc_nacionalidade, 0.44, 0.05, 0.15)

        #Label e Combobox do estado civil
        self.lb_estado_civil = ttk.Label(self.frame_cliente, text = "Estado Civil*")
        self.lb_estado_civil.place(relx= 0.63, rely=0.02)
        opc_estado_civil = ["solteiro", "solteira", "casado", "casada", "divorciado", "divorciada", "viúvo", "viúva", "separado", "separada", "união estável", "separação judicial"]
        self.estado_civil_combo = SearchableComboBox(self.frame_cliente, opc_estado_civil, 0.62, 0.05, 0.15)

        #Label e Entry da profissão
        self.lb_profissao = ttk.Label(self.frame_cliente, text = "Profissão*")
        self.lb_profissao.place(relx= 0.81, rely=0.02)
        self.profissao_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.profissao_entry.place(relx= 0.80, rely=0.05, relwidth=0.17)

        #Label e Entry do RG
        self.lb_rg = ttk.Label(self.frame_cliente, text = "RG*")
        self.lb_rg.place(relx= 0.04, rely=0.11)
        self.rg_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.rg_entry.place(relx= 0.03, rely=0.14, relwidth=0.15)

        #Label e Entry do CPF
        self.lb_cpf = ttk.Label(self.frame_cliente, text = "CPF*")
        self.lb_cpf.place(relx= 0.22, rely=0.11)
        self.cpf_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cpf_entry.place(relx= 0.21, rely=0.14, relwidth=0.15)

        #Label e Entry do CEP
        self.lb_cep = ttk.Label(self.frame_cliente, text = "CEP*")
        self.lb_cep.place(relx= 0.40, rely=0.11)
        self.cep_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cep_entry.place(relx= 0.39, rely=0.14, relwidth=0.15)

        #Label e Entry da UF
        self.lb_uf = ttk.Label(self.frame_cliente, text = "UF*")
        self.lb_uf.place(relx= 0.58, rely=0.11)
        self.uf_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.uf_entry.place(relx= 0.57, rely=0.14, relwidth=0.05)

        #Label e Entry da cidade
        self.lb_cidade = ttk.Label(self.frame_cliente, text = "Cidade*")
        self.lb_cidade.place(relx= 0.66, rely=0.11)
        self.cidade_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cidade_entry.place(relx= 0.65, rely=0.14, relwidth=0.18)

        #Label e Entry da rua
        self.lb_rua = ttk.Label(self.frame_cliente, text = "Rua*")
        self.lb_rua.place(relx= 0.04, rely=0.20)
        self.rua_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.rua_entry.place(relx= 0.03, rely=0.23, relwidth=0.3)

        #Label e Entry do numero da rua
        self.lb_n_rua = ttk.Label(self.frame_cliente, text = "Nº Rua*")
        self.lb_n_rua.place(relx= 0.37, rely=0.20)
        self.n_rua_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.n_rua_entry.place(relx= 0.36, rely=0.23, relwidth=0.1)

        #Label e Entry do bairro
        self.lb_bairro = ttk.Label(self.frame_cliente, text = "Bairro*")
        self.lb_bairro.place(relx= 0.50, rely=0.20)
        self.bairro_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.bairro_entry.place(relx= 0.49, rely=0.23, relwidth=0.25)

        #Label e Entry do telefone
        self.lb_telefone = ttk.Label(self.frame_cliente, text = "Telefone")
        self.lb_telefone.place(relx= 0.78, rely=0.20)
        self.telefone_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.telefone_entry.place(relx= 0.77, rely=0.23, relwidth=0.15)

        #Label e Entry do email
        self.lb_email = ttk.Label(self.frame_cliente, text = "Email")
        self.lb_email.place(relx= 0.04, rely=0.29)
        self.email_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.email_entry.place(relx= 0.03, rely=0.32, relwidth=0.25)

        #Label e Entry do nome do réu
        self.lb_nome_reu = ttk.Label(self.frame_cliente, text = "Nome Completo Réu")
        self.lb_nome_reu.place(relx= 0.32, rely=0.29)
        self.nome_reu_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.nome_reu_entry.place(relx= 0.31, rely=0.32, relwidth=0.4)

        #Label e Entry do CNPJ ou CPF do réu
        self.lb_cnpj_reu = ttk.Label(self.frame_cliente, text = "CNPJ/CPF Réu")
        self.lb_cnpj_reu.place(relx= 0.75, rely=0.29)
        self.cnpj_reu_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cnpj_reu_entry.place(relx= 0.74, rely=0.32, relwidth=0.23)

        #Botão adicionar cliente
        self.bt_add_cliente = ttk.Button(self.frame_cliente, text="Adicionar Cliente", style='Accent.TButton')
        self.bt_add_cliente.place(relx= 0.03, rely=0.44, relwidth=0.17)

        #Botão update cliente
        self.bt_update_cliente = ttk.Button(self.frame_cliente, text="Atualizar Cliente", style='Accent.TButton')
        self.bt_update_cliente.place(relx= 0.23, rely=0.44, relwidth=0.17)

        #Botão deletar cliente
        self.bt_del_cliente = ttk.Button(self.frame_cliente, text="Deletar Cliente", style='Accent.TButton')
        self.bt_del_cliente.place(relx= 0.43, rely=0.44, relwidth=0.17)

        #Label e Entry da pesquisa por nome ou cpf do cliente
        self.lb_nome_busca = ttk.Label(self.frame_cliente, text = "Buscar nome/CPF")
        self.lb_nome_busca.place(relx= 0.67, rely=0.41)
        self.nome_busca_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.nome_busca_entry.place(relx= 0.66, rely=0.44, relwidth=0.17)

        #Botão buscar cliente
        self.bt_buscar_cliente = ttk.Button(self.frame_cliente, text="Buscar", style='Accent.TButton')
        self.bt_buscar_cliente.place(relx= 0.84, rely=0.44, relwidth=0.11)

        #Botão limpar campos
        self.bt_limpar = ttk.Button(self.frame_cliente, text="Limpar", command=self.limpa_tela)
        self.bt_limpar.place(relx= 0.84, rely=0.38, relwidth=0.11)

        #Criação da Treeview
        self.lista_clientes()
    
    def gerenciar_documentos(self):
        #Configuração de estilo para as Entrys
        self.style = ttk.Style()
        self.style.configure("Big.TEntry", font=("Helvetica", 20))

        #Label e Entry do nome do documento
        self.lb_nome_doc = ttk.Label(self.frame_documento, text="Nome do Documento*")
        self.lb_nome_doc.place(relx= 0.04, rely=0.02)
        self.nome_doc_entry = ttk.Entry(self.frame_documento, style="Big.TEntry")
        self.nome_doc_entry.place(relx= 0.03, rely=0.05, relwidth=0.4)

        #Label e Combobox do tipo do documento
        self.lb_tipo = ttk.Label(self.frame_documento, text = "Tipo*")
        self.lb_tipo.place(relx= 0.47, rely=0.02)
        opc_tipo = ["Contrato", "Declaração", "Petição", "Tese", "Procuração"]
        self.tipo_combo = SearchableComboBox(self.frame_documento, opc_tipo, 0.46, 0.05, 0.15)

        #Label e Entry do caminho do documento
        self.lb_texto_caminho_doc = ttk.Label(self.frame_documento, text="Caminho do documento*: ")
        self.lb_texto_caminho_doc.place(relx= 0.04, rely=0.12)
        self.caminho_doc_entry = ttk.Entry(self.frame_documento, style="Big.TEntry")
        self.caminho_doc_entry.place(relx= 0.22, rely=0.11, relwidth=0.57)
        #Botão para abrir o explorer
        self.btn_escolher_doc = ttk.Button(self.frame_documento, text="Escolher Arquivo", command=self.escolher_arquivo)
        self.btn_escolher_doc.place(relx= 0.8, rely=0.11, relwidth=0.17)

        #Botão adicionar documento
        self.bt_add_documento = ttk.Button(self.frame_documento, text="Adicionar Documento", style='Accent.TButton')
        self.bt_add_documento.place(relx= 0.03, rely=0.2, relwidth=0.17)

        #Botão deletar documento
        self.bt_del_documento = ttk.Button(self.frame_documento, text="Deletar Documento", style='Accent.TButton')
        self.bt_del_documento.place(relx= 0.23, rely=0.2, relwidth=0.17)

        #Label e Entry da pesquisa por nome do documento
        self.lb_nome_doc_busca = ttk.Label(self.frame_documento, text="Buscar por nome")
        self.lb_nome_doc_busca.place(relx= 0.46, rely=0.17)
        self.nome_doc_busca_entry = ttk.Entry(self.frame_documento, style="Big.TEntry")
        self.nome_doc_busca_entry.place(relx= 0.45, rely=0.2, relwidth=0.34)

        #Botão buscar documento
        self.bt_buscar_documento = ttk.Button(self.frame_documento, text="Buscar", style='Accent.TButton')
        self.bt_buscar_documento.place(relx= 0.8, rely=0.2, relwidth=0.11)
        
        #Criação da Treeview
        self.lista_documentos()
    
    def clientes_doc(self):
        #Configuração de estilo para as Entrys
        self.style = ttk.Style()
        self.style.configure("Big.TEntry", font=("Helvetica", 20))

        #Label e Entry da pesquisa por Cliente
        self.lb_doc_busca = ttk.Label(self.frame_clientes_doc, text="Pesquisar por cliente")
        self.lb_doc_busca.place(relx= 0.04, rely=0.02)
        self.doc_busca_entry = ttk.Entry(self.frame_clientes_doc, style="Big.TEntry")
        self.doc_busca_entry.place(relx= 0.03, rely=0.05, relwidth=0.4)

        #Botão buscar cliente
        self.bt_doc_busca = ttk.Button(self.frame_clientes_doc, text="Buscar", style='Accent.TButton')
        self.bt_doc_busca.place(relx= 0.44, rely=0.05, relwidth=0.11)

        #Criação da Treeview
        self.lista_clientes_doc()

        #Botão deletar registro
        self.bt_del_registro = ttk.Button(self.frame_clientes_doc, text="Deletar Registro", style='Accent.TButton')
        self.bt_del_registro.place(relx= 0.02, rely=0.75, relwidth=0.17)

        #Botão exportar para Word
        self.bt_export_word = ttk.Button(self.frame_clientes_doc, text="Exportar Word", style='Accent.TButton')
        self.bt_export_word.place(relx= 0.60, rely=0.75, relwidth=0.17)

        #Botão exportar para PDF
        self.bt_export_pdf = ttk.Button(self.frame_clientes_doc, text="Exportar PDF", style='Accent.TButton')
        self.bt_export_pdf.place(relx= 0.80, rely=0.75, relwidth=0.17)

    def gerar_doc(self):
        #Configuração de estilo para as Entrys
        self.style = ttk.Style()
        self.style.configure("Big.TEntry", font=("Helvetica", 20))

        #Label e Entry da pesquisa por Cliente
        self.lb_cliente_busca = ttk.Label(self.frame_gerar_doc, text="Pesquisar de cliente")
        self.lb_cliente_busca.place(relx= 0.04, rely=0.02)
        
class App(Funcs):
    def __init__(self):
        #Configurações de inicialização
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.montaTabelas()
        root.mainloop()

    def tela(self):
        #Configurações da tela
        self.root.title("Sistema Advogados")
        sv_ttk.set_theme("light") 
        self.root.geometry("1280x1024")
        self.root.resizable(True, True)
        self.root.maxsize(width=1440, height=900)
        self.root.minsize(width=1024, height=768)
    
    def frames_da_tela(self):
        #Frame do menu de opções
        self.frame_menu = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_menu.place(relx= 0.02, rely=0.02, relwidth=0.2, relheight=0.96)

        #Frame da tela Gerenciar Clientes
        self.frame_cliente = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_cliente.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

        #Frame da tela Gerenciar Documentos
        self.frame_documento = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_documento.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

        #Frame da tela Clientes/Documentos
        self.frame_clientes_doc = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_clientes_doc.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

        #Frame da tela Gerar Contratos e Afins
        self.frame_gerar_doc = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_gerar_doc.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

    def widgets_frame1(self):
        #Logo da minha empresa
        self.img = PhotoImage(file="logo.png")
        self.img_logo = Label(self.frame_menu, image=self.img)
        self.img_logo.place(relx= 0.1, rely=0.02, relwidth=0.8, relheight=0.33)

        #Botão Gerenciar Clientes
        self.bt_clientes = ttk.Button(self.frame_menu, text="Gerenciar Clientes", command=lambda: [self.gerenciar_clientes(), self.frame_cliente.lift()])
        self.bt_clientes.place(relx= 0.05, rely=0.37, relwidth=0.9, relheight=0.05)

        #Botão Gerenciar Documentos
        self.bt_documentos = ttk.Button(self.frame_menu, text="Gerenciar Documentos", command=lambda: [self.gerenciar_documentos(), self.frame_documento.lift()])
        self.bt_documentos.place(relx= 0.05, rely=0.44, relwidth=0.9, relheight=0.05)

        #Botão Clientes/Documentos
        self.bt_clientes_doc = ttk.Button(self.frame_menu, text="Clientes/Documentos", command=lambda: [self.clientes_doc(), self.frame_clientes_doc.lift()])
        self.bt_clientes_doc.place(relx= 0.05, rely=0.51, relwidth=0.9, relheight=0.05)

        #Botão Gerar Contratos e Afins
        self.bt_contratos = ttk.Button(self.frame_menu, text="Gerar Contratos e Afins", command=lambda: [self.gerar_doc(), self.frame_gerar_doc.lift()])
        self.bt_contratos.place(relx= 0.05, rely=0.58, relwidth=0.9, relheight=0.05)

        #Botão Gerar Petição
        self.bt_peticao = ttk.Button(self.frame_menu, text="Gerar Petição")
        self.bt_peticao.place(relx= 0.05, rely=0.65, relwidth=0.9, relheight=0.05)

        #Botão Sair
        self.bt_sair = ttk.Button(self.frame_menu, text="Sair", command=self.root.destroy, style='Accent.TButton')
        self.bt_sair.place(relx= 0.05, rely=0.93, relwidth=0.9, relheight=0.05)

App()