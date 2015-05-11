__author__ = 'Alex Gomes'

"""
alx sync dir /home/file/ /tmp/file

Paramiko

"""

import logging
from pprint import pprint
from gettext import gettext as _

from alxlib.sync.path import SyncPath
import alxlib.sync.sys


class Sync(object):
    def __init__(self):
        pass


    def ssh_host_check(self, path):
        ssh_host = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]+\s*:\s*$"
        ssh_host = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\s*:\s*$"
        import re

        if re.match(ssh_host, path):
            return True
        else:
            return False

    def path_type(self, path):
        if path.startswith("s3://"):
            return "s3"
        elif self.ssh_host_check(path):
            return "ssh"
        elif path.startswith("az://"):
            return "azure"
        else:
            return "local"


    def path_reduce(self, a, b):
        try:
            import copy

            item2 = b.copy()
            # pprint(b)
            for key, value in item2.items():
                if a.get(key, None) is not None:
                    if a[key].IsDir and b[key].IsDir:
                        del a[key]
                        del b[key]
                    elif a[key].MD5 == b[key].MD5:
                        del a[key]
                        del b[key]
                    elif a[key].ModifiedTS == b[key].ModifiedTS:
                        #print("key->{0}".format(key))
                        del a[key]
                        del b[key]
                    elif float(a[key].ModifiedTS) < float(b[key].ModifiedTS):
                        del a[key]
                    else:
                        del b[key]
            return a, b
        except Exception as e:
            print(e)

    def wrap_text(self, text, max_width):
        if text is not None:
            from textwrap import wrap

            return '\n'.join(wrap(text, max_width))
        else:
            return ""

    def print_compare(self, src, dst, a, b, sym):

        from colorclass import Color, Windows

        from terminaltables import SingleTable

        Windows.enable(auto_colors=True, reset_atexit=True)  # Does nothing if not on Windows.

        max_width = 50
        l = [Color('{autocyan}' + self.wrap_text(src, max_width) + '{/autocyan}'),
             sym[0],
             Color('{autocyan}' + self.wrap_text(dst, max_width) + '{/autocyan}')]
        table_data = []
        table_data.append(l)

        for key, value in a.items():
            l = [self.wrap_text(key, max_width), sym[1], ""]
            table_data.append(l)
        for key, value in b.items():
            l = ["", sym[2], self.wrap_text(key, max_width)]
            table_data.append(l)

        table = SingleTable(table_data)
        table.inner_heading_row_border = True
        table.inner_row_border = True
        print(table.table)

    def sync_main(self, src, dst, option, verbose):

        try:
            src_type = self.path_type(src)
            dst_type = self.path_type(dst)

            sys_src = sys_dst = alxlib.sync.sys.SyncStorage()

            if src_type == "local":
                sys_src = alxlib.sync.sys.SLocal()
            elif src_type == "azure":
                sys_src = alxlib.sync.sys.SAzure()

            if dst_type == "local":
                sys_dst = alxlib.sync.sys.SLocal()
            elif dst_type == "azure":
                sys_dst = alxlib.sync.sys.SAzure()
                conn=sys_dst.connect_blob()
                if conn is None:
                    account_name=input("AZURE_STORAGE_ACCOUNT_NAME:")
                    account_key=input("AZURE_ACCESS_KEY:")
                    conn=sys_dst.connect_blob(az_account_name=account_name, az_account_key=account_key)
                    if conn is None:
                        print(_("Cannot connect to Azure"))
                        exit(1)




            self.src_path = sys_src.path_clean(src)
            self.src_list = sys_src.path_list(self.src_path)


            self.dst_path = sys_dst.path_clean(dst)
            self.dst_list = sys_dst.path_list(self.dst_path)

            #print(self.dst_path)
            #exit(1)

            # print(self.src_list)



            a, b = self.path_reduce(self.src_list.copy(), self.dst_list.copy())

            #self.print_compare(src, dst, a, b, ["=!=", "==>", "<=="])
            #print(len(a))
            #print(len(b))

            if len(a) == 0 and len(b) == 0:
                print(_("Directory is already synchronized"))
            elif option == "mirror":
                tmp = b.copy()
                for key, value in tmp.items():
                    item = self.src_list.get(key, None)
                    if item != None:
                        #a[key] = item
                        del b[key]
                n = len(a) + len(b)
                if n > 0:
                    if verbose:
                        self.print_compare(src, dst, a, b, ["act", "==>", "del"])
                    print(_("{0} files/directories will be updated ==>".format(len(a))))
                    print(_("{0} files/directories will be deleted (del)".format(len(b))))
                    choice = input(_("Proceed? [y] Yes  [a] Yes to All  [n] No:")).lower()
                    if choice.lower() != "n":
                        for key, value in b.items():
                            if choice.lower() != 'a':
                                if input("{0} (del)(y/n):".format(value.AbsPath)).lower() == "y":
                                    sys_dst.remove(value)
                            else:
                                sys_dst.remove(value)
                        for key, value in a.items():
                            if choice.lower() != 'a':
                                if input("{0} ==>(y/n):".format(value.AbsPath)).lower() == "y":
                                    sys_src.copy(value, self.dst_path, src_type, dst_type, sys_src, sys_dst)
                            else:
                                sys_src.copy(value, self.dst_path, src_type, dst_type, sys_src, sys_dst)
                else:
                    print(_("Destination is already mirrored"))



                                #delete b
            elif option == "merge":
                if verbose:
                    self.print_compare(src, dst, a, b, ["act", "==>", "<=="])
                n = len(a) + len(b)
                if n > 0:
                    print(_("{0} files/directories will be merged <==>".format(n)))
                    choice = input(_("Proceed? [y] Yes  [a] Yes to All  [n] No:")).lower()
                    if choice.lower() != "n":
                        for key, value in a.items():
                            if choice.lower() != 'a':
                                if input("{0} ==>(y/n):".format(value.AbsPath)).lower() == "y":
                                    sys_src.copy(value, self.dst_path, src_type, dst_type, sys_src, sys_dst)
                            else:
                                sys_src.copy(value, self.dst_path, src_type, dst_type, sys_src, sys_dst)
                        for key, value in b.items():
                            if choice.lower() != 'a':
                                if input("{0} <==(y/n):".format(value.AbsPath)).lower() == "y":
                                    sys_src.copy(value, self.src_path, dst_type, src_type, sys_dst, sys_src)
                            else:
                                sys_src.copy(value, self.src_path, dst_type, src_type, sys_dst, sys_src)
            elif option == "update":
                n = len(a)
                if n > 0:
                    if verbose:
                        self.print_compare(src, dst, a, b, ["act", "==>", "no"])
                        print(_("{0} files/directories will be updated ==>".format(n)))
                        choice = input(_("Proceed? [y] Yes  [a] Yes to All  [n] No:")).lower()
                        if choice.lower() != "n":
                            for key, value in a.items():
                                if choice.lower() != 'a':
                                    if input("{0} ==>(y/n):".format(value.AbsPath)).lower() == "y":
                                        sys_src.copy(value, self.dst_path, src_type, dst_type, sys_src, sys_dst)
                                else:
                                    sys_src.copy(value, self.dst_path, src_type, dst_type, sys_src, sys_dst)
                else:
                    print(_("Destination is already up to date"))

            else:
                if verbose:
                    self.print_compare(src, dst, a, b, ["act", "==>", "<=="])
                print(_("{0} files/directories are different ==>".format(len(a) + len(b))))







        except Exception as e:
            logging.debug("sync_main {0}".format(e))
            print("Error")
            raise ()


    def sync_update(self, src, dst, verbose):
        self.sync_main(src, dst, "update", verbose)

    def sync_mirror(self, src, dst, verbose):
        self.sync_main(src, dst, "mirror", verbose)

    def sync_merge(self, src, dst, verbose):
        self.sync_main(src, dst, "merge", verbose)

    def sync_compare(self, src, dst, verbose):
        self.sync_main(src, dst, "compare", verbose)