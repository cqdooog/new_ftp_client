import configparser
import pathlib
import sys

BasePath = pathlib.Path(sys.argv[0]).parent
config_path = BasePath.joinpath('config.ini')

config = configparser.ConfigParser()
config.read(config_path, encoding='utf-8')

#  Default
Interval = config.getint('Default', 'Interval')
dst_dirs = config.get('Default', 'dst_dirs').split(',')
file_type = config.get('Default', 'file_type')
# FtpInfo
Ftp_IP = config.get('FtpInfo', 'Ftp_IP')
Port = config.getint('FtpInfo', 'Port')
User_name = config.get('FtpInfo', 'User_name')
Password = config.get('FtpInfo', 'Password')
Local_path = config.get('FtpInfo', 'Local_path')
Remote_path = config.get('FtpInfo', 'Remote_path')

# print(Remote_path)
