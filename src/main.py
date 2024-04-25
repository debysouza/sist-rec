import subprocess

def execute_script(script):
    subprocess.run(["python", script])

if __name__ == "__main__":
    scripts = ["processador.py", "geradorListaInvertida.py", "indexador.py", "buscador.py"]

    for script in scripts:
        print(f"Executando script: {script}")
        execute_script(script)

    print("Execução concluída.")
