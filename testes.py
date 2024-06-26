import json, socket
hostname = socket.gethostname()
print(f'a maquina atual é: {hostname}\n')

with open('remote_maintenance.json', encoding='utf-8') as meu_json:
    remote_maintenance = json.load(meu_json)


for chave, valor in remote_maintenance.items():
    if chave != 'config':
        for maquina in valor['maquinas']:
            if maquina == 'all' or maquina == hostname:
                print(f'executar {chave}\nversion: {valor['version']}\n')
            else:
                pass
                #print(f'não executar {chave}')
