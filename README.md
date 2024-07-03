# remote_maintenance
Aplicativo para executar gerenciar APPS remotamente, possibilitando o download, inicialização, parada e atualizações.


## arquivo maintenance
*** ESSE É O APP QUE FICARÁ INSTALADO NO PC CLIENTE, SERÁ CHAMADO EM TODA INICIALIZAÇÃO ***
- É acionado em toda inicialização e procura por atualizações a cada tempo definido no arquivo json;
- Baixará o 'remote_maintenance.json' que informará o que deve ser feito


## arquivo install
*** ESSE É O ARQUIVO QUE INSTALARÁ O MAINTENANCE NA MAQUINA ***
- Finaliza processo remote_maintenance.exe caso esteja sendo executado;
- Fará download do arquivo "maintenance.exe" que estará compilado neste repositório;
- Copiará o arquivo maintenance.exe para a pasta Temp do windows;
- criará a tarefa agendada para ser exacutadas no login do usuário;
- criará arquivo de log bem detalhado sobre a instalação;


## python configs
> comando para criar ambiente virtual:
python -m venv .venv

> comando para entrar no ambiente virtual:
.venv\Scripts\activate

> comando para buildar o arquivo .py ou .pyw:
pyinstaller maintenance.py --onefile --icon img/icon.ico


## git configs
>lista todas as branche:
git branch -a

>ver todas as branches remotas:
git fetch

>Faz o checkout para a branch específica:
git checkout nome_do_branch
