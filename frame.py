import os
import shutil
import sys
import zipfile
from tempfile import TemporaryDirectory as t_dir
import logging
import psutil

logging.basicConfig(level=logging.INFO)


class Framework:
    def __init__(self, docpath, zip_here):
        self.docpath = docpath
        self.user_path = []
        self.user = []
        self.temp = t_dir(prefix='CleanWechatFiles_Frame_')
        self.temp_path = self.temp.name
        self.zip_here = zip_here
        self.rubbish_doc = {
            'Rubbish': [
                'Backup',
                'BackupFiles',
                'ResUpdateV2'],
            'Documents': [
                'FileStorage',
                'Msg',
                'config'
            ]
        }
        self.app_path = os.getcwd()

    def run(self):
        logging.info("Checking......")
        self.check()
        logging.info("Take path......")
        self.take_path()

    def check(self):
        pid = psutil.pids()
        try:
            for p in pid:
                if 'Wechat' in psutil.Process(p).name():
                    logging.error("Please close wechat!")
        except psutil.AccessDenied:
            logging.error("Please close wechat!")

    def take_path(self):
        walk = []
        for i in os.walk(self.docpath):
            walk = i
            break
        users = []
        for us in walk[1]:
            if us == 'All Users' or us == 'Applet':
                continue
            users.append(os.path.join(self.docpath, us))
            self.user.append(us)
            logging.info("New user:%s" % us)

        self.user_path = users
        self.clean_rubbish()

    def clean_rubbish(self):
        for l in self.user_path:
            try:
                for ll in self.rubbish_doc['Rubbish']:
                    shutil.rmtree(os.path.join(l, ll))
                    logging.info("Clean:%s" % ll)
            except (OSError, FileNotFoundError):
                pass
        self.move_to_temp()

    def move_to_temp(self):
        for l, u in zip(self.user_path, self.user):
            try:
                for ll in self.rubbish_doc['Documents']:
                    shutil.move(os.path.join(l, ll), os.path.join(self.temp_path, u, ll))
                    logging.info("Move %s" % os.path.join(l, ll))
            except (OSError, FileNotFoundError):
                pass
        self.temp_to_zip()

    def temp_to_zip(self):
        os.chdir(self.docpath)
        with zipfile.ZipFile(self.zip_here, 'w') as f:
            for pn, spn, fn in os.walk('.'):
                for i in fn:
                    f.write(os.path.join(pn, i))
                    logging.info("Write %s" % os.path.join(pn, i))
        self.__del__()

    def __del__(self):
        os.chdir(self.app_path)
        try:
            shutil.rmtree(self.docpath)
            logging.info("Clean temp......")
            self.temp.cleanup()
            logging.info("All done!")
        except Exception:
            pass
