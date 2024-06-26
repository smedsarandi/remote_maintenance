import json

with open('remote_maintenance.json', encoding='utf-8') as meu_json:
                remote_maintenance_old = json.load(meu_json)


print(remote_maintenance_old['all']['version'])