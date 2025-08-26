from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import sv_ttk
import darkdetect

root = Tk()

class SearchableComboBox():
    def __init__(self, parent, options) -> None:  # << agora recebe parent
        self.dropdown_id = None
        self.options = options

        # Create a Text widget for the entry field
        wrapper = ttk.Frame(parent)  # << usa o parent, não root
        wrapper.place(relx=0.45, rely=0.05, relwidth=0.15)  # posiciona no frame certo

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
    def gerenciar_clientes(self):
        #Criação LABEL e ENTRADA do nome completo
        self.lb_nome = ttk.Label(self.frame_2, text = "Nome Completo*")
        self.lb_nome.place(relx= 0.03, rely=0.02)

        self.nome_entry = ttk.Entry(self.frame_2)
        self.nome_entry.place(relx= 0.02, rely=0.05, relwidth=0.4)

        #Criação LABEL e LISTA DE ENTRADAS da nacionalidade
        self.lb_nacionalidade = ttk.Label(self.frame_2, text = "Nacionalidade*")
        self.lb_nacionalidade.place(relx= 0.46, rely=0.02)

        opc_nacionalidade = ["", "afegão", "afegã", "albanês", "albanesa", "alemão", "alemã", "americano", "americana", "andorrano", "andorrana", "angolano", "angolana", "antiguano", "antiguana", "argentino", "argentina", "armênio", "armênia", "australiano", "australiana", "austríaco", "austríaca", "azerbaijano", "azerbaijana", "bahamense", "bangladeshiano", "bangladeshiana", "barbadiano", "barbadiana", "belga", "belizenho", "belizenha", "beninense", "bielorrusso", "bielorrussa", "boliviano", "boliviana", "bósnio", "bósnia", "botsuanês", "botsuanesa", "brasileiro", "brasileira", "britânico", "britânica", "búlgaro", "búlgara", "burquinense", "burundês", "burundesa", "butanês", "butanesa", "cabo-verdiano", "cabo-verdiana", "camaronês", "camaronesa", "cambojano", "cambojana", "canadense", "catariano", "catarina", "chileno", "chilena", "chinês", "chinesa", "cingapuriano", "cingapuriana", "colombiano", "colombiana", "congolês", "congolesa", "coreano do norte", "coreana do norte", "coreano do sul", "coreana do sul", "costarriquenho", "costarriquenha", "croata", "cubano", "cubana", "dinamarquês", "dinamarquesa", "dominicano", "dominicana", "egípcio", "egípcia", "equatoriano", "equatoriana", "eritreu", "eritreia", "escocês", "escocesa", "eslovaco", "eslovaca", "esloveno", "eslovena", "espanhol", "espanhola", "estoniano", "estoniana", "etíope", "filipino", "filipina", "finlandês", "finlandesa", "francês", "francesa", "gabonês", "gabonesa", "galês", "galesa", "ganês", "ganesa", "georgiano", "georgiana", "grego", "grega", "guatemalteco", "guatemalteca", "guianês", "guianesa", "guineense", "haitiano", "haitiana", "holandês", "holandesa", "hondurenho", "hondurenha", "húngaro", "húngara", "iemenita", "indiano", "indiana", "indonésio", "indonésia", "inglês", "inglesa", "iraquiano", "iraquiana", "iraniano", "iraniana", "irlandês", "irlandesa", "islandês", "islandesa", "israelense", "italiano", "italiana", "jamaicano", "jamaicana", "japonês", "japonesa", "jordano", "jordana", "kazakhstanês", "kazakhstanesa", "keniano", "keniana", "kiribati", "kuwaitiano", "kuwaitiana", "letão", "letona", "libanês", "libanesa", "liberiano", "liberiana", "líbio", "líbia", "liechtensteiniano", "liechtensteiniana", "lituano", "lituana", "luxemburguês", "luxemburguesa", "macedônio", "macedônia", "malaio", "malaia", "malawiano", "malawiana", "maliano", "maliana", "maltês", "maltesa", "marroquino", "marroquina", "mauriciano", "mauriciana", "mexicano", "mexicana", "moçambicano", "moçambicana", "moldávio", "moldávia", "monegasco", "monegasca", "mongol", "montenegrino", "montenegrina", "namibiano", "namibiana", "nepalês", "nepalesa", "nicaraguense", "nigeriano", "nigeriana", "norueguês", "norueguesa", "neozelandês", "neozelandesa", "omanês", "omanesa", "paquistanês", "paquistanesa", "palestino", "palestina", "panamenho", "panamenha", "papua nova guiné", "paraguaio", "paraguaia", "peruano", "peruana", "polonês", "polonesa", "portorriquenho", "portorriquenha", "português", "portuguesa", "qatari", "qatari", "queniano", "queniana", "quirguiz", "quirguiz", "romeno", "romena", "ruandês", "ruandesa", "russo", "russa", "salvadorenho", "salvadorenha", "samoano", "samoana", "sanmarinense", "sanmarinense", "saudita", "saudita", "senegalês", "senegalesa", "sérvio", "sérvia", "somaliano", "somaliana", "sudanês", "sudanesa", "sueco", "sueca", "suíço", "suíça", "surinamês", "surinamesa", "tailandês", "tailandesa", "tanzaniano", "tanzaniana", "timorense", "timorense", "togolês", "togolesa", "turco", "turca", "turcomano", "turcomana", "ucraniano", "ucraniana", "ugandês", "ugandesa", "uruguaio", "uruguaia", "uzbeque", "uzbeque", "venezuelano", "venezuelana", "vietnamita", "vietnamita", "zambiano", "zambiana", "zimbabuano", "zimbabuana"]

        self.nacionalidade_combo = SearchableComboBox(self.frame_2, opc_nacionalidade)

class App(Funcs):        

    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        root.mainloop()

    def tela(self):
        self.root.title("Cadastro de Clientes")
        sv_ttk.set_theme("light") 
        self.root.geometry("1280x1024")
        self.root.resizable(True, True)
        self.root.maxsize(width=1440, height=900)
        self.root.minsize(width=1024, height=768)

    def frames_da_tela(self):
        self.frame_1 = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth=0.2, relheight=0.96)

        self.frame_2 = ttk.Frame(self.root, style='Card.TFrame')
        self.frame_2.place(relx= 0.24, rely=0.02, relwidth=0.74, relheight=0.96)

    def widgets_frame1(self):
        self.img = PhotoImage(file="logo.png")
        self.img_logo = Label(self.frame_1, image=self.img)
        self.img_logo.place(relx= 0.1, rely=0.02, relwidth=0.8, relheight=0.33)

        self.bt_clientes = ttk.Button(self.frame_1, text="Gerenciar Clientes", command=self.gerenciar_clientes)
        self.bt_clientes.place(relx= 0.05, rely=0.37, relwidth=0.9, relheight=0.05)

        self.bt_documentos = ttk.Button(self.frame_1, text="Gerenciar Documentos")
        self.bt_documentos.place(relx= 0.05, rely=0.44, relwidth=0.9, relheight=0.05)

        self.bt_contratos = ttk.Button(self.frame_1, text="Gerar Contratos/Declarações")
        self.bt_contratos.place(relx= 0.05, rely=0.51, relwidth=0.9, relheight=0.05)

        self.bt_peticao = ttk.Button(self.frame_1, text="Gerar Petição")
        self.bt_peticao.place(relx= 0.05, rely=0.58, relwidth=0.9, relheight=0.05)

        self.bt_peticao = ttk.Button(self.frame_1, text="Gerar Petição")
        self.bt_peticao.place(relx= 0.05, rely=0.58, relwidth=0.9, relheight=0.05)

        self.bt_sair = ttk.Button(self.frame_1, text="Sair", command=self.root.destroy, style='Accent.TButton')
        self.bt_sair.place(relx= 0.05, rely=0.93, relwidth=0.9, relheight=0.05)

App()