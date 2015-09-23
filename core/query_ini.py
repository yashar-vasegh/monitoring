#!/usr/bin/env python
import ConfigParser
import platform
from threading import Thread
import subprocess 
import Queue
from django.conf import settings
import os


config_file_path = os.path.join(settings.BASE_DIR, 'core')
plugins_path = os.path.join(config_file_path, 'plugins')

output = {}
output['system_info'] = {        
    'architecture': platform.architecture(),
    'dist': platform.dist(),
    'machine': platform.machine(),
    'node': platform.node(),
    'platform': platform.platform(),
    'processor': platform.processor(),
    'system': platform.system(),
    'uname': platform.uname(),
    'version': platform.version(),
    }


config = ConfigParser.ConfigParser()
config.read(os.path.join(config_file_path,'monitoring.ini'))
queue = Queue.Queue()

def get_cmd(params):
    for item in params:
        if item[0] == 'cmd': return item[1]

def Command_runner(queue):
           
    while True:
        cmd_name, cmd_params = queue.get()
        cmd = get_cmd(cmd_params)
        command = subprocess.Popen('cd %s;%s'%(plugins_path,cmd), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = command.communicate()
        output[cmd_name] = {}
        for item in cmd_params:
            if item[0] != 'cmd' : output[cmd_name][item[0]]=item[1]
        output[cmd_name]['result'] = out
        queue.task_done()    


def fill_queue():
    for section in config.sections():        
            queue.put((section,config.items(section))) 
            # ('disk_usage_root',[('type', 'bash'), ('cmd', "df / | awk {'print $5'} | tail -n1")])
    
    
def main():
    fill_queue()
    
    if queue.qsize() > 16:
        MAX_THREAD_CMD = 10
    else:
        MAX_THREAD_CMD = 3
        
    for i in range(MAX_THREAD_CMD):
        worker = Thread(target=Command_runner, args=(queue,))
        worker.setDaemon(True)        
        worker.start()

    queue.join()
    return output


if __name__ == '__main__':
    print main()
