import os 
from datetime import datetime

from pygitup.generic import get_content, set_content_append


class git_adapter:
    def __init__(self, logs = None, dummy  = "./dummy.txt"):
        self.logs = logs
        self.dummy = dummy
        


    def shell(self, command, path, local_print = None):
        path = path.replace('\\', '/')
        drive, _ = os.path.splitdrive(path)
        if os.name == 'nt':
            cmd = f'{drive} && cd {path} && {command} > {self.dummy} 2>&1'  
        else:
            cmd = f'cd {path} && {command} > {self.dummy} 2>&1'  

        if local_print:
            local_print(cmd)
        os.system(cmd)
        ret = get_content(self.dummy)
        os.remove(self.dummy)
        if local_print:
            local_print(ret)
        return ret
    

    
    def get_remotes(self, path):
        ret = self.shell('git branch -r' , path)
        ret = ret.split('\n')
        ret = [r.strip() for r in ret if '->' not in r]
        ret = [r.split('/') for r in ret if len(r) > 0]

        return ret
    
    def get_remote_locations(self,path):
        remotes = self.shell('git remote -v', path)
        remotes = remotes.split('\n')
        remotes =[r.split('\t')[1].split('(')[0].strip().replace('\\', '/') for r in remotes if len(r.strip())> 0]
        return remotes
    
    def get_remote_network(self, path):

        ret = [path.replace('\\', '/')]
        ret_length = 0
        while len(ret) > ret_length:
            ret_length = len(ret)
            for p in ret:
                if not os.path.exists(p):
                    continue
                rs = self.get_remote_locations(p)
                for r in rs:
                    if r not in ret:
                        ret.append(r)
        
        return ret
                

    
    def get_date_string(self):
        current_date = datetime.now() 
        # Format the date as a string 
        date_string = current_date.strftime("%Y-%m-%d")
        return date_string
    

    def add_all(self, path):
        ret = self.shell('git add *' , path, print)
        if self.logs is not None:
            set_content_append(self.logs, ret)
        

    def commit(self, path, message):
        ret = self.shell(f'git commit -m "{message}"' , path, print)
        if self.logs is not None:
            set_content_append(self.logs, ret)


    def pull(self, path, remote, branch):
        ret = self.shell(f'git pull {remote} {branch}'   , path, print)
        if self.logs is not None:
            set_content_append(self.logs, ret)
        

    def update_folder(self, path):
        self.add_all(path)
        self.commit(path, self.get_date_string())
        remotes = self.get_remotes(path)
        for r in remotes:
            self.pull(path, r[0], r[1]) 