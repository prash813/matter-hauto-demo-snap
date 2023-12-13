from flask import Flask, request
from flask import render_template
from devicelist import DeviceList
from OpModes import OpModes 
from matterbulbop import MatterBulbOp
import os
import subprocess
import json
import sys
app = Flask(__name__)
devicelist1 = None
reqipaddr = None
DeviceDataBase= None
OperationModesDb = None
demolist=None


def getip():
    global reqipaddr
    ifacename=os.environ.get('NWIFACE')
    print(ifacename)
    ipstring = "ip addr show " + ifacename + "| grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"      
    s = subprocess.check_output([ipstring], stdin=None, stderr=None, shell=True, universal_newlines=True)
    if len(s) != 0:
        reqipaddr = s[0:len(s)-1]
    
def QueueTheOperations(listops):
    cmdstr=""
    for i in listops:
        cmdstr+=i + '; echo; echo; echo; '
    return cmdstr
'''
def QueueTheOperations(listops):
    cmdstr=""
    cmddelay=os.environ.get('CMDDELAY')
    for i in listops:
        cmdstr+=i + '; echo; echo; echo; ' + 'sleep ' + cmddelay + '; '
    return cmdstr
'''    
@app.route('/Performdevops', methods=['GET'])
def PerformDeviceOps():
    global devicelist1
    global OperationModesDb
    prevnodeid=0
    CHIPCmdList=""
    snapvar = os.environ.get('SNAP')
    cmddelay=os.environ.get('CMDDELAY')
    tmpstr= "sleep " + cmddelay 
    pathvar=snapvar + "/extra-bin/chip-tool "
    
    try:
        reqargs=request.args.to_dict()
        demoname=reqargs.get("demoname")
        deviceops=OpModes.Getdevops(OperationModesDb["operationmodes"], demoname)
        print(deviceops)
        listlen=len(deviceops)
        itemcount=0
        Res= {"PerformdevOpsRes": "Failure"}
        for idx in deviceops:
            nodeid = DeviceList.GetDeviceNodeID(devicelist1, idx["devicename"])
            itemcount=itemcount+1            
            
            if nodeid == '0':
                nodeid=DeviceList.GetBridgeDeviceNodeID(DeviceDataBase, idx["devicename"])
            if nodeid != '0':    
                devicetype = DeviceList.GetDeviceType(devicelist1, idx["devicename"])
                print(devicetype)
                if devicetype in ["bridge","light", "plug", "light switch", "musicplayer"]:
                    listops=MatterBulbOp.PerformBulbOp(idx, nodeid, pathvar)
                    #if listlen > 1 and itemcount < listlen:
                    listops.append(tmpstr)
                        
                    CHIPCmdList+=QueueTheOperations(listops)
                    Res["PerformdevOpsRes"] = "Success"
        print(CHIPCmdList)
        sys.stdout.flush()
        subprocess.call([CHIPCmdList], stdin=None, stderr=None, shell=True, universal_newlines=True)
        return Res            
    except:
        print("some failure")
        
@app.route('/')
def hello_world():
    global devicelist1
    global DeviceDataBase
    global reqipaddr
    global demolist
    global OperationModesDb
    if OperationModesDb is None:
        OperationModesDb={}
    if demolist is None:
        demolist = []
    if devicelist1 is None:
        devicelist1 = []
    if reqipaddr is None:
        reqipaddr = "127.0.0.1"
    if DeviceDataBase is None:
        DeviceDataBase = {}
    getip()    
    pathname = os.environ.get('TMPDIR')
    fname=pathname + "/devicelist.json"
    print(pathname, fname)
    DeviceDataBase=DeviceList.getdata(fname)
    devicelist1=DeviceList.GetDeviceList(DeviceDataBase["devices"])
    opmodefile=pathname + '/opmodes.json'
    OperationModesDb=OpModes.GetData(opmodefile)
    demolist = OpModes.GetDemoList(OperationModesDb["operationmodes"])
    print(demolist)
    
    isdebug=os.environ.get('DEBUG')
    if isdebug == "true": #This is original woking code as on Aug17 2023 	
        return render_template('/devicedemo.html', ipaddr=reqipaddr, devicedemolist=demolist)
    elif isdebug== "false":
        return render_template('/devicedemo_nodbg.html', ipaddr=reqipaddr, devicedemolist=demolist)
    else:
        return render_template('/devicedemo.html', ipaddr=reqipaddr, devicedemolist=demolist)
    
if __name__ == '__main__':
    reqipaddr=None
    ifacename=os.environ.get('NWIFACE')
    print(ifacename)
    ipstring = "ip addr show " + ifacename + "| grep \"inet \" -|awk '{ print $2 }' -|awk -F'/' '{ print $1 }' -"      
    s = subprocess.check_output([ipstring], stdin=None, stderr=None, shell=True, universal_newlines=True)
    if len(s) != 0:
        reqipaddr = s[0:len(s)-1]
    
    if reqipaddr is not None:
        app.run(host=reqipaddr, debug=True, port=5002)
    else:    
        app.run(host='0.0.0.0', debug=True, port=5002)
