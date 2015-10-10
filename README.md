# monitoring
tiny client server system monitoring with python and bash

This program read monitoring ini file and rutuerns a json output based on this ini file. for getting better performance 
program creates number of threads based on number of commands in ini file.
for python web framework i used django but you can use anything else you want. ini file section example:

[disk_root]
cmd_total: df -lh | awk '{if ($6 == "/") { print $2 }}' | head -1 | cut -d'G' -f1 | tr -d '\n'
cmd_used: df -lh | awk '{if ($6 == "/") { print $3 }}' | head -1 | cut -d'G' -f1 | tr -d '\n'
unit: G
graph_type: gauge

also you can run scripts and send output,like this section, just you have to put your scripts in plugins folder:

[python_example]
cmd_result: ./ac.py 
graph_type: text

you have to use the example ini file to set gauges and text outputs.
gauges needs: cmd_total and cmd_used and graph_type: gauge
texts needs: cmd_result, graph_type: text

then you have to put fontend folder on your monitoring statiton , and you have to set the ip and name of you monitored
system in index.html nodes variable:

var nodes=[{name:'local', url:'http://localhost:8001/1234567'}]

it will create highchart graph for gauges and text blocks for text outputs.

It will create tab to each node to monitor it.
