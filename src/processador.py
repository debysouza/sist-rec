import os
import xml.etree.ElementTree as ET
import csv
import logging
import time

def ler_configuracao(config_file):
    with open(config_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        leia_file = lines[0].strip().split('=')[1]
        consultas_file = lines[1].strip().split('=')[1]
        esperados_file = lines[2].strip().split('=')[1]
    return leia_file, consultas_file, esperados_file

def processar_consultas(leia_file):
    consultas = []
    tree = ET.parse(leia_file)
    root = tree.getroot()
    for query in root.findall('QUERY'):
        query_number = query.find('QueryNumber').text
        query_text = query.find('QueryText').text.upper()
        records = query.find('Records')
        for record in records.findall('Item'):
            doc_number = record.text
            doc_votes = record.get('score')
            consultas.append((query_number, query_text, doc_number, doc_votes))
    return consultas

def gerar_arquivo_consultas(consultas, consultas_file):
    output_directory = '../result/'
    output_path = os.path.join(output_directory, consultas_file)
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        # writer.writerow(['QueryNumber', 'QueryText', 'DocNumber', 'DocVotes'])
        for consulta in consultas:
            formatted_text = ' '.join(consulta[1].split())
            writer.writerow([consulta[0], formatted_text, consulta[2], consulta[3]])

def gerar_arquivo_esperados(consultas, esperados_file):
    output_directory = '../result/'
    output_path = os.path.join(output_directory, esperados_file)
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['QueryNumber', 'DocNumber', 'DocVotes'])
        for consulta in consultas:
            writer.writerow([consulta[0], consulta[2], consulta[3]])

def processador_de_consultas(config_file):
    log_dir = '../log'
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=os.path.join(log_dir, 'processador_de_consultas.log'), level=logging.INFO, encoding='utf-8')
    logging.info("Iniciando processamento de consultas...")

    start_time = time.time()

    logging.info("Iniciando leitura do arquivo de configuração...")
    leia_file, consultas_file, esperados_file = ler_configuracao(config_file)
    logging.info(f"Arquivo de configuração lido. Tempo decorrido: {time.time() - start_time:.2f} segundos")

    logging.info("Iniciando processamento das consultas...")
    consultas = processar_consultas(leia_file)
    logging.info(f"Processamento das consultas concluído. Tempo decorrido: {time.time() - start_time:.2f} segundos")
    
    logging.info("Gerando arquivo de consultas...")
    gerar_arquivo_consultas(consultas, consultas_file)
    logging.info(f"Arquivo de consultas gerado. Tempo decorrido: {time.time() - start_time:.2f} segundos")
    
    logging.info("Gerando arquivo de resultados esperados...")
    gerar_arquivo_esperados(consultas, esperados_file)
    logging.info(f"Arquivo de resultados esperados gerado. Tempo decorrido: {time.time() - start_time:.2f} segundos")

    logging.info("Processamento de consultas concluído.")

if __name__ == "__main__":
    processador_de_consultas("../config/pc.cfg")
