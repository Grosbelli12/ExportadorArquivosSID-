from tkcalendar import Calendar
import customtkinter as ctk
from baixar_arquivos import processar_exportacao

# Configuração da janela principal
app = ctk.CTk()
app.geometry("700x700")
app.title("Exportador de Arquivos")


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

    janela_calendario.geometry(f"300x300+{pos_x}+{pos_y - 48 }")

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
    
    pos_x = btn_abrir.winfo_rootx()
    pos_y = btn_abrir.winfo_rooty()
    
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



frame_ip = ctk.CTkFrame(app, fg_color="transparent")
frame_ip.pack(pady=10)

input_ip = ctk.CTkEntry(frame_ip, placeholder_text="localhost", font=("Arial", 14),  width=220)
input_ip.pack(side="right", padx=(10, 60))

ip = ctk.CTkLabel(frame_ip, text="IP", font=("Arial", 14, ), width=130, anchor="e")
ip.pack(side="right")



frame_nome_banco = ctk.CTkFrame(app, fg_color="transparent")
frame_nome_banco.pack(pady=10)

input_nome_banco = ctk.CTkEntry(frame_nome_banco, placeholder_text="Nome do Banco", font=("Arial", 14), width=220)
input_nome_banco.pack(side="right", padx=(10, 60))

nome_banco = ctk.CTkLabel(frame_nome_banco, text="Nome", font=("Arial", 14),width=130, anchor="e")
nome_banco.pack(side="right")



frame_usuario = ctk.CTkFrame(app, fg_color="transparent")
frame_usuario.pack(pady=10)

input_usuario = ctk.CTkEntry(frame_usuario, placeholder_text="Usuário",  font=("Arial", 14), width=220)
input_usuario.pack(side="right", padx=(10, 60))

usuario = ctk.CTkLabel(frame_usuario, text="Usuário", font=("Arial", 14),width=130, anchor="e")
usuario.pack(side="right")



frame_senha = ctk.CTkFrame(app, fg_color="transparent")
frame_senha.pack(pady=10)

input_senha = ctk.CTkEntry(frame_senha, placeholder_text="Senha", font=("Arial", 14), width=220)
input_senha.pack(side="right", padx=(10, 60))

senha = ctk.CTkLabel(frame_senha, text="Senha", font=("Arial", 14),width=130, anchor="e")
senha.pack(side="right")



frame_cliente = ctk.CTkFrame(app, fg_color="transparent")
frame_cliente.pack(pady=(80,10))

input_cliente = ctk.CTkEntry(frame_cliente, placeholder_text="0 para Todos", width=220)
input_cliente.pack(side="right", padx=(10, 60))

cliente = ctk.CTkLabel(frame_cliente, text="Código do Cliente", font=("Arial", 14), width=130, anchor="e")
cliente.pack(side="right")



frame_data_inicio = ctk.CTkFrame(app, fg_color="transparent")
frame_data_inicio.pack(pady=10)

data_inicio = ctk.CTkLabel(frame_data_inicio, text="Data de Início", font=("Arial", 14), width=130, anchor="e")
data_inicio.pack(side="left", padx=(0, 10))

input_data_inicio = ctk.CTkEntry(frame_data_inicio, placeholder_text="Formato (YYYY-MM-DD)", width=220)
input_data_inicio.pack(side="left", padx=(0, 10))

btn_abrir = ctk.CTkButton(frame_data_inicio, text="📅", command=abrir_calendario_inicio,  width=50)
btn_abrir.pack(side="left")




frame_data_fim = ctk.CTkFrame(app, fg_color="transparent")
frame_data_fim.pack(pady=10)

data_fim = ctk.CTkLabel(frame_data_fim, text="Data de Fim", font=("Arial", 14), width=130, anchor="e")
data_fim.pack(side="left", padx=(0, 10))

input_data_fim = ctk.CTkEntry(frame_data_fim, placeholder_text="Data de Fim (YYYY-MM-DD)", width=220)
input_data_fim.pack(side="left", padx=(0, 10))

btn_abrir = ctk.CTkButton(frame_data_fim, text="📅", command=abrir_calendario_fim, width=50)
btn_abrir.pack(side="left")




frame_modulo = ctk.CTkFrame(app, fg_color="transparent")
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

button_exportar = ctk.CTkButton(app, text="Exportar Arquivos", command=iniciar_exportacao, width=220, hover_color="#3878D8", corner_radius=10)
button_exportar.pack(pady=30, padx=(140, 60))

label_aviso = ctk.CTkLabel(app, text="", font=("Arial", 14))
label_aviso.pack(pady=10)

# Mantém o app rodando
app.mainloop()