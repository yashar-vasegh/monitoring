#!/usr/bin/env python
import ConfigParser
import platform
from threading import Thread
import subprocess 
import Queue
from django.conf import settings
import os
import collections


config_file_path = os.path.join(settings.BASE_DIR, 'core')
plugins_path = os.path.join(config_file_path, 'plugins')

output = collections.OrderedDict()

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

def get_cmds(params):
    commands = []
    for item in params:
        if item[0].startswith('cmd_'): commands.append((item[0][4:],item[1]))
    return commands

def Command_runner(queue):
           
    while True:
        section_name, cmd_params = queue.get()
        output[section_name] = {}        
        cmds = get_cmds(cmd_params)
        for cmd in cmds:
            cmd_name, cmd_rule = cmd
            command = subprocess.Popen('cd %s;%s'%(plugins_path,cmd_rule), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, err = command.communicate()
            output[section_name][cmd_name] = out 
        for item in cmd_params:
            item_name, item_value = item
            if not item[0].startswith('cmd_') : output[section_name][item_name]=item_value        
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
