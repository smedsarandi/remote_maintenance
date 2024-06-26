#Este módulo deverá ser chamado sempre que iniciar o usuário. Ele será instalado pelo módulo "install"
import os, zipfile, time, glob, socket, json, requests, shutil
hostname = socket.gethostbyname()

#definindo o local de trabalho do executável
os.chdir('c:/Windows/Temp/')

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
    with zipfile.ZipFile(app_name, 'r') as Zip:#extraindo arquivos
        Zip.extractall()
        print('extraido')
        time.sleep(5)
        os.remove(app_name)

    padrao = os.path.join("c:/Windows/Temp/", "*start*.exe") #  criar um caminho que procura por todos os arquivos .exe no diretório c:/Windows/Temp/ que contenham "start" no nome.

    lista_de_arquivos = []
    for arquivo in glob.glob(padrao): #Itera sobre cada arquivo que corresponde ao padrão definido em padrao. A função glob.glob(padrao) retorna uma lista de caminhos completos dos arquivos que correspondem ao padrão.
        lista_de_arquivos.append(os.path.basename(arquivo))

    print(f'Os arquivos extraidos são: {lista_de_arquivos}')
    #execute script
    for arquivo in lista_de_arquivos:
        os.popen(arquivo)
    
#loop que será chamado no intervalo de tempo definido no "time_loop"
while True:
    remote_maintenance_new = downloader_json(url='https://github.com/smedsarandi/remote_maintenance/raw/gui/remote_maintenance.json')
    try:
        #verifica se ja existe o remote_maintenance.json
        if os.path.exists("remote_maintenance.json"):
            #abrirá o arquivo atual para verificar a diferença de versão
            with open('remote_maintenance.json', encoding='utf-8') as meu_json:
                remote_maintenance_old = json.load(meu_json)
            
            if remote_maintenance_old['config']['version_json'] < remote_maintenance_new['config']['version_json']:
                print(f'Versão desatualizada')
                #file_executor(app_name, url, executable_name)

            else:
                print('versão atualizada, não é necessário baixar mudanças')
        
        else:
            #ainda não existe o arquivo
            remote_maintenance = remote_maintenance_new
        
        



    except:
        print('não foi possivel baixar o json inicial') #Substituir este print por um log

    time.sleep(remote_maintenance_new['time_loop'])




'''
        for chave, valor in maquinas.items():
            if chave == "all" or chave == hostname:
                downloader_file(url=valor, local_filename=f'{chave}.zip')
                file_executor(filename=f'{chave}.zip')
'''