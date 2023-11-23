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
