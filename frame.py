import os
import shutil
import zipfile
from tempfile import TemporaryDirectory as t_dir
import psutil
import sys

class Framework:
    def __init__(self,docpath,zip_here):
        self.docpath = docpath
        self.user_path = []
        self.user = []
        self.temp = t_dir(prefix='CleanWechatFiles_Frame_')
        self.temp_path = self.temp.name
        self.zip_here = zip_here
        self.rubbish_doc = {
            'Rubbish':[
                'Backup',
                'BackupFiles',
                'ResUpdateV2'],
            'Documents':[
                'FileStorage',
                'Msg',
                'config'
            ]
        }
        self.app_path = os.getcwd()

    def run(self):
        print('正在做一个检查……')
        self.check()
        print('检查成功，正在导入用户列表……')
        self.take_path()

    def check(self):
        if not os.path.exists(self.docpath):
            print('没有该路径！')
        else:
            pid = psutil.pids()
            for p in pid:
                if 'Wechat' in psutil.Process(p).name():
                    print('请关闭微信后重试！')
                    sys.exit(1)

    def take_path(self):
        walk = []
        for i in os.walk(self.docpath):
            walk = i
            break
        users = []
        for us in walk[1]:
            if us == 'All Users' or us == 'Applet':
                continue
            users.append(os.path.join(self.docpath,us))
            self.user.append(us)
            print('切入了新的历史用户：%s ，它的路径：%s'%(us,os.path.join(self.docpath,us)))
        
        self.user_path = users
        self.clean_rubbish()

    def clean_rubbish(self):
        for l in self.user_path:
            try:
                for ll in self.rubbish_doc['Rubbish']:
                    shutil.rmtree(os.path.join(l,ll))
                    print('已删除 %s'%ll)
            except (OSError,FileNotFoundError):
                pass
        self.move_to_temp()

    def move_to_temp(self):
        for l,u in zip(self.user_path,self.user):
            try:
                for ll in self.rubbish_doc['Documents']:
                    shutil.move(os.path.join(l,ll),os.path.join(self.temp_path,u,ll))
                    print('已把 %s 移到 %s'%(os.path.join(l,ll),os.path.join(self.temp_path,u)))
            except (OSError,FileNotFoundError):
                pass
        self.temp_to_zip()

    def temp_to_zip(self):
        os.chdir(self.docpath)
        with zipfile.ZipFile(self.zip_here,'w') as f:
            for pn,spn,fn in os.walk('.'):
                for i in fn:
                    f.write(os.path.join(pn,i))
                    print('向%s写入：%s'%(self.zip_here,os.path.join(pn,i)))
        self.__del__()
        
    def __del__(self):
        os.chdir(self.app_path)
        shutil.rmtree(self.docpath)
        print('已清除完Wechat Files，正在清除临时文件夹……')
        self.temp.cleanup()
        print('已清除临时文件夹！')
        print('CleanWechatFiles Framework已结束！')