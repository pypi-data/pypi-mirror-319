import os
import shutil
from os.path import join


def make_relative_symlink(src, dst):
    path_cwd = os.getcwd()
    
    path_dir_dst = os.path.dirname(dst)
    if not os.path.isdir(path_dir_dst):
        raise ValueError(
            'utils.make_relative_symlink: not os.path.isdir(os.path.dirname(dst))'
        )
    
    os.chdir(path_dir_dst)
    
    os.symlink(os.path.relpath(src, './'), dst)
    
    os.chdir(path_cwd)


def get_tmp_path(path):
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    if ('.' in basename) and (not basename.startswith('.')):
        return join(dirname, basename+'.tmp')
    else:
        return join(dirname, basename+'_tmp')


def backup(path):
    basename = os.path.basename(path)
    dirname = os.path.dirname(path)
    
    max_index = 0
    for i in os.listdir(join(dirname)):
        if i.startswith(basename):
            suffix = i.split(sep=basename)[1]
            if suffix.startswith('_'):
                suffix = suffix.split('_')
                if len(suffix) == 2:
                    try:
                        index = int(suffix[1])
                        if index > max_index: max_index = index
                    except:
                        pass
    
    path_backup = join(dirname, basename+'_'+str(max_index+1))
    
    os.rename(path, path_backup)
    
    return path_backup


def cp_r_atomic(src, des):
    # using this function will involve a file named '%s.tmp' % (os.path.basename(des))
    # please ensure this file does not exist
    path_des_tmp = join(os.path.dirname(des), '%s.tmp' % (os.path.basename(des)))
    rm_fr(path_des_tmp)
    
    if os.path.isdir(src):
        shutil.copytree(src, path_des_tmp)
    elif os.path.isfile(src):
        shutil.copy(src, path_des_tmp)
    else:
        raise ValueError('%s represents neither a directory nor a file' % (src))
    
    os.rename(path_des_tmp, des)


def cp_r(src, des):
    if os.path.isdir(src):
        shutil.copytree(src, des)
    elif os.path.isfile(src):
        shutil.copy(src, des)
    else:
        raise ValueError('%s represents neither a directory nor a file' % (src))


def rm_fr_atomic(path):
    # using this function will involve a file named '%s.tmp' % (os.path.basename(path))
    # please ensure this file does not exist
    path_tmp = join(os.path.dirname(path), '%s.tmp' % (os.path.basename(path)))
    rm_fr(path_tmp)
    
    if not os.path.exists(path):
        pass
    else:
        if os.path.isdir(path):
            os.rename(path, path_tmp)
            shutil.rmtree(path_tmp)
        elif os.path.isfile(path):
            os.rename(path, path_tmp)
            os.remove(path_tmp)
        else:
            raise ValueError('%s represents neither a directory nor a file' % (path))


def rm_fr(path):
    if not os.path.exists(path):
        pass
    else:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            raise ValueError('%s represents neither a directory nor a file' % (path))
