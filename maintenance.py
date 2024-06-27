#Este módulo deverá ser chamado sempre que iniciar o usuário. Ele será instalado pelo módulo "install"
import os, zipfile, time, glob, socket, json, requests, shutil, subprocess
hostname = socket.gethostname()
directory_executor = 'c:/apps/'
os.chdir(directory_executor)#definindo o local de trabalho do executável

#Classe que gerenciará os apps já baixados e possivelmente em execução que foram filtrados pela Função get_new_app()
class App_manager:
    def __init__(self, app_name, version, url_download, executable_name):
        self.app_name = app_name
        self.version = version
        self.url_download = url_download
        self.executable_name = executable_name
        self.status = {}

    #metodo que apenas baixa o arquivo .zip e o extrai no 'directory_executor'
    def app_download(self):
        try:
            response = requests.get(self.url_download, stream=True)
            if response.status_code == 200:
                print('statuscode 200') 
                with open(f'{self.app_name}.zip', 'wb') as file:
                    print('baixando o arquivo .zip')
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, file)
            
                with zipfile.ZipFile(f'{self.app_name}.zip', 'r') as Zip:
                    print(f'extraido {self.app_name}.zip')
                    Zip.extractall()
                    time.sleep(5)
                print('excluindo o .zip baixado')
                os.remove(f'{self.app_name}.zip')
                return True
            else:
                print('statuscode do download não é 200')
                return False
        except:
            return False

    #metodo que inicia o app baixado pelo 'app_download()'
    def app_start(self):
        try:
            executable_path = os.path.join(directory_executor, self.executable_name)
            if os.path.exists(executable_path):
                print(f'Iniciando o app {self.executable_name}')
                subprocess.Popen([executable_path], shell=True)
            else:
                print(f'O executável {self.executable_name} não foi encontrado no diretório {directory_executor}')
        except Exception as e:
            print(f'Erro ao iniciar o app: {e}')

    def app_stop(self):
        pass

    def app_update(self):
        response = requests.get('https://github.com/smedsarandi/remote_maintenance/raw/main/remote_maintenance.json', stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            remote_maintenance = json.load(response.raw)
            if self.version < remote_maintenance[self.app_name]['version']:
                print('Inicializando atualização')
                self.app_stop()
                self.app_download()
                self.app_start()
        else:
            return False

'''
Esta função vai baixar o remote_maintenance.json e verificará se ESTE PC precisa executar algum APP.
Se afirmativo, ele instanciará a classe App_manager com o nome do APP
'''
def get_new_app():
    pass


app1 = App_manager(app_name='teste1', version=1, url_download='https://github.com/smedsarandi/remote_maintenance/raw/main/apps/teste1/dist/teste1.zip', executable_name='teste1.exe')
app1.app_download()
app1.app_start()
app1.app_update()



'''

#função usada para baixar novas configuraçõesm do json
def downloader_json(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        response.raw.decode_content = True
        #shutil.copyfileobj(response.raw, file)
        return json.load(response.raw)
    else:
        return False



#loop que será chamado no intervalo de tempo definido no "time_loop"
whil e True:
    os.chdir(directory_executor)
    remote_maintenance_new = downloader_json(url='https://github.com/smedsarandi/remote_maintenance/raw/gui/remote_maintenance.json')
    try:
        #verifica se ja existe o remote_maintenance.json
        if os.path.exists("remote_maintenance.json"):
            #abrirá o arquivo atual para verificar a diferença de versão
            with open('remote_maintenance.json', encoding='utf-8') as meu_json:
                remote_maintenance_old = json.load(meu_json)
            
            if remote_maintenance_old['config']['version_json'] < remote_maintenance_new['config']['version_json']:
                print(f'Versão desatualizada')

                for chave, valor in remote_maintenance_new.items():
                    if chave != 'config':
                        for maquina in valor['maquinas']:
                            if maquina == 'all' or maquina == hostname:
                                ######## FALTA COMPARAR A VERSÃO ANTES DE MANDAR BAIXAR
                                if valor['version'] > remote_maintenance_old[chave]['version']:
                                    file_executor(app_name=chave, url=valor['url'], executable_name=valor['executable_name'])

                                    with open('remote_maintenance.json', 'w') as file:
                                        json.dump(remote_maintenance_old, file, indent=4)

            else:
                print('versão atualizada, não é necessário fazer mudanças')
        else:
            #ainda não existe o arquivo
            file_executor(app_name=chave, url=valor['url'], executable_name=valor['executable_name'])
            #cria o arquivo
            with open('remote_maintenance.json', 'w') as file:
                json.dump(remote_maintenance_new, file, indent=4)


    except:
        print('não foi possivel baixar o json inicial') #Substituir este print por um log

    time.sleep(remote_maintenance_new['time_loop'])

'''