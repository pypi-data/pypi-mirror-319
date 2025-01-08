import os
import subprocess
from os.path import join


def check_gpu():
    try:
        subprocess.run(["nvidia-smi"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except:
        return False


def get_server_name():
    path_home = os.path.expanduser('~')
    path_server_info = join(path_home, '.server_info')
    
    if os.path.isfile(path_server_info):
        with open(path_server_info) as f:
            return f.readline().split(sep='=')[1].strip()
