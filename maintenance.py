import os, zipfile, time, socket, json, requests, shutil, psutil, subprocess, threading

hostname = socket.gethostname()

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
    def app_update(self, remote_version, remote_url):
        print(f'\n\nSOLICITADO UPDATE PARA {self.app_name}')
        if self.version < remote_version:
            print(f'{self.app_name}: Versão Local: {self.version}, Versão Server: {remote_version}')
            print(f'{self.app_name}: Inicializando atualização')
            self.url_download = remote_url
            self.app_stop()
            self.app_download()
            self.app_start()
            self.version = remote_version
        else:
            print(f'{self.app_name}: Não é necessário atualizar. Versão Local: {self.version}, Versão Server: {remote_version}')

# Função para gerenciar cada app em uma thread separada
def manage_app(app_manager, remote_version, remote_url):
    if not app_manager.app_download():
        return
    app_manager.app_start()
    while True:
        app_manager.app_update(remote_version, remote_url)
        time.sleep(time_loop)

# Função que verifica se este PC precisa executar algum APP
def get_new_app():
    global time_loop
    try:
        response = requests.get('https://github.com/smedsarandi/remote_maintenance/raw/main/remote_maintenance.json')
        if response.status_code == 200:
            data = response.json()
            config = data.get('config', {})
            time_loop = config.get('time_loop', 60)  # Tempo padrão de 60 segundos se não especificado

            app_managers = {}

            while True:
                for app_name, app_info in data.items():
                    if app_name == 'config':
                        continue
                    maquinas = app_info.get('maquinas', [])
                    if 'all' in maquinas or hostname in maquinas:
                        if app_name not in app_managers:
                            app_manager = App_manager(
                                app_name=app_info['app_name'],
                                version=0,  # Inicializa a versão como 0 para garantir que baixe a primeira vez
                                url_download=app_info['url'],
                                executable_name=app_info['executable_name']
                            )
                            app_managers[app_name] = app_manager
                            threading.Thread(target=manage_app, args=(app_manager, app_info['version'], app_info['url'])).start()
                time.sleep(time_loop)  # Espera pelo tempo definido antes de verificar novamente
        else:
            print('Falha ao baixar remote_maintenance.json')
            time.sleep(60)  # Espera 60 segundos antes de tentar novamente em caso de falha
    except requests.exceptions.RequestException as e:
        print(f'Erro ao baixar o arquivo JSON: {e}')
        time.sleep(60)  # Espera 60 segundos antes de tentar novamente em caso de erro de rede
    except json.JSONDecodeError as e:
        print(f'Erro ao decodificar o arquivo JSON: {e}')
        time.sleep(60)  # Espera 60 segundos antes de tentar novamente em caso de erro de decodificação
    except KeyError as e:
        print(f'Erro na estrutura do arquivo JSON: {e}')
        time.sleep(60)  # Espera 60 segundos antes de tentar novamente em caso de erro de estrutura
    except Exception as e:
        print(f'Erro inesperado: {e}')
        time.sleep(60)  # Espera 60 segundos antes de tentar novamente em caso de erro inesperado

# Exemplo de uso
get_new_app()
