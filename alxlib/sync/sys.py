__author__ = 'Alex Gomes'

import os, sys, shutil, logging
from gettext import gettext as _
from alxlib.sync.path import SyncPath
from azure.storage import BlobService

logging.getLogger("azure").setLevel(logging.CRITICAL)


class SyncStorage(object):
    def __init__(self):
        pass



    def copy(self, src: SyncPath, base_dir, src_type, dst_type, src_child, dst_child):
        if src_type == "local" and dst_type == "local":
            src_child.copy_local2local(src, base_dir)
        elif src_type == "local" and dst_type == "azure":
            dst_child.copy_local2azure(src, base_dir)
        elif src_type == "azure" and dst_type == "local":
            src_child.copy_azure2local(src, base_dir)




class SLocal(SyncStorage):
    def __init__(self):
        super().__init__()

    def path_clean(self, path):
        try:
            norm_path = os.path.abspath(os.path.normpath(os.path.expanduser(os.path.expandvars(path))))
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
        spath.BasePath = path
        new_path = os.path.abspath(os.path.normpath(os.path.join(root, rel)))
        spath.AbsPath = new_path
        new_path = new_path[len(path):]
        spath.SPath = new_path.replace("\\", "/")
        spath.Size = os.path.getsize(spath.AbsPath)
        spath.ModifiedTS = os.path.getmtime(spath.AbsPath)
        spath.sys="local"
        # print(str(spath))
        return spath

    def path_list(self, path):
        try:
            logging.debug("local_path_list {0}".format(path))

            import hashlib

            d = {}

            for root, dirs, files in os.walk(path):
                # logging.debug("{0}--{1}--{2}" .format(root, dirs, files))
                for dir in dirs:
                    spath = self.spath(path, root, dir)
                    spath.IsDir = True
                    d[spath.SPath] = spath
                    #print(str(spath.SPath))
                for file in files:
                    spath = self.spath(path, root, file)
                    spath.IsFile = True
                    spath.MD5 = hashlib.md5(open(spath.AbsPath, 'rb').read())
                    d[spath.SPath] = spath
                    #print(str(spath.SPath))
            # pprint(d)
            return d
        except Exception as e:
            print(e)

    def remove(self, src: SyncPath):

        logging.debug("Removing {0}".format(src.AbsPath))
        if src.IsDir:
            shutil.rmtree(src.AbsPath, ignore_errors=False, onerror=None)
        else:
            os.remove(src.AbsPath)

    def copy_local2local(self, src: SyncPath, baseDir):
        try:
            path = os.path.normpath(baseDir + src.SPath)
            logging.debug("copy_local_local->{0}".format(path))

            if src.IsDir:
                os.makedirs(path, exist_ok=True)
            else:
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                shutil.copy2(src.AbsPath, path, follow_symlinks=False)
        except Exception as e:
            print("Error Copying")


class SAzure(SyncStorage):
    def __init__(self):
        super().__init__()
        self.msg_key_na = _('Key not available')
        try:
            import alxlib.key

            key = alxlib.key.Key()
            if os.path.isfile(key.get_path()):
                sys.path.insert(0, key.get_dir())

                import alxkey

                self.key = alxkey.alxkey_azure
                """self.blob = BlobService(account_name=self.key['AZURE_STORAGE_ACCOUNT_NAME'],
                                        account_key=self.key['AZURE_ACCESS_KEY'])"""
            else:
                # raise (self.msg_key_na)
                self.key = None
        except:
            pass
            # raise (self.msg_key_na)

    def connect(self):
        try:

            self.blob = BlobService(account_name=self.key['AZURE_STORAGE_ACCOUNT_NAME'],
                                    account_key=self.key['AZURE_ACCESS_KEY'])

            return self.blob.list_containers(maxresults=1)

        except:
            return None

    def connect_blob(self, az_account_name=None, az_account_key=None):

        try:
            if az_account_name != None:
                self.key['AZURE_STORAGE_ACCOUNT_NAME'] = az_account_name
                self.key['AZURE_ACCESS_KEY'] = az_account_key

            return self.connect()

        except:
            return None

    def path_clean(self, path: str):
        try:
            i = path.index("//") + 2
            self.container = path[0:i]
            if path[len(path) - 1] != "/":
                path += "/"

            return path[i:]
        except:
            print(_("Bad Path"))
            exit(1)

    def spath(self, container, root, b):
        spath = SyncPath()
        spath.BasePath = container
        if b.name[len(b.name)-1]=="/":
            spath.IsDir= True
        else:
            spath.IsFile= True
        spath.AbsPath = b.name
        if len(root)>0:
            spath.SPath = b.name[len(root) - 1:]
        else:
            spath.SPath=b.name
        spath.Size = b.properties.content_length
        import alxlib.time_help

        spath.ModifiedTS = alxlib.time_help.to_timestamp(b.properties.last_modified)
        spath.MD5 = b.properties.content_md5
        spath.sys="azure"
        return spath

    def path_split(self, path: str):
        try:
            list = path.split("/")
            container = list[0]
            uri = ""
            if len(list) > 1:
                uri = "/".join(map(str, list[1:]))

            return container, uri
        except:
            print(_("Bad path"))
            exit(1)

    def path_list_blobs(self, container, uri):

        try:
            if len(uri)>0:
                blobs = self.blob.list_blobs(container, prefix=uri)
            else:
                blobs = self.blob.list_blobs(container)


            """for blob in blobs:
                print(blob.properties.__dict__)
                print(blob.name)
                print(blob.url)"""
            return blobs
        except Exception as e:
            print(_("Bad connection"))
            logging.warning("container {0}, path {1}".format(container, uri))
            exit(1)

    def path_list(self, path):
        try:
            logging.debug("path_list {0}".format(path))

            container, uri = self.path_split(path)
            logging.debug("Container: {0}, Uri: {1}".format(container, uri))

            self.connect()
            self.blob.create_container(container)

            blobs = self.path_list_blobs(container, uri)

            d = {}

            for b in blobs:
                spath = self.spath(container, uri, b)
                # print(b.__dict__)
                #print(str(b.properties.last_modified.__dict__))
                #print(str(spath.ModifiedTS))
                d[spath.SPath] = spath
            # print(d)
            return d
        except Exception as e:
            print(e)

    def remove(self, src: SyncPath):
        try:
            logging.debug("Removing {0}".format(src.AbsPath))
            self.connect()
            self.blob.create_container(src.BasePath)
            self.blob.delete_blob(src.BasePath, src.AbsPath)
        except:
            pass


    def copy_local2azure(self, src, base_dir):
        try:

            container, uri = self.path_split(base_dir)

            if len(src.SPath)>0 and src.SPath[0]=="/":
                path= uri+ src.SPath[1:]
            else:
                path= uri+src.SPath
            logging.debug("copy_local2azure Spath {0}. path:{1}".format(src.SPath, path))
            self.connect()
            if not src.IsDir:
                self.blob.put_block_blob_from_path (container, path, src.AbsPath)
            else:
                self.blob.put_block_blob_from_text(container, path+"/", "")
        except Exception as e:
            print("Error Copying")
            print(e)

    def copy_azure2local(self, src, base_dir):
        try:

            if len(src.SPath)>0 and (src.SPath[0] == "/" or src.SPath[0] == "\\") :
                path = src.SPath[1:]
            else:
                path = src.SPath


            path= os.path.normpath(os.path.join(base_dir, path))
            logging.debug("copy_azure2local basedir:{0} Spath {1}, path {2}, abs: {3}".format( base_dir, src.SPath, path, src.AbsPath))


            if not os.path.isdir(path):
               os.makedirs(os.path.dirname(path), exist_ok=True)
            #print( os.path.dirname(path)+"***************")

            if not (len(src.AbsPath)>0 and src.AbsPath[len(src.AbsPath)-1]=="/"):
                self.blob.get_blob_to_path(src.BasePath, src.AbsPath, path)




            """container, uri = self.path_split(base_dir)

            if len(src.SPath)>0 and src.SPath[0]=="/":
                path= uri+ src.SPath[1:]
            else:
                path= uri+src.SPath
            self.connect()
            if not src.IsDir:
                self.blob.get_blob_to_path(src.BasePath, path, src.AbsPath)
            else:
                self.blob.put_block_blob_from_text(container, path, "")"""
        except Exception as e:
            print("Error copying")
            print(e)





