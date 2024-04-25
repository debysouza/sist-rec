import os
import csv
import logging
import time

def ler_configuracao(config_file):
    with open(config_file, 'r') as file:
        lines = file.readlines()
        model_file = lines[0].strip().split('=')[1]
        query_file = lines[1].strip().split('=')[1]
        output_file = lines[2].strip().split('=')[1]
    return model_file, query_file, output_file

def ler_modelo_vetorial(model_file):
    modelo_vetorial = {}
    with open(model_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            termo = row['Word']
            documento = row['DocNumber'].strip()
            if documento not in modelo_vetorial:
                modelo_vetorial[documento] = set()
            modelo_vetorial[documento].add(termo)
    return modelo_vetorial

def calcular_distancias(modelo_vetorial, consulta):
    distancias = {}
    for documento, termos in modelo_vetorial.items():
        distancias[documento] = len(termos.intersection(consulta))
    return distancias

def realizar_busca(modelo_vetorial, consulta):
    distancias = calcular_distancias(modelo_vetorial, consulta)
    resultados = [(rank + 1, doc_id, distancia) for rank, (doc_id, distancia) in enumerate(sorted(distancias.items(), key=lambda x: x[1], reverse=True))]
    return resultados

def escrever_resultados(output_file, resultados):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["QueryNumber", "[(DocRank, DocNumber, Distance)]"])
        
        for consulta_id, docs in resultados.items():
            writer.writerow([consulta_id, docs])

def buscador(config_file):
    log_dir = '../log'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=os.path.join(log_dir, 'buscar.log'), level=logging.INFO, encoding='utf-8')
    logging.info("Iniciando operação de busca...")

    start_time = time.time()
    
    logging.info("Lendo arquivo de configuração...")
    model_file, query_file, output_file = ler_configuracao(config_file)

    logging.info("Lendo modelo vetorial...")
    modelo_vetorial = ler_modelo_vetorial(model_file)

    logging.info("Realizando busca nas consultas...")
    resultados = {}
    with open(query_file, 'r', encoding='utf-8') as file:
        for row in csv.reader(file, delimiter=';'):
            if len(row) < 2:
                logging.warning("Linha inválida encontrada no arquivo de consultas, pulando...")
                continue
            consulta_id, consulta = row[0], row[1].upper().split()
            resultados[consulta_id] = realizar_busca(modelo_vetorial, consulta)

    logging.info("Escrevendo resultados em arquivo CSV...")
    escrever_resultados(output_file, resultados)

    logging.info("Operação de busca concluída. Tempo total decorrido: %.2f segundos", time.time() - start_time)

if __name__ == "__main__":
    buscador("../config/busca.cfg")
