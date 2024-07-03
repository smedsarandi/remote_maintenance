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


if not os.path.exists(directory_executor):# Verificação a existência do diretório de execução, caso contrário ele será criado
    os.makedirs(directory_executor)
os.chdir(directory_executor) # definindo o diretório de execução


logging.basicConfig(level=logging.INFO, # Configurando o logger
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("remote_maintenance.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger()


#Classe que gerenciará os apps já baixados e possivelmente em execução que foram filtrados pela função "initialize()"
#Cada APP será uma instancia dessa classe e a partir dela será possivel baixar, iniciar, parar e atualizar o APP individualmente
class App_manager:
    def __init__(self, app_name, version, url_download, executable_name): #as propriedades que serão instanciadas para cada APP
        self.app_name = app_name
        self.version = version
        self.url_download = url_download
        self.executable_name = executable_name

    def app_download(self): # Método que apenas baixa e extrai o arquivo .zip da url no 'directory_executor' definido nas variaveis globais
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

    def app_start(self):# Método que INICIA O APP
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

    def app_stop(self):# Método que PARA O APP
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

    def app_update(self, remote_version):# Método que ATUALIZA O APP
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


#Está função será colocada em outra função de loop;
#Ela é responsavel por verificar no json remoto se será preciso iniciar algum app;
#Se APPS ja estão inicializados ela vetificará a versão atual para possiveis update.
def initialize():
    global app_quot
    app_quot_remote = 0
    headers = {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    response = requests.get('https://github.com/smedsarandi/remote_maintenance/raw/main/remote_maintenance.json', headers=headers)
    if response.status_code == 200: #só vai executar se o statuscode for 200 (ok)
        json_remote = response.json()  #Decodifica o conteúdo da resposta e cria essa variavel com o json dentro
        
        for key, value in json_remote.items(): #vai interar sobre cada item do json remoto
            if 'maquinas' in value: #se dentro dos valores existir o 'atributo' 'maquinas'
                if hostname in value['maquinas'] or 'all' in value['maquinas']: # vai verificar se nessa lista de maquina se encontra este pc
                    app_instanciado = False # por padrao ele vai considerar que nao existe a instancia do app remoto, a nao ser que a proxima linha prove isso
                    for app in app_managers:#esse "app_managers" é uma lista que contêm todos os apps em execução no momento
                        if app.app_name == key:                            
                            app_instanciado = True
                            logger.info(f'{app.app_name}: já está instanciado') #identificou que o APP ja esta instanciado na maquina, entao ele vai buscar por atts
                            app.app_update(remote_version=value['version'])   
                    
                    if app_instanciado == False: #agora se o APPS nao estiver instanciado, entao esta parte vai instancialo
                        logger.info(f'{key}: instanciando')
                        app_manager = App_manager(app_name=key, version=value['version'], url_download=value["url"], executable_name=value["executable_name"])
                        app_manager.app_download()
                        app_manager.app_start()
                        app_managers.append(app_manager)
                        app_quot += 1
    else:
        logger.error('Não foi possivel baixar json com novas informações')


def initialize_loop():
    while True:
        global app_managers
        logger.info('\n\n')
        logger.info(f'##########o tamano do app_managers atualmente é:{len(app_managers)}')
        logger.warning("INICIALIZANDO LOOP")
        initialize()
        time.sleep(10)


initialize_loop()
#initialize_thread = threading.Thread(target=initialize_loop)
#initialize_thread.start()

