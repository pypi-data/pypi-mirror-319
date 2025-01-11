import os
import argparse
from pygitup import generic
from pygitup import programs
from pygitup.git_adapter import git_adapter

def to_absolute(p):
    p = p if os.path.isabs(p) else os.path.join(os.getcwd(), p)
    return p

def update(cmdargs):
    parser = argparse.ArgumentParser(description='update repository')
    parser.add_argument('--path',      help='Path to repository',default=None,required=True)
    parser.add_argument('--logs',      help='Path to folder for log files',default=None,required=False)

    args = parser.parse_args(cmdargs[2:])
    
    logs = to_absolute(args.logs) +"/logs.txt" if args.logs else None
    dummy = to_absolute(args.logs) +"/dummy.txt" if args.logs else  os.getcwd() + "/dummy.txt"
    status_file = to_absolute(args.logs) +"/status.txt" if args.logs else None
    git = git_adapter(
        logs = logs, 
        dummy = dummy
    )
    path = args.path
    path = to_absolute(path)
    if not os.path.exists(path):
        exit(1)
    
    if status_file:
        generic.set_content(status_file, 'in progress')

    remotes = git.get_remote_network(path)
    for i in range(2):
        for path in remotes:
            if os.path.exists(path):
                print(i, "process: ", path)    
                git.update_folder(path)
            else: 
                print(i, "path not found: ", path)    

    if status_file:
        generic.set_content(status_file, 'done')



programs.add_program("update", update)