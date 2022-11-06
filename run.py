import time
from src.my_ftpclient import MyFTP
from src import read_config
from src.my_ftpclient import log
from src import file_back
from src.read_config import BasePath

srcDir = read_config.Local_path
dst1 = BasePath.joinpath('data')  # 生成中间文件，用于FTP读取
dst_dirs = read_config.dst_dirs.append(dst1)  # 将该文件添加到文件备份的list表中


def run():
    while 1:
        try:
            ftp_client = MyFTP(ip=read_config.Ftp_IP, port=read_config.Port, uname=read_config.User_name,
                               pwd=read_config.Password)  # 初始化FTP
        except Exception as e:
            log.error('FTP 初始化错误：{}'.format(e))
            time.sleep(read_config.Interval)
            continue
        while 1:
            try:
                file_back.run(src=srcDir, dsts=read_config.dst_dirs, filetype=read_config.file_type)  # 先备份
                ftp_client.upload(dst1)  # 再上传
                time.sleep(read_config.Interval)
            except Exception as e:
                log.error('文件传输中错误：{}'.format(e))
                break
        ftp_client.close_ftp()


if __name__ == '__main__':
    run()
