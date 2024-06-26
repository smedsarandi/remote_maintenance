# remote_maintenance
Aplicativo para executar softwares na inicialização do windows

## arquivo maintenance
*** ESSE É O APP QUE FICARÁ INSTALADO NO PC CLIENTE, SERÁ CHAMADO EM TODA INICIALIZAÇÃO ***
- É acionado em toda inicialização;
- Todos os arquivos serão trabalhados dentro da pasta Temp do windows;
- Baixará o maquinas.json que informará qual zip a maquina deve baixar;
- Após o download do arquivo .zip baixado a maquina executará os main_0.exe, main_1.exe, main_2.exe, main_3.exe, main_4.exe...


## arquivo install
*** ESSE É O ARQUIVO QUE INSTALARÁ O MAINTENANCE NA MAQUINA ***
- Finaliza processo maintenance.exe caso esteja sendo executado;
- Fará download do arquivo "maintenance.exe" que estará compilado neste repositório;
- Copiará o arquivo maintenance.exe para a pasta Temp do windows;
- criará a tarefa agendada para ser exacutadas no login do usuário;
- criará arquivo de log bem detalhado sobre a instalação;


## config
> código para criar ambiente virtual
python -m venv .venv
> código para entrar no ambiente virtual
.venv\Scripts\activate

>lista todas as branche
git branch -a
>ver todas as branches remotas
git fetch
>Faz o checkout para a branch específica:
git checkout nome_do_branch


pyinstaller --icon img/icon.ico --onefile maintenance.py
pyinstaller --icon img/icon.ico --onefile install.py
