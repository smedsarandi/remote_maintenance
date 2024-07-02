import os, zipfile, time, socket, json, requests, shutil, psutil, subprocess, threading

hostname = socket.gethostname()
app_managers = []
# Verificação de existência do diretório
directory_executor = 'c:/apps/'
if not os.path.exists(directory_executor):
    os.makedirs(directory_executor)
os.chdir(directory_executor)

# Classe que gerenciará os apps já baixados e possivelmente em execução que foram filtrados pela Função get_new_app()
class App_manager:
    def __init__(self, app_name, version, url_download, executable_name):
        self.app_name = app_name
        self.version = version
        self.url_download = url_download
        self.executable_name = executable_name
        self.status = {}

    # Método que APENAS BAIXA E EXTRAI o arquivo .zip no 'directory_executor'
    def app_download(self):
        print(f'\n\nSOLICITADO DOWNLOAD PARA {self.app_name}')
        try:
            response = requests.get(self.url_download, stream=True)
            if response.status_code == 200:
                print(f'{self.app_name}: statuscode 200') 
                with open(f'{self.app_name}.zip', 'wb') as file:
                    print(f'{self.app_name}: baixando o arquivo .zip')
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, file)
            
                with zipfile.ZipFile(f'{self.app_name}.zip', 'r') as Zip:
                    print(f'{self.app_name}: extraido {self.app_name}.zip')
                    Zip.extractall()
                    time.sleep(5)
                print(f'{self.app_name}: excluindo o .zip baixado')
                os.remove(f'{self.app_name}.zip')
                return True
            else:
                print(f'{self.app_name}: statuscode do download não é 200')
                return False
        except requests.exceptions.RequestException as e:
            print(f'{self.app_name}: Erro ao baixar o arquivo: {e}')
            return False
        except zipfile.BadZipFile as e:
            print(f'{self.app_name}: Erro ao extrair o arquivo zip: {e}')
            return False
        except Exception as e:
            print(f'{self.app_name}: Erro inesperado: {e}')
            return False

    # Método que INICIA O APP
    def app_start(self):
        print(f'\n\nSOLICITADO START PARA {self.app_name}')
        try:
            executable_path = os.path.join(directory_executor, self.executable_name)
            if os.path.exists(executable_path):
                print(f'{self.app_name}: Iniciando o app {self.executable_name}')
                subprocess.Popen([executable_path], shell=True)
            else:
                print(f'{self.app_name}: O executável {self.executable_name} não foi encontrado no diretório {directory_executor}')
        except Exception as e:
            print(f'{self.app_name}: Erro ao iniciar o app: {e}')

    # Método que PARA O APP
    def app_stop(self):
        print(f'\n\nSOLICITADO STOP PARA {self.app_name}')
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if self.executable_name.lower() in proc.info['name'].lower():
                    print(f"{self.app_name}: Finalizando processo: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()  # Envia o sinal de término
                    proc.wait(timeout=5)  # Espera que o processo termine
                    print(f"{self.app_name}: Processo {proc.info['name']} (PID: {proc.info['pid']}) finalizado com sucesso")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                print(f'{self.app_name}: Erro ao finalizar o processo: {e}')

    # Método que ATUALIZA O APP
    def app_update(self, remote_version):
        print(f'\n\nSOLICITADO UPDATE PARA {self.app_name}')
        if self.version < remote_version:
            print(f'{self.app_name}: Versão Local: {self.version}, Versão Server: {remote_version}')
            print(f'{self.app_name}: Inicializando atualização')
            self.app_stop()
            self.app_download()
            self.app_start()
            self.version = remote_version
        else:
            print(f'{self.app_name}: Não é necessário atualizar. Versão Local: {self.version}, Versão Server: {remote_version}')

def initialize():
    response = requests.get('https://github.com/smedsarandi/remote_maintenance/raw/main/remote_maintenance.json')
    if response.status_code == 200:
       
        objeto_criado = response.json()  # Decodifica o conteúdo JSON da resposta
        
        

        if len(app_managers) == 0:
            print("existem 0 apps")
            for key, value in objeto_criado.items():
                if 'maquinas' in value:
                    if hostname in value['maquinas'] or 'all' in value['maquinas']:
                        print(f'Será inicializado o app"{key}"')
                        app_manager = App_manager(app_name=key, version=value['version'], url_download=value["url"], executable_name=value["executable_name"])
                        app_managers.append(app_manager)
        else:
            print(f"exitem {len(app_managers)} apps")
            for instance in app_managers:
                versao_remote = objeto_criado[instance.app_name]['version']
                if instance.version < versao_remote:
                    print(f'app {instance.app_name} será atualizado')
                    instance.app_update(remote_version=versao_remote)
                    
                else:
                    print(f'app {instance.app_name} Não será atualizado')
                #print(instance.app_name)
        return app_managers
    else:
        print(f'Falha ao fazer o download. Status code: {response.status_code}')





while True:
    app_managers = initialize()
    time.sleep(5)

#print(app_managers[0].app_name)

