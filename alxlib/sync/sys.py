__author__ = 'Alex Gomes'

import os,sys, shutil, logging
from gettext import gettext as _
from alxlib.sync.path import SyncPath



class SyncStorage(object):
    def __init__(self):
        pass

class SLocal(SyncStorage):

    def __init__(self):
        super().__init__()

    def path_clean(self, path):
        try:
            norm_path= os.path.abspath(os.path.normpath(os.path.expanduser(os.path.expandvars(path))))
            if not os.path.isdir(norm_path):
                print(_("Error: {0} is not directory".format(norm_path)))
                sys.exit(1)
            else:
                return norm_path
        except Exception as e:
            print(_("Bad path {}").format())
            sys.exit(1)

    def spath(self, path, root, rel):
        spath = SyncPath()
        spath.BasePath=path
        new_path=os.path.abspath(os.path.normpath(os.path.join(root, rel)))
        spath.AbsPath=new_path
        new_path= new_path[len(path):]
        spath.SPath= new_path.replace("\\", "/")
        spath.Size= os.path.getsize(spath.AbsPath)
        spath.ModifiedTS= os.path.getmtime(spath.AbsPath)
        return spath

    def path_list(self, path):
        try:
            logging.debug("local_path_list {0}".format(path))

            import hashlib

            d={}

            for root, dirs, files in os.walk(path):
                #logging.debug("{0}--{1}--{2}" .format(root, dirs, files))
                for dir in dirs:
                    spath= self.spath(path, root, dir)
                    spath.IsDir=True
                    d[spath.SPath]= spath
                    #print(str(spath.SPath))
                for file in files:
                    spath= self.spath(path, root, file)
                    spath.IsFile=True
                    spath.MD5=hashlib.md5(open(spath.AbsPath, 'rb').read())
                    d[spath.SPath]= spath
                    #print(str(spath.SPath))
            #pprint(d)
            return d
        except Exception as e:
            print(e)

    def copy_local_local(self, src: SyncPath, baseDir):
        try:
            path= os.path.normpath(baseDir+ src.SPath)
            logging.debug("copy_local_local->{0}".format(path))

            if src.IsDir:
                os.makedirs(path, exist_ok=True)
            else:
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                shutil.copy2(src.AbsPath, path, follow_symlinks=False)
        except Exception as e:
            print("Error Copying")


    def copy(self, src: SyncPath, baseDir, src_type, dst_type):
        if src_type=="local" and dst_type=="local":
            self.copy_local_local(src, baseDir)

    def remove(self, src: SyncPath, src_type):

        if src_type=="local":
            logging.debug("Removing {0}".format(src.AbsPath))
            if src.IsDir:
                shutil.rmtree(src.AbsPath, ignore_errors=False, onerror=None)
            else:
                os.remove(src.AbsPath)






