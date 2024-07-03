# Importações de bibliotecas padrão
import os
import zipfile
import time
import socket
import json
import shutil
import subprocess
import threading
import logging

# Importações de bibliotecas de terceiros
import requests
import psutil

# Variaveis globais
hostname = socket.gethostname()
app_managers = [] #É uma lista que contêm todos os apps em execução no momento
app_quot = 0 #Vai armazenar a quantidade de app que existe quando o app_managers for criado, pois se for criados novos apps para essa maquina, ele reconhecerá
directory_executor = 'c:/apps/'

# Verificação a existência do diretório de execução, caso contrário ele será criado
if not os.path.exists(directory_executor):
    os.makedirs(directory_executor)
# definindo o diretório de execução
os.chdir(directory_executor)

# Configurando o logger
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("remote_maintenance.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger()

''' 
Classe que gerenciará os apps já baixados e possivelmente em execução que foram filtrados pela função "initialize()"
Cada APP será uma instancia dessa classe e a partir dela será possivel baixar, iniciar, parar e atualizar o APP individualmente
'''
class App_manager:
    #as propriedades que serão instanciadas para cada APP
    def __init__(self, app_name, version, url_download, executable_name):
        self.app_name = app_name
        self.version = version
        self.url_download = url_download
        self.executable_name = executable_name

    # Método que apenas baixa e extrai o arquivo .zip da url no 'directory_executor' definido nas variaveis globais
    def app_download(self):
        logger.info(f'{self.app_name}: em download')
        try:
            response = requests.get(self.url_download, stream=True)
            if response.status_code == 200:
                logger.info(f'{self.app_name}: statuscode 200')
                with open(f'{self.app_name}.zip', 'wb') as file:
                    logger.info(f'{self.app_name}: baixando o arquivo .zip')
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, file)
            
                with zipfile.ZipFile(f'{self.app_name}.zip', 'r') as Zip:
                    logger.info(f'{self.app_name}: extraido {self.app_name}.zip')
                    Zip.extractall()
                    time.sleep(5)
                logger.info(f'{self.app_name}: excluindo o .zip baixado')
                os.remove(f'{self.app_name}.zip')
                return True
            else:
                logger.warning(f'{self.app_name}: statuscode do download não é 200')
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f'{self.app_name}: Erro ao baixar o arquivo: {e}')
            return False
        except zipfile.BadZipFile as e:
            logger.error(f'{self.app_name}: Erro ao extrair o arquivo zip: {e}')
            return False
        except Exception as e:
            logger.error(f'{self.app_name}: Erro inesperado: {e}')
            return False

    # Método que INICIA O APP
    def app_start(self):
        logger.info(f'{self.app_name}: em start')
        try:
            executable_path = os.path.join(directory_executor, self.executable_name)
            if os.path.exists(executable_path):
                logger.info(f'{self.app_name}: Iniciando o app {self.executable_name}')
                subprocess.Popen([executable_path], shell=True)
            else:
                logger.error(f'{self.app_name}: O executável {self.executable_name} não foi encontrado no diretório {directory_executor}')
        except Exception as e:
            logger.error(f'{self.app_name}: Erro ao iniciar o app: {e}')

    # Método que PARA O APP
    def app_stop(self):
        logger.info(f'{self.app_name}: em stop')
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if self.executable_name.lower() in proc.info['name'].lower():
                    logger.info(f"{self.app_name}: Finalizando processo: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()  # Envia o sinal de término
                    proc.wait(timeout=5)  # Espera que o processo termine
                    logger.info(f"{self.app_name}: Processo {proc.info['name']} (PID: {proc.info['pid']}) finalizado com sucesso")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                logger.error(f'{self.app_name}: Erro ao finalizar o processo: {e}')

    # Método que ATUALIZA O APP
    def app_update(self, remote_version):
        logger.info(f'{self.app_name}: em update')
        if self.version < remote_version:
            logger.info(f'{self.app_name}: Versão Local: {self.version}, Versão Server: {remote_version}.\nSerá feito update!!')
            self.app_stop()
            self.app_download()
            self.app_start()
            self.version = remote_version
            logger.info(f'{self.app_name}: agora está na versão: {self.version}.')
        else:
            logger.info(f'{self.app_name}: Desnecessário atualizar. Versão Local: {self.version}, Versão Server: {remote_version}')

'''
Está função será colocada em outra função de loop;
Ela é responsavel por verificar no json remoto se será preciso iniciar algum app;
Se APPS ja estão inicializados ela vetificará a versão atual para possiveis update.
'''
def initialize():
    print(f'ao chamar initialize o app_managers é: {len(app_managers)}')
    global app_quot
    app_quot_remote = 0
    response = requests.get('https://github.com/smedsarandi/remote_maintenance/raw/main/remote_maintenance.json')
    if response.status_code == 200: 
        json_remote = response.json()  # Decodifica o conteúdo JSON da resposta
        #esse "app_managers" é uma lista que contêm todos os apps em execução no momento
        for key, value in json_remote.items():
            if 'maquinas' in value:
                if hostname in value['maquinas'] or 'all' in value['maquinas']:     
                    if len(app_managers) == 0:
                        logger.info(f'{key}: instanciando')
                        app_manager = App_manager(app_name=key, version=value['version'], url_download=value["url"], executable_name=value["executable_name"])
                        app_manager.app_download()
                        app_manager.app_start()
                        app_managers.append(app_manager)
                        app_quot += 1
                            
                    elif len(app_managers) > 0:
                        #aqui ele vai intera por cada APP instanciado, e dar o update em cada um deles
                        for app in app_managers:
                                logger.info(f'{app.app_name} já está instanciado')
                                if app.app_name == key:
                                    app.app_update(remote_version=value['version'])

        '''
        quando a maquina já estiver executando o código a algum tempo 
        ele vai verificar se a quantidade de apps remotos é maior que o numero de app rodando na maquina local
        '''
        for key, value in json_remote.items():
            if 'maquinas' in value:
                if hostname in value['maquinas'] or 'all' in value['maquinas']:
                    if key != "config":
                        app_quot_remote += 1
        logger.info(f'existem {app_quot_remote} apps remotos')
        if app_quot < app_quot_remote:
            logger.warning('HÁ NOVOS APPS DISPONIVEIS')
    else:
        logger.critical(f'LOOP ERROR Falha ao fazer o download. Status code: {response.status_code}')


def initialize_loop():

    while True:
        global app_managers
        #print(f'##########o tamano do app_managers é:{len(app_managers)}')
        logger.info('\n\n')
        logger.warning("INICIALIZANDO LOOP")
        initialize()
        time.sleep(5)
        

initialize_loop()
#initialize_thread = threading.Thread(target=initialize_loop)
#initialize_thread.start()

