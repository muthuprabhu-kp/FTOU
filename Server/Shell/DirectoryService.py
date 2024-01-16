import json
import os
import pwd
from datetime import datetime
from pathlib import Path


class DirectoryService:
    def __init__(self, user):
        self.home_dir = user.get_user_home()
        self.current_dir = user.get_user_home()

    def get_path(self, file_path=None):
        fpath = file_path or self.current_dir
        path = Path(fpath)

        return path

    def get_size(self, size):
        if size < 1024:
            return f"{size} bytes"
        elif size < pow(1024, 2):
            return f"{round(size / 1024, 2)} KB"
        elif size < pow(1024, 3):
            return f"{round(size / (pow(1024, 2)), 2)} MB"
        elif size < pow(1024, 4):
            return f"{round(size / (pow(1024, 3)), 2)} GB"

    def check_permission(self, path=None):
        current_user_group = pwd.getpwuid(os.getgid())[0]
        fpath = path or self.get_path()
        owner = fpath.owner()
        group = fpath.group()
        # Print real user id of the current process
        # print(current_user)
        # print(fpath.)
        # print(owner, group)
        return current_user_group == group

    def cd(self, path):
        if not path:
            return "Path can not be empty"

        pass

    def ls(self, options=None):
        files_info = []
        try:
            path = Path(self.current_dir)
            has_permission = self.check_permission(path)
            files = [f for f in path.iterdir()]
            # print(files)
            if not has_permission:
                return "You dont have enough permission to list dir"
            for f in files:
                stat = f.lstat()
                m_date = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                f_size = self.get_size(stat.st_size) if not f.is_dir() else '_'
                files_info.append({'name': str(f), 'size': f_size, "modified_date": m_date})
        except Exception as e:
            print(e)
            return "You dont have enough permission to list dir"
        return json.dumps(files_info)


if __name__ == '__main__':
    a = DirectoryService('/home/hackers')
    print(a.check_permission())
    print(a.ls())
