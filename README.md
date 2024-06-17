# remote_maintenance
Aplicativo para executar softwares na inicialização do windows

## arquivo maintenance
*** ESSE É O APP QUE FICARÁ INSTALADO NO PC CLIENTE, SERÁ CHAMADO EM TODA INICIALIZAÇÃO ***
- É acionado em toda inicialização;
- Todos os arquivos serão trabalhados dentro da pasta temp do windows;
- Antes de baixar qualquer coisa, ele verifica se há scripts antigos para serem excluidos;
- Baixará o scripts.zip que será extraido nesta pasta;
- Após a extração será executado os arquivos exe de nomes script0.exe, script1.exe, script2.exe, script3.exe, script4.exe...


## arquivo install
*** ESSE É O ARQUIVO QUE INSTALARÁ O MAINTENANCE NA MAQUINA ***
- Finaliza processo maintenance.exe caso esteja sendo executado
- exclui todos scripts da pasta temp
- Copiará o arquivo maintenance.exe para a pasta temp
- excluirá todas as tarefas inuteis e scripts antigos
- criará a tarefa agendada para ser exacutadas nos logins
- criará arquivo de log bem detalhado sobre a instalação