#Este módulo deverá ser chamado sempre que iniciar o usuário. Ele será instalado pelo módulo "install"
import os, zipfile, time, glob, socket, json, requests, shutil
hostname = socket.gethostbyname()

#definindo o local de trabalho do executável
directory_executor = 'c:/Windows/Temp/'
os.chdir(directory_executor)

#função usada para baixar arquivos
def downloader_file(url, local_filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_filename, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
        print(f'foi baixado e salvo como {local_filename}')
    else:
        print(f'Falha ao baixar: {url}')


#função usada para baixar novas configuraçõesm do json
def downloader_json(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        response.raw.decode_content = True
        #shutil.copyfileobj(response.raw, file)
        return json.load(response.raw)
    else:
        return False


#função usada para executar os app
def file_executor(app_name, url, executable_name):
    downloader_file(url=url, local_filename = f'{app_name}.zip')
    time.sleep(2)

    with zipfile.ZipFile(f'{app_name}.zip', 'r') as Zip:#extraindo arquivos
        Zip.extractall()
        print(f'extraido {app_name}.zip')
        time.sleep(5)
        os.remove(f'{app_name}.zip')
        os.popen(executable_name)
    
#loop que será chamado no intervalo de tempo definido no "time_loop"
while True:
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
