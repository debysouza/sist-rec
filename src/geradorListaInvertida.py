import os
import xml.etree.ElementTree as ET
import csv
from collections import defaultdict
import logging
from nltk.tokenize import word_tokenize
import time

def ler_configuracao(config_file):
    leia_files = []
    for line in config_file:
        if line.startswith('LEIA='):
            leia_files.append(line.strip().split('=')[1])
        elif line.startswith('ESCREVA='):
            escreva_file = os.path.join('..', 'src', line.strip().split('=')[1])
    return leia_files, escreva_file

def extrair_palavras(texto):
    return [word.strip().upper() for word in word_tokenize(texto) if len(word) >= 2 and word.isalpha()]

def atualizar_lista_invertida(lista_invertida, word, record_num):
    lista_invertida[word].append(record_num)

def processar_arquivo_xml(filename, lista_invertida):
    tree = ET.parse(os.path.join('..', 'data', filename))
    root = tree.getroot()
    for record in root.findall('.//RECORD'):
        record_num = record.find('RECORDNUM').text
        abstract_element = record.find('ABSTRACT')
        extract_element = record.find('EXTRACT')
        if abstract_element is not None:
            texto = abstract_element.text
        elif extract_element is not None:
            texto = extract_element.text
        else:
            texto = ''
        texto = texto.upper()
        palavras = extrair_palavras(texto)
        for palavra in palavras:
            atualizar_lista_invertida(lista_invertida, palavra, record_num)

def gerar_lista_invertida(config_file):
    log_dir = '../log'
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=os.path.join(log_dir, 'gerar_lista_invertida.log'), level=logging.INFO, encoding='utf-8')
    logging.info("Iniciando operação de geração da lista invertida...")

    start_time = time.time()

    with open(config_file, 'r') as config:
        leia_files, escreva_file = ler_configuracao(config)

    lista_invertida = defaultdict(list)

    for filename in leia_files:
        logging.info(f"Lendo arquivo: {filename}")
        file_start_time = time.time()
        processar_arquivo_xml(filename, lista_invertida)
        logging.info(f"Arquivo {filename} lido. Tempo decorrido: {time.time() - file_start_time:.2f} segundos")

    with open(escreva_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        for word, doc_ids in lista_invertida.items():
            writer.writerow([word, doc_ids])

    logging.info(f"Operação de geração da lista invertida concluída. Tempo total decorrido: {time.time() - start_time:.2f} segundos")

if __name__ == "__main__":
    gerar_lista_invertida("../config/gli.cfg")
