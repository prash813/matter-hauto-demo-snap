# matter-hauto-demo-snap
Sample application to communicate with matter chip-tool.
In a nutshell this web application runs webUI for commisioning matter devices and once they are commissioned they can then be controlled.
To commission devices , device details need to be provided through devicelist.json file which need to be copied to ```$SNAP_DATA/mnt``` dir.
device operation sequences for demo purposes need to be provided thru opemodes.json file which is also need to be copied to ```$SNAP_DATA/mnt``` dir.
## resource files info
- firstapp.py-: commissioning application
- pywrapper.sh-: calls firstapp.py
- thirdapp.py-: device operation application
- matterdemo.sh-: calls thirdapp.py
- devicelist.json-: details about devices to be part of demo
- opmodes.json-: details about demo sequences
- opmodes1.json and devicelist1.json-: these are subset of data listed in above two files 
- templates and static-: these two folder carries web ui assets
## building the snap
currently this snap doesnt support crossbuild

command to build the snap is-:
```
snapcraft --destructive-mode --verbosity=verbose

```

### Running the snap
- sanp has got two services and which listens on the IP of the interface(that user set thru snap config) ports used are 5001 and 5002
- to set network interface for the snap services use command
  ```
    snap set matter-hauto-demo-wweb nwiface=<name of network interface like wlan0 wlp1s0 etc>
  
  ```
 if you want debug messages then also set
 ```
    snap set matter-hauto-demo-wweb debug=true
``` 
 
