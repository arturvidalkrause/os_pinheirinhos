import os
import subprocess

# Nome do ambiente virtual
venv_name = "venv"

# Verifica se o arquivo requirements.txt existe
requirements_file = "requirements.txt"
if not os.path.exists(requirements_file):
    print(f"O arquivo {requirements_file} não foi encontrado. Crie um arquivo com as bibliotecas necessárias.")
else:
    # Cria o ambiente virtual
    print("Criando ambiente virtual...")
    subprocess.run(["python", "-m", "venv", venv_name])

    # Ativa o ambiente virtual (no Windows)
    activate_script = os.path.join(venv_name, "Scripts", "activate")

    # Instala as bibliotecas listadas no requirements.txt
    print("Instalando bibliotecas do requirements.txt...")
    subprocess.run([os.path.join(venv_name, "Scripts", "python"), "-m", "pip", "install", "-r", requirements_file])

    print("Ambiente virtual criado e bibliotecas instaladas.")
