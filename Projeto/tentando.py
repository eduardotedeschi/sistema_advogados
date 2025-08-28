from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import sv_ttk
import darkdetect

root = Tk()

class SearchableComboBox():
    def __init__(self, parent, options, x, y, w) -> None:
        self.dropdown_id = None
        self.options = options

        # Create a Text widget for the entry field
        wrapper = ttk.Frame(parent)
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

    # Função para abrir o explorador e jogar o caminho no ENTRY
    def escolher_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione um documento",
            filetypes=[("Documentos Word", "*.docx"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            self.caminho_doc_entry.delete(0, END)
            self.caminho_doc_entry.insert(0, caminho)
    
    # Função para criar a Treeview dos documentos
    def lista_documentos(self):
        # Scroll vertical com mouse
        def _on_mousewheel_vertical(event):
            self.listaDoc.yview_scroll(-3 * int(event.delta / 120), "units")
            self.listaDoc.bind("<MouseWheel>", _on_mousewheel_vertical)

        # Scroll horizontal com Shift + mouse
        def _on_mousewheel_horizontal(event):
            self.listaDoc.xview_scroll(-1 * int(event.delta / 120), "units")
            self.listaDoc.bind("<Shift-MouseWheel>", _on_mousewheel_horizontal)

        self.listaDoc = ttk.Treeview(self.frame_documento, height= 3, columns=("col1","col2","col3",), show="headings")

        self.listaDoc.heading("#1", text="Código")
        self.listaDoc.heading("#2", text="Nome")
        self.listaDoc.heading("#3", text="Tipo")

        self.listaDoc.column("#1", width=50)
        self.listaDoc.column("#2", width=350)
        self.listaDoc.column("#3", width=100)

        self.listaDoc.place(relx= 0.02, rely=0.27, relwidth=0.95, relheight=0.73)

        # Criando barra de rolagem vertical
        self.scroll_y = ttk.Scrollbar(self.frame_documento, orient='vertical', command=self.listaDoc.yview)
        self.listaDoc.configure(yscrollcommand=self.scroll_y.set)
        self.scroll_y.place(relx=0.97, rely=0.27, relwidth=0.02, relheight=0.73)

        # Criando barra de rolagem horizontal
        self.scroll_x = ttk.Scrollbar(self.frame_documento, orient='horizontal', command=self.listaDoc.xview)
        self.listaDoc.configure(xscrollcommand=self.scroll_x.set)
        self.scroll_x.place(relx=0.02, rely=0.97, relwidth=0.95, relheight=0.02)
        
        # Adicionando dados do dataframe a treeview de documentos
        for index, row in self.df_docs.iterrows():
            valores = [row["ID"], row["Nome"], row["Tipo"]]
            self.listaDoc.insert("", "end", iid=row["ID"], values=valores)
    
    # Função que busca os documentos na treeview
    def busca_documentos(self, event=None):
        query = self.nome_doc_busca_entry.get().strip().lower()
        df_docs_filtered = self.df_docs.iloc[:0]

        if query.isdigit():
            df_docs_filtered = self.df_docs[self.df_docs['ID'] == int(query)]
        else:
            words = query.split(" ")
            words_stop = ["to", "and", "or"]
            words = list(set(words) - set(words_stop))
            for w in words:
                df_docs_filtered = pd.concat([df_docs_filtered, self.df_docs[self.df_docs['Nome'].str.contains(w, case=False)]], ignore_index=True)

        df_docs_filtered = df_docs_filtered.drop_duplicates()

        # Limpa a Treeview antes de inserir os resultados
        for item in self.listaDoc.get_children():
            self.listaDoc.delete(item)

        # Insere os resultados filtrados
        for index, row in df_docs_filtered.iterrows():
            valores = [row["ID"], row["Nome"], row["Tipo"]]
            self.listaDoc.insert("", "end", iid=row["ID"], values=valores)
    
    # Função que busca os registros na treeview dos clientes/documentos
    def busca_clientes_doc(self, event=None):
        query = self.doc_busca_entry.get().strip().lower()
        df_cli_docs_filtred = self.df_cli_docs.iloc[:0]

        if query.isdigit():
            df_cli_docs_filtred = self.df_cli_docs[self.df_cli_docs['ID'] == int(query)]
        else:
            words = query.split(" ")
            words_stop = ["to", "and", "or"]
            words = list(set(words) - set(words_stop))
            for w in words:
                df_cli_docs_filtred = pd.concat([df_cli_docs_filtred, self.df_cli_docs[self.df_cli_docs['Nome Cliente'].str.contains(w, case=False)]], ignore_index=True)

        df_cli_docs_filtred = df_cli_docs_filtred.drop_duplicates()

        # Limpa a Treeview antes de inserir os resultados
        for item in self.listCliDoc.get_children():
            self.listCliDoc.delete(item)

        # Insere os resultados filtrados
        for index, row in df_cli_docs_filtred.iterrows():
            valores = [row["ID"], row["Nome Cliente"], row["CPF Cliente"], row["Nome Documento"], row["Tipo Documento"], row["Data Gerada"]]
            self.listCliDoc.insert("", "end", iid=row["ID"], values=valores)

    # Função que busca os clientes na treeview
    def busca_cliente(self, event=None):
        query = self.nome_busca_entry.get().strip().lower()
        df2 = self.df_clientes.iloc[:0]  # DataFrame vazio

        if query.isdigit():
            df2 = self.df_clientes[self.df_clientes['ID'] == int(query)]
        else:
            words = query.split(" ")
            words_stop = ["to", "and", "or"]
            words = list(set(words) - set(words_stop))
            for w in words:
                df2 = pd.concat([df2, self.df_clientes[self.df_clientes['Nome'].str.contains(w, case=False)]], ignore_index=True)

        df2 = df2.drop_duplicates()

        # Limpa a Treeview antes de inserir os resultados
        for item in self.listaCli.get_children():
            self.listaCli.delete(item)

        # Insere os resultados filtrados
        for index, row in df2.iterrows():
            valores = [
                row["ID"], row["Nome"], row["Nacionalidade"], row["Estado Civil"], 
                row["Profissão"], row["RG"], row["CPF"], row["CEP"], row["UF"], row["Cidade"], 
                row["Rua"], row["N° Rua"], row["Bairro"], row["Telefone"], row["E-mail"], 
                row["Nome réu"], row["CNPJ réu"]
            ]
            self.listaCli.insert("", "end", iid=row["ID"], values=valores)
    
    # Função para criar a Treeview dos clientes
    def lista_clientes(self):

        # Scroll vertical com mouse
        def _on_mousewheel_vertical(event):
            self.listaCli.yview_scroll(-3 * int(event.delta / 120), "units")
            self.listaCli.bind("<MouseWheel>", _on_mousewheel_vertical)

        # Scroll horizontal com Shift + mouse
        def _on_mousewheel_horizontal(event):
            self.listaCli.xview_scroll(-1 * int(event.delta / 120), "units")
            self.listaCli.bind("<Shift-MouseWheel>", _on_mousewheel_horizontal)

        self.listaCli = ttk.Treeview(self.frame_cliente, height= 3, columns=("col1","col2","col3","col4","col5","col6","col7","col8","col9","col10","col11","col12","col13","col14","col15","col16","col17"), show="headings")

        self.listaCli.heading("#1", text="Código")
        self.listaCli.heading("#2", text="Nome Completo")
        self.listaCli.heading("#3", text="Nacionalidade")
        self.listaCli.heading("#4", text="Estado Civil")
        self.listaCli.heading("#5", text="Profissão")
        self.listaCli.heading("#6", text="RG")
        self.listaCli.heading("#7", text="CPF")
        self.listaCli.heading("#8", text="CEP")
        self.listaCli.heading("#9", text="UF")
        self.listaCli.heading("#10", text="Cidade")
        self.listaCli.heading("#11", text="Rua")
        self.listaCli.heading("#12", text="Nº Rua")
        self.listaCli.heading("#13", text="Bairro")
        self.listaCli.heading("#14", text="Telefone")
        self.listaCli.heading("#15", text="Email")
        self.listaCli.heading("#16", text="Nome Completo Réu")
        self.listaCli.heading("#17", text="CNPJ Réu")

        self.listaCli.column("#1", width=100)
        self.listaCli.column("#2", width=250)
        self.listaCli.column("#3", width=150)
        self.listaCli.column("#4", width=150)
        self.listaCli.column("#5", width=200)
        self.listaCli.column("#6", width=125)
        self.listaCli.column("#7", width=125)
        self.listaCli.column("#8", width=100)
        self.listaCli.column("#9", width=75)
        self.listaCli.column("#10", width=200)
        self.listaCli.column("#11", width=200)
        self.listaCli.column("#12", width=100)
        self.listaCli.column("#13", width=200)
        self.listaCli.column("#14", width=125)
        self.listaCli.column("#15", width=150)
        self.listaCli.column("#16", width=250)
        self.listaCli.column("#17", width=200)
        self.listaCli.place(relx= 0.02, rely=0.51, relwidth=0.95, relheight=0.46)

        # Criando barra de rolagem vertical
        self.scroll_y = ttk.Scrollbar(self.frame_cliente, orient='vertical', command=self.listaCli.yview)
        self.listaCli.configure(yscrollcommand=self.scroll_y.set)
        self.scroll_y.place(relx=0.97, rely=0.51, relwidth=0.02, relheight=0.46)

        # Criando barra de rolagem horizontal
        self.scroll_x = ttk.Scrollbar(self.frame_cliente, orient='horizontal', command=self.listaCli.xview)
        self.listaCli.configure(xscrollcommand=self.scroll_x.set)
        self.scroll_x.place(relx=0.02, rely=0.97, relwidth=0.95, relheight=0.02)

        for index, row in self.df_clientes.iterrows():
            valores = [
                row["ID"], row["Nome"], row["Nacionalidade"], row["Estado Civil"], 
                row["Profissão"], row["RG"], row["CPF"], row["CEP"], row["UF"], row["Cidade"], 
                row["Rua"], row["N° Rua"], row["Bairro"], row["Telefone"], row["E-mail"], 
                row["Nome réu"], row["CNPJ réu"]
            ]
            self.listaCli.insert("", "end", iid=row["ID"], values=valores)
    
    # Função para criar a Treeview dos clientes/documentos
    def lista_clientes_doc(self):
        # Scroll vertical com mouse
        def _on_mousewheel_vertical(event):
            self.listCliDoc.yview_scroll(-3 * int(event.delta / 120), "units")
            self.listCliDoc.bind("<MouseWheel>", _on_mousewheel_vertical)

        # Scroll horizontal com Shift + mouse
        def _on_mousewheel_horizontal(event):
            self.listCliDoc.xview_scroll(-1 * int(event.delta / 120), "units")
            self.listCliDoc.bind("<Shift-MouseWheel>", _on_mousewheel_horizontal)

        self.listCliDoc = ttk.Treeview(self.frame_clientes_doc, height= 3, columns=("col1","col2","col3", "col4", "col5", "col6"), show="headings")

        self.listCliDoc.heading("#1", text="Código")
        self.listCliDoc.heading("#2", text="Nome Cliente")
        self.listCliDoc.heading("#3", text="CPF Cliente")
        self.listCliDoc.heading("#4", text="Nome Documento")
        self.listCliDoc.heading("#5", text="Tipo Documento")
        self.listCliDoc.heading("#6", text="Data Gerada")

        self.listCliDoc.column("#1", width=25)
        self.listCliDoc.column("#2", width=150)
        self.listCliDoc.column("#3", width=100)
        self.listCliDoc.column("#4", width=150)
        self.listCliDoc.column("#5", width=75)
        self.listCliDoc.column("#6", width=75)

        self.listCliDoc.place(relx= 0.02, rely=0.1, relwidth=0.95, relheight=0.6)

        # Criando barra de rolagem vertical
        self.scroll_y = ttk.Scrollbar(self.frame_clientes_doc, orient='vertical', command=self.listCliDoc.yview)
        self.listCliDoc.configure(yscrollcommand=self.scroll_y.set)
        self.scroll_y.place(relx=0.97, rely=0.1, relwidth=0.02, relheight=0.6)

        # Criando barra de rolagem horizontal
        self.scroll_x = ttk.Scrollbar(self.frame_clientes_doc, orient='horizontal', command=self.listCliDoc.xview)
        self.listCliDoc.configure(xscrollcommand=self.scroll_x.set)
        self.scroll_x.place(relx=0.02, rely=0.70, relwidth=0.95, relheight=0.02)

        # Adicionando dados do dataframe a treeview de clientes/documentos
        for index, row in self.df_cli_docs.iterrows():
            valores = [row["ID"], row["Nome Cliente"], row["CPF Cliente"], row["Nome Documento"], row["Tipo Documento"], row["Data Gerada"]]
            self.listCliDoc.insert("", "end", iid=row["ID"], values=valores)

    # Função para criar os widgets da tela de gerenciamento de clientes
    def gerenciar_clientes(self):

        self.df_clientes = pd.read_excel(r"C:\Users\dudu\Documents\CLIENTES WEB\sistema_advogados\Projeto\Base de dados.xlsx")
        
        # Estilo para aumentar a fonte dos Entry
        style = ttk.Style()
        style.configure("Big.TEntry", font=("Helvetica", 20))

        # Criação LABEL e ENTRADA do nome completo
        self.lb_nome = ttk.Label(self.frame_cliente, text = "Nome Completo*")
        self.lb_nome.place(relx= 0.04, rely=0.02)

        self.nome_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.nome_entry.place(relx= 0.03, rely=0.05, relwidth=0.4)

        # Criação LABEL, LISTA DE ENTRADAS e COMBOBOX da nacionalidade
        self.lb_nacionalidade = ttk.Label(self.frame_cliente, text = "Nacionalidade*")
        self.lb_nacionalidade.place(relx= 0.47, rely=0.02)

        opc_nacionalidade = ["afegão", "afegã", "albanês", "albanesa", "alemão", "alemã", "americano", "americana", "andorrano", "andorrana", "angolano", "angolana", "antiguano", "antiguana", "argentino", "argentina", "armênio", "armênia", "australiano", "australiana", "austríaco", "austríaca", "azerbaijano", "azerbaijana", "bahamense", "bangladeshiano", "bangladeshiana", "barbadiano", "barbadiana", "belga", "belizenho", "belizenha", "beninense", "bielorrusso", "bielorrussa", "boliviano", "boliviana", "bósnio", "bósnia", "botsuanês", "botsuanesa", "brasileiro", "brasileira", "britânico", "britânica", "búlgaro", "búlgara", "burquinense", "burundês", "burundesa", "butanês", "butanesa", "cabo-verdiano", "cabo-verdiana", "camaronês", "camaronesa", "cambojano", "cambojana", "canadense", "catariano", "catarina", "chileno", "chilena", "chinês", "chinesa", "cingapuriano", "cingapuriana", "colombiano", "colombiana", "congolês", "congolesa", "coreano do norte", "coreana do norte", "coreano do sul", "coreana do sul", "costarriquenho", "costarriquenha", "croata", "cubano", "cubana", "dinamarquês", "dinamarquesa", "dominicano", "dominicana", "egípcio", "egípcia", "equatoriano", "equatoriana", "eritreu", "eritreia", "escocês", "escocesa", "eslovaco", "eslovaca", "esloveno", "eslovena", "espanhol", "espanhola", "estoniano", "estoniana", "etíope", "filipino", "filipina", "finlandês", "finlandesa", "francês", "francesa", "gabonês", "gabonesa", "galês", "galesa", "ganês", "ganesa", "georgiano", "georgiana", "grego", "grega", "guatemalteco", "guatemalteca", "guianês", "guianesa", "guineense", "haitiano", "haitiana", "holandês", "holandesa", "hondurenho", "hondurenha", "húngaro", "húngara", "iemenita", "indiano", "indiana", "indonésio", "indonésia", "inglês", "inglesa", "iraquiano", "iraquiana", "iraniano", "iraniana", "irlandês", "irlandesa", "islandês", "islandesa", "israelense", "italiano", "italiana", "jamaicano", "jamaicana", "japonês", "japonesa", "jordano", "jordana", "kazakhstanês", "kazakhstanesa", "keniano", "keniana", "kiribati", "kuwaitiano", "kuwaitiana", "letão", "letona", "libanês", "libanesa", "liberiano", "liberiana", "líbio", "líbia", "liechtensteiniano", "liechtensteiniana", "lituano", "lituana", "luxemburguês", "luxemburguesa", "macedônio", "macedônia", "malaio", "malaia", "malawiano", "malawiana", "maliano", "maliana", "maltês", "maltesa", "marroquino", "marroquina", "mauriciano", "mauriciana", "mexicano", "mexicana", "moçambicano", "moçambicana", "moldávio", "moldávia", "monegasco", "monegasca", "mongol", "montenegrino", "montenegrina", "namibiano", "namibiana", "nepalês", "nepalesa", "nicaraguense", "nigeriano", "nigeriana", "norueguês", "norueguesa", "neozelandês", "neozelandesa", "omanês", "omanesa", "paquistanês", "paquistanesa", "palestino", "palestina", "panamenho", "panamenha", "papua nova guiné", "paraguaio", "paraguaia", "peruano", "peruana", "polonês", "polonesa", "portorriquenho", "portorriquenha", "português", "portuguesa", "qatari", "qatari", "queniano", "queniana", "quirguiz", "quirguiz", "romeno", "romena", "ruandês", "ruandesa", "russo", "russa", "salvadorenho", "salvadorenha", "samoano", "samoana", "sanmarinense", "sanmarinense", "saudita", "saudita", "senegalês", "senegalesa", "sérvio", "sérvia", "somaliano", "somaliana", "sudanês", "sudanesa", "sueco", "sueca", "suíço", "suíça", "surinamês", "surinamesa", "tailandês", "tailandesa", "tanzaniano", "tanzaniana", "timorense", "timorense", "togolês", "togolesa", "turco", "turca", "turcomano", "turcomana", "ucraniano", "ucraniana", "ugandês", "ugandesa", "uruguaio", "uruguaia", "uzbeque", "uzbeque", "venezuelano", "venezuelana", "vietnamita", "vietnamita", "zambiano", "zambiana", "zimbabuano", "zimbabuana"]

        self.nacionalidade_combo = SearchableComboBox(self.frame_cliente, opc_nacionalidade, 0.46, 0.05, 0.15)

        # Criação LABEL, LISTA DE ENTRADAS e COMBOBOX do estado civil
        self.lb_estado_civil = ttk.Label(self.frame_cliente, text = "Estado Civil*")
        self.lb_estado_civil.place(relx= 0.65, rely=0.02)

        opc_estado_civil = ["solteiro", "solteira", "casado", "casada", "divorciado", "divorciada", "viúvo", "viúva", "separado", "separada", "união estável", "separação judicial"]

        self.estado_civil_combo = SearchableComboBox(self.frame_cliente, opc_estado_civil, 0.64, 0.05, 0.15)

        # Criação LABEL e ENTRADA da profissão
        self.lb_profissao = ttk.Label(self.frame_cliente, text = "Profissão*")
        self.lb_profissao.place(relx= 0.83, rely=0.02)

        self.profissao_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.profissao_entry.place(relx= 0.82, rely=0.05, relwidth=0.15)

        # Criação LABEL e ENTRADA da rg
        self.lb_rg = ttk.Label(self.frame_cliente, text = "RG*")
        self.lb_rg.place(relx= 0.04, rely=0.11)

        self.rg_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.rg_entry.place(relx= 0.03, rely=0.14, relwidth=0.15)

        # Criação LABEL e ENTRADA da cpf
        self.lb_cpf = ttk.Label(self.frame_cliente, text = "CPF*")
        self.lb_cpf.place(relx= 0.22, rely=0.11)

        self.cpf_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cpf_entry.place(relx= 0.21, rely=0.14, relwidth=0.15)
        # Criação LABEL e ENTRADA da cep
        self.lb_cep = ttk.Label(self.frame_cliente, text = "CEP*")
        self.lb_cep.place(relx= 0.40, rely=0.11)

        self.cep_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cep_entry.place(relx= 0.39, rely=0.14, relwidth=0.15)

        # Criação LABEL, LISTA DE ENTRADAS e COMBOBOX da uf
        self.lb_uf = ttk.Label(self.frame_cliente, text = "UF*")
        self.lb_uf.place(relx= 0.58, rely=0.11)

        self.uf_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.uf_entry.place(relx= 0.57, rely=0.14, relwidth=0.05)

        # Criação LABEL e ENTRADA da cidade
        self.lb_cidade = ttk.Label(self.frame_cliente, text = "Cidade*")
        self.lb_cidade.place(relx= 0.66, rely=0.11)

        self.cidade_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cidade_entry.place(relx= 0.65, rely=0.14, relwidth=0.18)

        # Criação LABEL e ENTRADA da rua
        self.lb_rua = ttk.Label(self.frame_cliente, text = "Rua*")
        self.lb_rua.place(relx= 0.04, rely=0.20)

        self.rua_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.rua_entry.place(relx= 0.03, rely=0.23, relwidth=0.3)

        # Criação LABEL e ENTRADA do numero rua
        self.lb_n_rua = ttk.Label(self.frame_cliente, text = "Nº Rua*")
        self.lb_n_rua.place(relx= 0.37, rely=0.20)

        self.n_rua_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.n_rua_entry.place(relx= 0.36, rely=0.23, relwidth=0.1)

        # Criação LABEL e ENTRADA do bairro
        self.lb_bairro = ttk.Label(self.frame_cliente, text = "Bairro*")
        self.lb_bairro.place(relx= 0.50, rely=0.20)

        self.bairro_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.bairro_entry.place(relx= 0.49, rely=0.23, relwidth=0.25)

        # Criação LABEL e ENTRADA do telefone
        self.lb_telefone = ttk.Label(self.frame_cliente, text = "Telefone")
        self.lb_telefone.place(relx= 0.78, rely=0.20)

        self.telefone_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.telefone_entry.place(relx= 0.77, rely=0.23, relwidth=0.15)

        # Criação LABEL e ENTRADA do email
        self.lb_email = ttk.Label(self.frame_cliente, text = "Email")
        self.lb_email.place(relx= 0.04, rely=0.29)

        self.email_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.email_entry.place(relx= 0.03, rely=0.32, relwidth=0.25)

        # Criação LABEL e ENTRADA do nome réu
        self.lb_nome_reu = ttk.Label(self.frame_cliente, text = "Nome Completo Réu")
        self.lb_nome_reu.place(relx= 0.32, rely=0.29)

        self.nome_reu_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.nome_reu_entry.place(relx= 0.31, rely=0.32, relwidth=0.4)

        # Criação LABEL e ENTRADA do cnpj réu
        self.lb_cnpj_reu = ttk.Label(self.frame_cliente, text = "CNPJ/CPF Réu")
        self.lb_cnpj_reu.place(relx= 0.75, rely=0.29)

        self.cnpj_reu_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cnpj_reu_entry.place(relx= 0.74, rely=0.32, relwidth=0.23)

        # Criação botão adicionar cliente
        self.bt_add_cliente = ttk.Button(self.frame_cliente, text="Adicionar Cliente", style='Accent.TButton')
        self.bt_add_cliente.place(relx= 0.03, rely=0.44, relwidth=0.17)

        # Criação botão atualizar cliente
        self.bt_update_cliente = ttk.Button(self.frame_cliente, text="Atualizar Cliente", style='Accent.TButton')
        self.bt_update_cliente.place(relx= 0.23, rely=0.44, relwidth=0.17)

        # Criação botão deletar cliente
        self.bt_del_cliente = ttk.Button(self.frame_cliente, text="Deletar Cliente", style='Accent.TButton')
        self.bt_del_cliente.place(relx= 0.43, rely=0.44, relwidth=0.17)

        # Criação LABEL e ENTRADA do nome para buscar cliente
        self.lb_nome_busca = ttk.Label(self.frame_cliente, text = "Buscar por nome/CPF")
        self.lb_nome_busca.place(relx= 0.67, rely=0.41)

        self.nome_busca_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.nome_busca_entry.place(relx= 0.66, rely=0.44, relwidth=0.30)
        self.nome_busca_entry.bind("<KeyRelease>", lambda event: self.busca_cliente())

        # Criação botão limpar 
        self.bt_limpar = ttk.Button(self.frame_cliente, text="Limpar", command=self.limpa_tela)
        self.bt_limpar.place(relx= 0.05, rely=0.38, relwidth=0.13)

        self.lista_clientes()
    
    # Função para criar os widgets da tela de gerenciamento de documentos
    def gerenciar_documentos(self):
        # Adicionando carregamento do dataframe de documentos
        self.df_docs = pd.read_excel(r"C:\Users\dudu\Documents\CLIENTES WEB\sistema_advogados\Projeto\Base de dados docs.xlsx")

        # Estilo para aumentar a fonte dos Entry
        style = ttk.Style()
        style.configure("Big.TEntry", font=("Helvetica", 20))

        # Criando o LABEL E ENTRY do nome do documento
        self.lb_nome_doc = ttk.Label(self.frame_documento, text="Nome do Documento*")
        self.lb_nome_doc.place(relx= 0.04, rely=0.02)

        self.nome_doc_entry = ttk.Entry(self.frame_documento, style="Big.TEntry")
        self.nome_doc_entry.place(relx= 0.03, rely=0.05, relwidth=0.4)

        # Criação LABEL, LISTA DE ENTRADAS e COMBOBOX do tipo
        self.lb_tipo = ttk.Label(self.frame_documento, text = "Tipo*")
        self.lb_tipo.place(relx= 0.47, rely=0.02)

        opc_tipo = ["Contrato", "Declaração", "Petição", "Tese", "Procuração"]
        self.tipo_combo = SearchableComboBox(self.frame_documento, opc_tipo, 0.46, 0.05, 0.15)

        # Criando a LABEL e ENTRY do caminho do documento
        self.lb_texto_caminho_doc = ttk.Label(self.frame_documento, text="Caminho do documento*: ")
        self.lb_texto_caminho_doc.place(relx= 0.04, rely=0.12)

        self.caminho_doc_entry = ttk.Entry(self.frame_documento, style="Big.TEntry")
        self.caminho_doc_entry.place(relx= 0.22, rely=0.11, relwidth=0.57)

        # Criando o botão de escolher documento no explorer
        self.btn_escolher_doc = ttk.Button(self.frame_documento, text="Escolher Arquivo", command=self.escolher_arquivo)
        self.btn_escolher_doc.place(relx= 0.8, rely=0.11, relwidth=0.17)

        # Criação botão adicionar documento
        self.bt_add_documento = ttk.Button(self.frame_documento, text="Adicionar Documento", style='Accent.TButton')
        self.bt_add_documento.place(relx= 0.03, rely=0.2, relwidth=0.17)

        # Criação botão deletar documento
        self.bt_del_documento = ttk.Button(self.frame_documento, text="Deletar Documento", style='Accent.TButton')
        self.bt_del_documento.place(relx= 0.23, rely=0.2, relwidth=0.17)

        # Criando o LABEL E ENTRY da pesquisa por nome do documento
        self.lb_nome_doc_busca = ttk.Label(self.frame_documento, text="Buscar por nome")
        self.lb_nome_doc_busca.place(relx= 0.51, rely=0.17)

        self.nome_doc_busca_entry = ttk.Entry(self.frame_documento, style="Big.TEntry")
        self.nome_doc_busca_entry.place(relx= 0.5, rely=0.2, relwidth=0.4)

        self.nome_doc_busca_entry.bind("<KeyRelease>", lambda event: self.busca_documentos())

        self.lista_documentos()
    
    # Função para criar os widgets da tela de clientes/documentos
    def clientes_doc(self):

        self.df_cli_docs = pd.read_excel(r"C:\Users\dudu\Documents\CLIENTES WEB\sistema_advogados\Projeto\Base de dados cli-docs.xlsx")

        #Criando a LABEL e ENTRY da busca por cliente
        self.lb_doc_busca = ttk.Label(self.frame_clientes_doc, text="Pesquisar por cliente")
        self.lb_doc_busca.place(relx= 0.04, rely=0.02)

        self.doc_busca_entry = ttk.Entry(self.frame_clientes_doc, style="Big.TEntry")
        self.doc_busca_entry.place(relx= 0.03, rely=0.05, relwidth=0.4)

        self.doc_busca_entry.bind("<KeyRelease>", lambda event: self.busca_clientes_doc())

        self.lista_clientes_doc()

        # Criação botão deletar registro
        self.bt_del_registro = ttk.Button(self.frame_clientes_doc, text="Deletar Registro", style='Accent.TButton')
        self.bt_del_registro.place(relx= 0.02, rely=0.75, relwidth=0.17)

        # Criação botão exportar word
        self.bt_export_word = ttk.Button(self.frame_clientes_doc, text="Exportar Word", style='Accent.TButton')
        self.bt_export_word.place(relx= 0.60, rely=0.75, relwidth=0.17)

        # Criação botão exportar pdf
        self.bt_export_pdf = ttk.Button(self.frame_clientes_doc, text="Exportar PDF", style='Accent.TButton')
        self.bt_export_pdf.place(relx= 0.80, rely=0.75, relwidth=0.17)



class App(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        root.mainloop()

    def tela(self):
        self.root.title("Sistema Advogados")
        sv_ttk.set_theme("light") 
        self.root.geometry("1280x1024")
        self.root.resizable(True, True)
        self.root.maxsize(width=1440, height=900)
        self.root.minsize(width=1024, height=768)

    def frames_da_tela(self):
        self.frame_menu = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_menu.place(relx= 0.02, rely=0.02, relwidth=0.2, relheight=0.96)

        self.frame_2 = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_2.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

        self.frame_cliente = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_cliente.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

        self.frame_documento = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_documento.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

        self.frame_clientes_doc = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_clientes_doc.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

    def widgets_frame1(self):
        self.img = PhotoImage(file="logo.png")
        self.img_logo = Label(self.frame_menu, image=self.img)
        self.img_logo.place(relx= 0.1, rely=0.02, relwidth=0.8, relheight=0.33)

        self.bt_clientes = ttk.Button(self.frame_menu, text="Gerenciar Clientes", command=lambda: [self.gerenciar_clientes(), self.frame_cliente.lift()])
        self.bt_clientes.place(relx= 0.05, rely=0.37, relwidth=0.9, relheight=0.05)

        self.bt_documentos = ttk.Button(self.frame_menu, text="Gerenciar Documentos", command=lambda: [self.gerenciar_documentos(), self.frame_documento.lift()])
        self.bt_documentos.place(relx= 0.05, rely=0.44, relwidth=0.9, relheight=0.05)

        self.bt_clientes_doc = ttk.Button(self.frame_menu, text="Clientes/Documentos", command=lambda: [self.clientes_doc(), self.frame_clientes_doc.lift()])
        self.bt_clientes_doc.place(relx= 0.05, rely=0.51, relwidth=0.9, relheight=0.05)

        self.bt_contratos = ttk.Button(self.frame_menu, text="Gerar Contratos/Declarações")
        self.bt_contratos.place(relx= 0.05, rely=0.58, relwidth=0.9, relheight=0.05)

        self.bt_peticao = ttk.Button(self.frame_menu, text="Gerar Petição")
        self.bt_peticao.place(relx= 0.05, rely=0.65, relwidth=0.9, relheight=0.05)

        self.bt_sair = ttk.Button(self.frame_menu, text="Sair", command=self.root.destroy, style='Accent.TButton')
        self.bt_sair.place(relx= 0.05, rely=0.93, relwidth=0.9, relheight=0.05)

App()