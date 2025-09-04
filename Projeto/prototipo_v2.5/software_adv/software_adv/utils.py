import re
from tkinter import END

def valida_email(email: str) -> bool:
    regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(regex.fullmatch(email.strip()))

def valida_rg(rg: str) -> bool:
    rg_limpo = re.sub(r'\D', '', rg)
    return len(rg_limpo) == 9

def valida_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (11 - soma % 11) if soma % 11 >= 2 else 0
    if dig1 != int(cpf[9]): return False
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (11 - soma % 11) if soma % 11 >= 2 else 0
    return dig2 == int(cpf[10])

def valida_cnpj(cnpj: str) -> bool:
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    soma = 0
    mult = 5
    for i in range(12):
        soma += int(cnpj[i]) * mult
        mult -= 1
        if mult < 2: mult = 9
    dig1 = 0 if soma % 11 < 2 else 11 - (soma % 11)
    if int(cnpj[12]) != dig1: return False
    soma = 0
    mult = 6
    for i in range(13):
        soma += int(cnpj[i]) * mult
        mult -= 1
        if mult < 2: mult = 9
    dig2 = 0 if soma % 11 < 2 else 11 - (soma % 11)
    return int(cnpj[13]) == dig2

# Máscaras
def formatar_cpf(cpf: str) -> str:
    cpf = re.sub(r'\D', '', cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf

def formatar_cnpj(cnpj: str) -> str:
    cnpj = re.sub(r'\D', '', cnpj)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}" if len(cnpj) == 14 else cnpj

def formatar_cep(cep: str) -> str:
    cep = re.sub(r'\D', '', cep)
    return f"{cep[:5]}-{cep[5:]}" if len(cep) == 8 else cep

def formatar_telefone(tel: str) -> str:
    tel = re.sub(r'\D', '', tel)
    if len(tel) == 11:
        return f"({tel[:2]}) {tel[2:7]}-{tel[7:]}"
    elif len(tel) == 10:
        return f"({tel[:2]}) {tel[2:6]}-{tel[6:]}"
    return tel

def OnDoubleClick_Cli(self, event):
    self.limpa_cliente()
    self.listaCli.selection()

    for n in self.listaCli.selection():
        col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14,col15,col16,col17 = self.listaCli.item(n, 'values')
        self.id_entry.insert(END, col1)
        self.nome_entry.insert(END, col2)
        self.nacionalidade_combo.insert(END, col3)
        self.estado_civil_combo.insert(END, col4)
        self.profissao_entry.insert(END, col5)
        self.rg_entry.insert(END, col6)
        self.cpf_entry.insert(END, col7)
        self.cep_entry.insert(END, col8)
        self.uf_entry.insert(END, col9)
        self.cidade_entry.insert(END, col10)
        self.rua_entry.insert(END, col11)
        self.n_rua_entry.insert(END, col12)
        self.bairro_entry.insert(END, col13)
        self.telefone_entry.insert(END, col14)
        self.email_entry.insert(END, col15)
        self.nome_reu_entry.insert(END, col16)
        self.cnpj_reu_entry.insert(END, col17)

def setup_enter_bindings(self, frame):
    # Crie uma lista com todos os widgets na ordem que você quer
    # Substitua pelas variáveis das suas Entrys
    if(frame == "frame_cliente"):
        self.entry_list = [
            self.nome_entry,
            self.nacionalidade_combo,
            self.estado_civil_combo,
            self.profissao_entry,
            self.rg_entry,
            self.cpf_entry,
            self.cep_entry,
            self.n_rua_entry,
            self.telefone_entry,
            self.email_entry,
            self.nome_reu_entry,
            self.cnpj_reu_entry
        ]
    elif(frame == "frame_documento"):
        self.entry_list = [
            self.nome_doc_entry,
            self.tipo_combo,
            self.caminho_doc_entry
        ]
    
    for i in range(len(self.entry_list) - 1):
        current_entry = self.entry_list[i]
        next_entry = self.entry_list[i + 1]
        
        # Cria uma função lambda para passar o próximo widget para a próxima função
        # Isso garante que cada entry saiba para onde ir
        current_entry.bind("<Return>", lambda event, next_widget=next_entry: next_widget.focus_set())
