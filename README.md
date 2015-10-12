# monitoring
tiny client server system monitoring with python and bash

This program read monitoring ini file and rutuerns a json output based on this ini file. for getting better performance program creates number of threads based on number of commands in ini file.<br/>
for python web framework i used django but you can use anything else you want. ini file section example:<br/>
<br/>
[disk_root]<br/>
cmd_total: df -lh | awk '{if ($6 == "/") { print $2 }}' | head -1 | cut -d'G' -f1 | tr -d '\n'<br/>
cmd_used: df -lh | awk '{if ($6 == "/") { print $3 }}' | head -1 | cut -d'G' -f1 | tr -d '\n'<br/>
unit: G<br/>
graph_type: gauge<br/>
<br/>
also you can run scripts and send output,like this section, just you have to put your scripts in plugins folder:<br/>
<br/>
[python_example]<br/>
cmd_result: ./ac.py <br/>
graph_type: text<br/>
<br/>
you have to use the example ini file to set gauges and text outputs.<br/>
gauges needs: cmd_total and cmd_used and graph_type: gauge<br/>
texts needs: cmd_result, graph_type: text<br/>
<br/>
then you have to put fontend folder on your monitoring statiton , and you have to set the ip and name of you monitored
system in index.html nodes variable:<br/>
<br/>
var nodes=[{name:'local', url:'http://localhost:8001/1234567'}]<br/>
<br/>
It will create seperate tabs for each node with highchart graph for gauges and text blocks for text outputs.<br/>
<br/>
