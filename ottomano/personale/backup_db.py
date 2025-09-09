import datetime
import glob
import os
import shutil
from pathlib import Path

from django.conf import settings

if settings.NOME_COMPUTER.lower() == 'srvdc1':
    PATH_BCK = r'D:\Gestionale'
elif settings.NOME_COMPUTER.lower() == 'desktop-8g2ro2g':
    PATH_BCK = r'D:\Studio\Python\ottomano\ottomano'
else:
    PATH_BCK = r'C:\Users\L. MASI\Documents\Programmi\ottomano\ottomano'

OGGI = datetime.date.today()
MAX_BACKUP = 10


def backup():
    pathname = os.path.join(PATH_BCK, '*.sqlite3')
    db = glob.glob(pathname)
    backup_gia_effettuato = [True for x in db if Path(x).stem == f'bck_{OGGI}']

    if not backup_gia_effettuato:
        src = os.path.join(PATH_BCK, 'db.sqlite3')
        dst = os.path.join(PATH_BCK, f'bck_{OGGI}.sqlite3')

        shutil.copy2(src, dst)

    pulizia()


def pulizia(max_backup=MAX_BACKUP):
    path_bck = str(Path(PATH_BCK) / 'bck_*.sqlite3')

    lista_bck = glob.glob(path_bck)
    lista_bck.sort()

    bck_vecchi = lista_bck[:-MAX_BACKUP]

    for bck in bck_vecchi:
        os.remove(bck)
