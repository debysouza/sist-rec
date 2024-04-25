# Implementação de um Sistema de Recuperação em Memória segundo o Modelo Vetorial

Este é um projeto da disciplina de Mineração de Texto do Programa de Pós-graduação em Engenharia de Sistemas e Computação (PESC-UFRJ) que implementa um sistema de recuperação de informações utilizando o modelo vetorial. O projeto é dividido em módulos, cada um com sua funcionalidade específica.

## Instruções de Uso

### 1. Clonar o repositório

```bash
git clone https://github.com/debysouza/sist-rec.git
```

### 2. Instalar Dependências

As dependências foram instaladas utilizando o Anaconda no ambiente do VS Code.

### 3. Executar o Programa

```bash
cd src ; python main.py
```

## Arquivos e Diretórios

- **src/**: Diretório contendo todo o código fonte do projeto.
- **data/**: Diretório contendo os documentos originais utilizados pelo sistema.
- **config/**: Diretório contendo os arquivos de configuração de cada módulo.
- **modelo.txt**: Descrição do formato do modelo utilizado.
- **result/**: Diretório contendo todos os arquivos gerados durante a execução do programa.
  - **consultas_processadas.csv**: Arquivo contendo as consultas processadas.
  - **resultados_esperados.csv**: Arquivo contendo os resultados esperados.
  - **modelo_vetorial.csv**: Arquivo contendo o modelo vetorial gerado.
  - **lista_invertida.csv**: Arquivo contendo as listas invertidas.
  - **resultados.csv**: Arquivo contendo os resultados da busca.
- **log/**: Diretório contendo os arquivos de log gerados pelo programa.
