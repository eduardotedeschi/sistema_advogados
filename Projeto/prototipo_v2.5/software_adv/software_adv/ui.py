import tkinter as tk
from tkinter import ttk, messagebox, filedialog, END
import sv_ttk

from software_adv import services, db, utils
from software_adv.autocomplete import AutocompleteEntry


class App:
    def __init__(self, root):
        self.root = root
        self.tela()

        self.montar_tela_clientes()
        self.montar_tela_documentos()

    def tela(self):
        #Configurações da tela
        self.root.title("Sistema Advogados")
        sv_ttk.set_theme("light") 
        self.root.geometry("1280x1024")
        self.root.resizable(True, True)
        self.root.maxsize(width=1440, height=900)
        self.root.minsize(width=1024, height=768)
    
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
    
    # ==============================
    # CLIENTES
    # ==============================
    def montar_tela_clientes(self):
        self.frame_clientes_doc = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_clientes_doc.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

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
        self.nacionalidade_combo = AutocompleteEntry(opc_nacionalidade, self.frame_cliente, style="Big.TEntry", listboxLength=6, width=23, matchesFunction=self.matches)
        self.nacionalidade_combo.place(relx=0.44, rely=0.05, relwidth=0.13)

        #Label e Combobox do estado civil
        self.lb_estado_civil = ttk.Label(self.frame_cliente, text = "Estado Civil*")
        self.lb_estado_civil.place(relx= 0.61, rely=0.02)
        opc_estado_civil = ["solteiro", "solteira", "casado", "casada", "divorciado", "divorciada", "viúvo", "viúva", "separado", "separada", "união estável", "separação judicial"]
        self.estado_civil_combo = AutocompleteEntry(opc_estado_civil, self.frame_cliente, style="Big.TEntry", listboxLength=6, width=23, matchesFunction=self.matches)
        self.estado_civil_combo.place(relx=0.6, rely=0.05, relwidth=0.12)

        #Label e Entry da profissão
        self.lb_profissao = ttk.Label(self.frame_cliente, text = "Profissão*")
        self.lb_profissao.place(relx= 0.76, rely=0.02)
        self.profissao_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.profissao_entry.place(relx= 0.75, rely=0.05, relwidth=0.22)

        #Label e Entry do RG
        self.lb_rg = ttk.Label(self.frame_cliente, text = "RG*")
        self.lb_rg.place(relx= 0.04, rely=0.11)
        self.rg_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.rg_entry.place(relx= 0.03, rely=0.14, relwidth=0.15)
        self.rg_entry.bind("<KeyRelease>", self.valida_rg)

        #Label e Entry do CPF
        self.lb_cpf = ttk.Label(self.frame_cliente, text = "CPF*")
        self.lb_cpf.place(relx= 0.22, rely=0.11)
        self.cpf_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cpf_entry.place(relx= 0.21, rely=0.14, relwidth=0.15)
        self.cpf_entry.bind("<KeyRelease>", self.valida_cpf)

        #Label e Entry do CEP
        self.lb_cep = ttk.Label(self.frame_cliente, text = "CEP*")
        self.lb_cep.place(relx= 0.40, rely=0.11)
        self.cep_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cep_entry.place(relx= 0.39, rely=0.14, relwidth=0.15)
        self.cep_entry.bind("<KeyRelease>", self.cepCorreios)

        #Label e Entry da UF
        self.lb_uf = ttk.Label(self.frame_cliente, text = "UF*")
        self.lb_uf.place(relx= 0.58, rely=0.11)
        self.uf_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.uf_entry.place(relx= 0.57, rely=0.14, relwidth=0.05)

        #Label e Entry da cidade
        self.lb_cidade = ttk.Label(self.frame_cliente, text = "Cidade*")
        self.lb_cidade.place(relx= 0.66, rely=0.11)
        self.cidade_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.cidade_entry.place(relx= 0.65, rely=0.14, relwidth=0.32)

        #Label e Entry da rua
        self.lb_rua = ttk.Label(self.frame_cliente, text = "Rua*")
        self.lb_rua.place(relx= 0.04, rely=0.20)
        self.rua_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.rua_entry.place(relx= 0.03, rely=0.23, relwidth=0.31)

        #Label e Entry do numero da rua
        self.lb_n_rua = ttk.Label(self.frame_cliente, text = "Nº Rua*")
        self.lb_n_rua.place(relx= 0.38, rely=0.20)
        self.n_rua_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.n_rua_entry.place(relx= 0.37, rely=0.23, relwidth=0.1)

        #Label e Entry do bairro
        self.lb_bairro = ttk.Label(self.frame_cliente, text = "Bairro*")
        self.lb_bairro.place(relx= 0.51, rely=0.20)
        self.bairro_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.bairro_entry.place(relx= 0.5, rely=0.23, relwidth=0.31)

        #Label e Entry do telefone
        self.lb_telefone = ttk.Label(self.frame_cliente, text = "Telefone")
        self.lb_telefone.place(relx= 0.85, rely=0.20)
        self.telefone_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.telefone_entry.place(relx= 0.84, rely=0.23, relwidth=0.13)

        #Label e Entry do email
        self.lb_email = ttk.Label(self.frame_cliente, text = "Email")
        self.lb_email.place(relx= 0.04, rely=0.29)
        self.email_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.email_entry.place(relx= 0.03, rely=0.32, relwidth=0.25)
        self.email_entry.bind("<KeyRelease>", self.valida_email)

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
        self.cnpj_reu_entry.bind("<KeyRelease>", self.valida_cpf_cnpj)

        #Botão adicionar cliente
        self.bt_add_cliente = ttk.Button(self.frame_cliente, text="Adicionar Cliente", style='Accent.TButton', command=self.add_cliente)
        self.bt_add_cliente.place(relx= 0.03, rely=0.44, relwidth=0.17)

        #Botão update cliente
        self.bt_update_cliente = ttk.Button(self.frame_cliente, text="Atualizar Cliente", style='Accent.TButton', command=self.upt_cliente)
        self.bt_update_cliente.place(relx= 0.23, rely=0.44, relwidth=0.17)

        #Botão deletar cliente
        self.bt_del_cliente = ttk.Button(self.frame_cliente, text="Deletar Cliente", style='Accent.TButton', command=lambda: self.del_cliente(None))
        self.bt_del_cliente.place(relx= 0.43, rely=0.44, relwidth=0.17)

        #Label e Entry da pesquisa por nome ou cpf do cliente
        self.lb_nome_busca = ttk.Label(self.frame_cliente, text = "Buscar nome/CPF")
        self.lb_nome_busca.place(relx= 0.67, rely=0.41)
        self.nome_busca_entry = ttk.Entry(self.frame_cliente, style="Big.TEntry")
        self.nome_busca_entry.place(relx= 0.66, rely=0.44, relwidth=0.31)
        self.nome_busca_entry.bind("<KeyRelease>", lambda event: self.busca_cliente(self.nome_busca_entry ,self.listaCli, event))

        #Botão limpar campos
        self.bt_limpar = ttk.Button(self.frame_cliente, text="Limpar", command=self.limpa_cliente)
        self.bt_limpar.place(relx= 0.84, rely=0.38, relwidth=0.11)

        #Criação da Treeview
        self.lista_clientes()
        services.select_listaClientes(self.listaCli)
        utils.setup_enter_bindings("frame_cliente")
        self.listaCli.bind("<Delete>", self.del_cliente)
        self.listaCli.bind("<BackSpace>", self.del_cliente) 

    def lista_clientes(self):
        #Declaração dos parâmetros
        colunas = ("col1","col2","col3","col4","col5","col6","col7","col8","col9","col10","col11","col12","col13","col14","col15","col16","col17")
        cabecalhos = ("ID", "Nome Completo", "Nacionalidade", "Estado Civil", "Profissão", "RG", "CPF", "CEP", "UF", "Cidade", "Rua", "Nº Rua", "Bairro", "Telefone", "Email", "Nome Completo Réu", "CNPJ Réu")
        larguras = (35, 250, 100, 110, 200, 100, 110, 85, 40, 150, 220, 150, 200, 110, 230, 400, 130)
        relx, rely, relwidth, relheight = 0.02, 0.51, 0.95, 0.46
        
        self.listaCli = self.criar_treeview_generica(self.frame_cliente, colunas, cabecalhos, larguras, relx, rely, relwidth, relheight)

        self.listaCli.bind("<Double-1>", utils.OnDoubleClick_Cli)

    # ==============================
    # DOCUMENTOS
    # ==============================
    def montar_tela_documentos(self):
        frm = self.frame_documentos

        self.doc_nome_var = tk.StringVar()
        self.doc_tipo_var = tk.StringVar()

        ttk.Label(frm, text="Nome:").pack()
        ttk.Entry(frm, textvariable=self.doc_nome_var).pack()
        ttk.Label(frm, text="Tipo:").pack()
        ttk.Entry(frm, textvariable=self.doc_tipo_var).pack()
        ttk.Button(frm, text="Selecionar Arquivo", command=self.selecionar_arquivo).pack()
        ttk.Button(frm, text="Adicionar Documento", command=self.add_documento).pack()

        self.lista_docs = ttk.Treeview(frm, columns=("id", "nome", "tipo"), show="headings")
        for col in ("id", "nome", "tipo"):
            self.lista_docs.heading(col, text=col.capitalize())
        self.lista_docs.pack(fill="both", expand=True)

        self.atualizar_lista_documentos()

    def selecionar_arquivo(self):
        self.caminho_doc = filedialog.askopenfilename(
            title="Selecione um documento",
            filetypes=[("Word", "*.docx"), ("Todos", "*.*")]
        )

    def add_documento(self):
        ok, msg = services.add_documento(
            self.doc_nome_var.get(), self.doc_tipo_var.get(), self.caminho_doc
        )
        messagebox.showinfo("Info", msg)
        self.atualizar_lista_documentos()

    def atualizar_lista_documentos(self):
        for i in self.lista_docs.get_children():
            self.lista_docs.delete(i)
        for d in services.listar_documentos():
            self.lista_docs.insert("", END, values=d)
