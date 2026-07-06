import re
from datetime import datetime
import psycopg2

def valida_data(data):
    regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    if re.match(regex, data):
        return True
    return False

def testar_conexao(ip, nome_banco, usuario, senha):
    try:
        conexao = psycopg2.connect(
            host=ip,
            database=nome_banco,
            user=usuario,
            password=senha
        )
        conexao.close()
        return True, "Conexão bem-sucedida!"
    except Exception as erro:
        return False, f"Erro ao conectar ao banco de dados: {erro}"
    
def processar_exportacao(ip, nome_banco, usuario, senha, cliente, data_inicio, data_fim, opcao_modulo):
    if not cliente.isdigit():
        return False, "Erro: Código de cliente inválido. Digite apenas números."

    if not valida_data(data_inicio):
        return False, "Data de início inválida. Use YYYY-MM-DD."
        
    if not valida_data(data_fim):
        return False, "Data de fim inválida. Use YYYY-MM-DD."

    try:
        opcao_modulo = int(opcao_modulo)
    except ValueError:
        return False, "Erro: Módulo inválido."

    if opcao_modulo < 0 or opcao_modulo > 11:
        return False, "Opção inválida. Selecione um módulo válido."

    try:
        conexao = psycopg2.connect(
            host=ip,
            database=nome_banco,
            user=usuario,
            password=senha
        )
        
        cursor = conexao.cursor()

        if cliente != "0":
            query_sql = "SELECT client_arq FROM ep001.sg_arquivos WHERE client_arq = %s LIMIT 1"
            cursor.execute(query_sql, (cliente,))
            resultado = cursor.fetchone()
            
            if resultado is None:
                return False, "Nenhum arquivo encontrado para este código de cliente."

        match opcao_modulo:
            case 0:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and dcadas_arq between %s and %s"
            case 1:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'CL' and dcadas_arq between %s and %s "
            case 2:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'FT' and dcadas_arq between %s and %s "
            case 3:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'OC' and dcadas_arq between %s and %s "
            case 4:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'PV' and dcadas_arq between %s and %s "
            case 5:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'OS' and dcadas_arq between %s and %s "
            case 6:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'PC' and dcadas_arq between %s and %s "
            case 7:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'EN' and dcadas_arq between %s and %s "
            case 8:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'PG' and dcadas_arq between %s and %s "
            case 9:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'RC' and dcadas_arq between %s and %s "
            case 10:
                query_sql = "select nome01_arq, docume_arq from ep001.sg_arquivos where (%s = '0' or client_arq = %s) and origem_arq = 'CQ' and dcadas_arq between %s and %s "
                
        cursor.execute(query_sql, (cliente, cliente, data_inicio, data_fim))
        resultados = cursor.fetchall()

        if len(resultados) == 0:
            return False, "Nenhum arquivo encontrado neste período e módulo."

        arquivos_baixados = 0
        for linha in resultados:
            nome01_arq = linha[0]
            docume_arq = linha[1]

            if docume_arq is not None:
                with open(nome01_arq, 'wb') as arquivo:
                    arquivo.write(docume_arq)
                    arquivos_baixados += 1
        
        return True, f"Sucesso! {arquivos_baixados} arquivo(s) exportado(s)."

    except Exception as erro:
        return False, f"Ocorreu um erro no banco de dados: {erro}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals():
            conexao.close()