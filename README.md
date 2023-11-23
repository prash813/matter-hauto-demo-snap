# matter-hauto-demo-snap
sample application to communicate with matter chip-tool
## resource file info
- firstapp.py-: commissioning application
- pywrapper,sh-: calls firstapp.py
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
- sanp has got two services and listens on the IP of the interface(that user set thru snap config) ports used are 5001 and 5002
- to set network interface for the snap services use command
  ```
    snap set matter-hauto-demo-wweb nwiface=<name of network interface like wlan0 wlp1s0 etc>
  
  ```
 if you want debug messages then also set
 ```
    snap set matter-hauto-demo-wweb debug=true
``` 
- 
