import pathlib
import os
import shutil
import time
from ftplib import FTP
from src.my_log import Log

log = Log(path='', file_handler=True, console_handler=True)


class MyFTP(object):
    """
    @note: upload local file or dirs recursively to ftp server
    """

    def __init__(self, ip, uname, pwd, port=21, timeout=60):
        self.ftp = None
        self.ip = ip
        self.uname = uname
        self.pwd = pwd
        self.port = port
        self.timeout = timeout
        self.ftp = self.ftp_init()

    def ftp_init(self):
        self.ftp = FTP()
        log.info('### connect ftp server: %s ...' % self.ip)
        try:
            self.ftp.connect(self.ip, self.port, self.timeout)
            self.ftp.login(self.uname, self.pwd)
            print(self.ftp.getwelcome())
            return self.ftp
        except Exception as e:
            raise e

    def close_ftp(self):
        if self.ftp:
            self.ftp.close()
            log.info('### disconnect ftp server: %s!' % self.ip)
            self.ftp = None

    def upload_dir(self, localdir='./', remotedir='./', IsDel=True):
        if not os.path.isdir(localdir):
            return
        self.ftp.cwd(remotedir)
        for file in os.listdir(localdir):
            src = os.path.join(localdir, file)
            if os.path.isfile(src):
                self.upload_file(src, file)
            elif os.path.isdir(src):
                try:
                    self.ftp.mkd(file)
                except Exception:
                    log.info('the dir is exists %s' % file)
                self.upload_dir(src, file)
            if IsDel:
                shutil.rmtree(src, ignore_errors=True)
        self.ftp.cwd('..')

    def upload_file(self, localpath, remotepath='./'):
        if not os.path.isfile(localpath):
            return
        log.info('+++ upload %s to %s:%s' % (localpath, self.ip, remotepath))
        self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))
        os.remove(localpath)  # del this file

    def upload(self, src):
        if os.path.isfile(src):
            file_name = pathlib.Path(src).name
            self.upload_file(src, file_name)
        elif os.path.isdir(src):
            self.upload_dir(src)


if __name__ == '__main__':
    srcDir = r"E:\temp\user\zctz"
    srcFile = r'E:\temp\user\zctz\20221022_000050_rzx.DAT'
    ftp_client = MyFTP(ip='192.168.1.9', port=21, uname='t1', pwd='t1')
    while 1:
        try:
            ftp_client.upload(srcDir)
            time.sleep(10)
        except Exception as e:
            log.info('文件传输中错误：', e)
            break
    ftp_client.close_ftp()
