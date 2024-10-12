# Este script automatiza a criação de um ambiente virtual Python e a instalação de bibliotecas a partir de um arquivo requirements.txt.
# Ele verifica se o arquivo requirements.txt existe, cria um ambiente virtual e instala todas as dependências listadas no arquivo.
# O script é especialmente útil para configurar rapidamente o ambiente de desenvolvimento de um projeto Python.

import os
import subprocess

# Nome do ambiente virtual que será criado
venv_name = "venv"

# Verifica se o arquivo requirements.txt existe no diretório atual
requirements_file = "requirements.txt"
if not os.path.exists(requirements_file):
    # Se o arquivo não for encontrado, exibe uma mensagem para o usuário.
    print(f"O arquivo {requirements_file} não foi encontrado. Crie um arquivo com as bibliotecas necessárias.")
else:
    # Caso o arquivo requirements.txt seja encontrado:
    
    # 1. Cria o ambiente virtual
    print("Criando ambiente virtual...")
    # O subprocess.run executa o comando "python -m venv venv" para criar o ambiente virtual chamado "venv".
    subprocess.run(["python", "-m", "venv", venv_name])

    # 2. Define o caminho para o script de ativação do ambiente virtual no Windows.
    # No Windows, o script de ativação do ambiente virtual fica na pasta "Scripts".
    activate_script = os.path.join(venv_name, "Scripts", "activate")

    # 3. Instala as bibliotecas listadas no arquivo requirements.txt
    print("Instalando bibliotecas do requirements.txt...")
    # Executa o comando "pip install -r requirements.txt" dentro do ambiente virtual, para instalar as dependências.
    subprocess.run([os.path.join(venv_name, "Scripts", "python"), "-m", "pip", "install", "-r", requirements_file])

    # 4. Exibe uma mensagem indicando que o ambiente foi criado com sucesso e as bibliotecas foram instaladas.
    print("Ambiente virtual criado e bibliotecas instaladas.")
