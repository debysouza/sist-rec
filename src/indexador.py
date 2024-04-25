import os
import csv
import math
from collections import defaultdict
import logging
import time

def ler_configuracao(config_file):
    leia_file = None
    escreva_file = None
    with open(config_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        leia_file = lines[0].strip().split('=')[1]
        escreva_file = lines[1].strip().split('=')[1]
    return leia_file, escreva_file

def ler_lista_invertida(leia_file):
    lista_invertida = defaultdict(list)
    num_docs = set()
    with open(leia_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if len(row) > 1:
                texto = row[0].upper()
                doc_ids = [doc.strip() for doc in row[1].strip("[]").split(",")]
                lista_invertida[texto] = doc_ids
                num_docs.update(doc_ids)
    n_docs = len(num_docs)
    return lista_invertida, n_docs

def calcular_idf(lista_invertida, n_docs):
    idf = {}
    for word, doc_ids in lista_invertida.items():
        idf[word] = math.log(n_docs / (1 + len(doc_ids)))
    return idf

def escrever_normalizar_modelo(escreva_file, lista_invertida, idf):
    with open(escreva_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Word', 'DocNumber', 'TF-IDF'])
        for word, doc_ids in lista_invertida.items():
            tf_idf_values = []
            back_doc_id = None
            max_abs_value = 0
            for doc_id in doc_ids:
                if doc_id != back_doc_id:
                    term_frequency = doc_ids.count(doc_id)
                    tf_idf = (1 + math.log(1 + term_frequency)) * idf[word]
                    tf_idf_values.append((doc_id.strip(), tf_idf))  # Removendo as aspas
                    if abs(tf_idf) > max_abs_value:
                        max_abs_value = abs(tf_idf)
                    back_doc_id = doc_id
            normalized_values = [(doc_id, tf_idf + max_abs_value) for doc_id, tf_idf in tf_idf_values]
            for doc_id, tf_idf in normalized_values:
                writer.writerow([word, doc_id, round(tf_idf, 2)])
            
def indexador(config_file):
    log_dir = '../log'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=os.path.join(log_dir, 'indexador.log'), level=logging.INFO, encoding='utf-8')
    logging.info("Iniciando operação de indexação...")

    start_time = time.time()

    leia_file, escreva_file = ler_configuracao(config_file)
    logging.info("Arquivo de configuração lido.")

    lista_invertida, n_docs = ler_lista_invertida(leia_file)
    logging.info("Arquivo de dados lido.")

    logging.info("Calculando IDF...")
    idf = calcular_idf(lista_invertida, n_docs)
    logging.info("IDF calculado.")

    escrever_normalizar_modelo(escreva_file, lista_invertida, idf)
    logging.info("Modelo vetorial criado com sucesso.")

    logging.info(f"Operação de indexação concluída. Tempo total decorrido: {time.time() - start_time:.2f} segundos")

if __name__ == "__main__":
    indexador("../config/index.cfg")
