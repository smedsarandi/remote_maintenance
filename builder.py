#modulo que criará os executáveis de instalação e maintenance
import os
#os.popen('pyinstaller --icon img/icon.ico --onefile maintenance.pyw')
os.popen('pyinstaller --icon img/icon.ico --onefile install.pyw')