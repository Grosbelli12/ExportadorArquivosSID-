import customtkinter as ctk
import os
from tkcalendar import Calendar
from baixar_arquivos import processar_exportacao, testar_conexao
from cryptography.fernet import Fernet

# Configuração da janela principal
app = ctk.CTk()
app.geometry("700x700")
app.title("Exportador de Arquivos")

os.makedirs("base", exist_ok=True)


# Cria uma chave mestra para criptografia se não existir
if not os.path.exists("chave.key"):
    chave_nova = Fernet.generate_key()
    with open("base/chave.key", "wb") as arquivo_chave:
        arquivo_chave.write(chave_nova)
    
    # Carregamos a chave para a memória do programa 
    # fernet é o cofre que vai criptografar e descriptografar os dados
with open("base/chave.key", "rb") as arquivo_chave:
    chave_mestra = arquivo_chave.read()
    fernet = Fernet(chave_mestra) 
    
def salvar_dados():
    ip = input_ip.get()
    nome_banco = input_nome_banco.get()
    usuario = input_usuario.get()
    senha_digitada = input_senha.get()
    
    if not ip or not nome_banco or not usuario or not senha_digitada:
        label_aviso_conexao.configure(text="Todos os campos devem ser preenchidos!", text_color="red")
        return

    deu_certo, mensagem = testar_conexao(ip, nome_banco, usuario, senha_digitada)

    if not deu_certo:
        label_aviso_conexao.configure(text=mensagem, text_color="red")
        return

    senha = fernet.encrypt(senha_digitada.encode()).decode()
    
    with open("base/dados_conexao.txt", "w") as arquivo:
        arquivo.write(f"{ip}\n{nome_banco}\n{usuario}\n{senha}")

    label_aviso.configure(text="Dados salvos com sucesso!", text_color="green")
    pagina_conexao.pack_forget()
    pagina_exportacao.pack(fill="both", expand=True)

def iniciar_exportacao():
    ip = input_ip.get()
    nome_banco = input_nome_banco.get()
    usuario = input_usuario.get()
    senha = input_senha.get()
    cliente = input_cliente.get()
    data_inicio = input_data_inicio.get()
    data_fim = input_data_fim.get()
    opcao_modulo = combo_modulo.get().split(" - ")[0]  # Pega apenas o número da opção
    
    deu_certo, mensagem = processar_exportacao(ip, nome_banco, usuario, senha, cliente, data_inicio, data_fim, opcao_modulo)
    


    if deu_certo == True:
        label_aviso.configure(text=mensagem, text_color="green")
    else:
        label_aviso.configure(text=mensagem, text_color="red")
        

def abrir_calendario_inicio():
    # Cria um popup para o calendário
    janela_calendario = ctk.CTkToplevel(app)
    janela_calendario.title("Escolher Data")

    # Força a janela a ficar por cima de tudo
    janela_calendario.attributes("-topmost", True)


    # Puxa o foco do teclado/mouse para ela
    janela_calendario.focus()
    
    # Pega a posição EXATA do botão no eixo x e y 
    pos_x = btn_abrir.winfo_rootx()
    pos_y = btn_abrir.winfo_rooty()

    janela_calendario.geometry(f"300x300+{pos_x}+{pos_y}")

    # Cria o calendário date_pattern já formata do jeito que o Postgres utiliza
    calendario = Calendar(janela_calendario, selectmode='day', date_pattern='yyyy-mm-dd')
    calendario.pack(pady=20, padx=20)

    def confirmar_data():
        data_escolhida = calendario.get_date()
        input_data_inicio.delete(0, 'end')          # Limpa o que estava escrito no input
        input_data_inicio.insert(0, data_escolhida) # Insere a nova data no input
        janela_calendario.destroy()  
    
    btn_confirmar = ctk.CTkButton(janela_calendario, text="Confirmar", command=confirmar_data)
    btn_confirmar.pack(pady=10)


def abrir_calendario_fim():
    # Cria um popup para o calendário
    janela_calendario = ctk.CTkToplevel(app)
    janela_calendario.title("Escolher Data")
    janela_calendario.attributes("-topmost", True)
    janela_calendario.focus()
    
    pos_x = btn_abrir_fim.winfo_rootx()
    pos_y = btn_abrir_fim.winfo_rooty()
    
    janela_calendario.geometry(f"300x300+{pos_x}+{pos_y}")

    # Cria o calendário date_pattern já formata do jeito que o Postgres utiliza
    calendario = Calendar(janela_calendario, selectmode='day', date_pattern='yyyy-mm-dd')
    calendario.pack(pady=20, padx=20)

    def confirmar_data():
        data_escolhida = calendario.get_date()
        input_data_fim.delete(0, 'end')        
        input_data_fim.insert(0, data_escolhida) 
        janela_calendario.destroy()  
    
        
    btn_confirmar = ctk.CTkButton(janela_calendario, text="Confirmar", command=confirmar_data)
    btn_confirmar.pack(pady=10)





titulo = ctk.CTkLabel(app, text="Exportador de Arquivos", font=("Arial", 20, "bold"))
titulo.pack(pady=10)



pagina_conexao = ctk.CTkFrame(app, fg_color="transparent")


frame_ip = ctk.CTkFrame(pagina_conexao, fg_color="transparent")
frame_ip.pack(pady=10)

input_ip = ctk.CTkEntry(frame_ip, placeholder_text="localhost", font=("Arial", 14),  width=220)
input_ip.pack(side="right", padx=(10, 60))

ip = ctk.CTkLabel(frame_ip, text="IP", font=("Arial", 14, ), width=130, anchor="e")
ip.pack(side="right")



frame_nome_banco = ctk.CTkFrame(pagina_conexao, fg_color="transparent")
frame_nome_banco.pack(pady=10)

input_nome_banco = ctk.CTkEntry(frame_nome_banco, placeholder_text="Nome do Banco", font=("Arial", 14), width=220)
input_nome_banco.pack(side="right", padx=(10, 60))

nome_banco = ctk.CTkLabel(frame_nome_banco, text="Nome", font=("Arial", 14),width=130, anchor="e")
nome_banco.pack(side="right")




frame_usuario = ctk.CTkFrame(pagina_conexao, fg_color="transparent")
frame_usuario.pack(pady=10)

input_usuario = ctk.CTkEntry(frame_usuario, placeholder_text="Usuário",  font=("Arial", 14), width=220)
input_usuario.pack(side="right", padx=(10, 60))

usuario = ctk.CTkLabel(frame_usuario, text="Usuário", font=("Arial", 14),width=130, anchor="e")
usuario.pack(side="right")



frame_senha = ctk.CTkFrame(pagina_conexao, fg_color="transparent")
frame_senha.pack(pady=10)

input_senha = ctk.CTkEntry(frame_senha, placeholder_text="Senha", font=("Arial", 14), width=220)
input_senha.pack(side="right", padx=(10, 60))

senha = ctk.CTkLabel(frame_senha, text="Senha", font=("Arial", 14),width=130, anchor="e")
senha.pack(side="right")


btn_salvar = ctk.CTkButton(pagina_conexao, text="Salvar Dados", command=salvar_dados,  width=220, hover_color="#3878D8", corner_radius=10)
btn_salvar.pack(pady=10, padx=(140, 60))

label_aviso_conexao = ctk.CTkLabel(pagina_conexao, text="", font=("Arial", 14), wraplength=650)
label_aviso_conexao.pack(pady=10)



pagina_exportacao = ctk.CTkFrame(app, fg_color="transparent")


frame_cliente = ctk.CTkFrame(pagina_exportacao, fg_color="transparent")
frame_cliente.pack(pady=(80,10))

input_cliente = ctk.CTkEntry(frame_cliente, placeholder_text="0 para Todos", width=220)
input_cliente.pack(side="right", padx=(10, 60))

cliente = ctk.CTkLabel(frame_cliente, text="Código do Cliente", font=("Arial", 14), width=130, anchor="e")
cliente.pack(side="right")



frame_data_inicio = ctk.CTkFrame(pagina_exportacao, fg_color="transparent")
frame_data_inicio.pack(pady=10)

data_inicio = ctk.CTkLabel(frame_data_inicio, text="Data de Início", font=("Arial", 14), width=130, anchor="e")
data_inicio.pack(side="left", padx=(0, 10))

input_data_inicio = ctk.CTkEntry(frame_data_inicio, placeholder_text="Formato (YYYY-MM-DD)", width=220)
input_data_inicio.pack(side="left", padx=(0, 10))

btn_abrir = ctk.CTkButton(frame_data_inicio, text="📅", command=abrir_calendario_inicio,  width=50)
btn_abrir.pack(side="left")





frame_data_fim = ctk.CTkFrame(pagina_exportacao, fg_color="transparent")
frame_data_fim.pack(pady=10)

data_fim = ctk.CTkLabel(frame_data_fim, text="Data de Fim", font=("Arial", 14), width=130, anchor="e")
data_fim.pack(side="left", padx=(0, 10))

input_data_fim = ctk.CTkEntry(frame_data_fim, placeholder_text="Data de Fim (YYYY-MM-DD)", width=220)
input_data_fim.pack(side="left", padx=(0, 10))

btn_abrir_fim= ctk.CTkButton(frame_data_fim, text="📅", command=abrir_calendario_fim, width=50)
btn_abrir_fim.pack(side="left")




frame_modulo = ctk.CTkFrame(pagina_exportacao, fg_color="transparent")
frame_modulo.pack(pady=10)

modulo = ctk.CTkLabel(frame_modulo, text="Selecione o Módulo", font=("Arial", 14), width=130, anchor="e")
modulo.pack(side="left", padx=(0, 10))    

opcoes_modulos = [
    "0 - Todos",
    "1 - Cadastro de Cliente",
    "2 - Faturamento",
    "3 - Orçamento",
    "4 - Pré-Venda",
    "5 - Ordem de Serviço",
    "6 - Pedido de Compra",
    "7 - Notas de Entrada",
    "8 - Contas a Pagar",
    "9 - Contas a Receber",
    "10 - Cheque de Terceiros         "
    ]
combo_modulo = ctk.CTkComboBox(frame_modulo, values=opcoes_modulos, width=220)
combo_modulo.set("0 - Todos") 
combo_modulo.pack(side="right", padx=(0, 60))

button_exportar = ctk.CTkButton(pagina_exportacao, text="Exportar Arquivos", command=iniciar_exportacao, width=220, hover_color="#3878D8", corner_radius=10)
button_exportar.pack(pady=30, padx=(140, 60))

label_aviso = ctk.CTkLabel(pagina_exportacao, text="", font=("Arial", 14))
label_aviso.pack(pady=10)


if os.path.exists("base/dados_conexao.txt"):
    with open("base/dados_conexao.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        ip_salvo = linhas[0].strip()
        nome_banco_salvo = linhas[1].strip()
        usuario_salvo = linhas[2].strip()
        senha_salva = linhas[3].strip()
        
        senha = fernet.decrypt(senha_salva.encode()).decode()
        input_ip.insert(0, ip_salvo)
        input_nome_banco.insert(0, nome_banco_salvo)
        input_usuario.insert(0, usuario_salvo)
        input_senha.insert(0, senha)
        
        pagina_exportacao.pack(fill="both", expand=True)
        
else:
        pagina_conexao.pack(fill="both", expand=True)

# Mantém o app rodando
app.mainloop()