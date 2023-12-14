#chip-tool onoff on <nodeid> <endpointid>
#chip-tool onoff off <nodeid> <endpointid>
#chip-tool onoff toggle <nodeid> <endpointid<ep>>
#chip-tool levelcontrol move-to-level <level> <transition T> <OptionMask> <Optionoverrides> <nodeid> <ep>
#chip-tool colorcontrol move-to-hue Hue Direction TransitionTime OptionsMask OptionsOverride dest-nodeid endpoint-id
#chip-tool colorcontrol move-to-hue-and-saturation Hue Saturation TransitionTime OptionsMask OptionsOverride destination-id endpoint-id
import random
import sys
class MatterBulbOp:
    CommandList= { "On": ["onoff", "on", "1", "1"], "Off": ["onoff", "off", "1", "1"], "toggle": ["onoff", "toggle", "1", "1"],
    "brightness":["levelcontrol", "move-to-level", "100", "0", "0", "0", "1", "1"], "color": ["colorcontrol", "move-to-hue", "red", "0", "0", "0", "0", "1", "1"],
    "saturation": ["colorcontrol", "move-to-saturation", "100",  "0", "0", "0", "1", "1"],
    "StartMusic": ["onoff", "on", "1", "1"], "StopMusic": ["onoff", "off", "1", "1"],
    "huesaturation": ["colorcontrol", "move-to-hue-and-saturation", "0", "254", "0", "0", "0", "1", "1"]}
    CorrectColorTable= {"Red":"0","Orange":"15", "Yellow":"30", "Pear":"40", "Green":"85", "Turquoise":"120", "Cyan":"150", "Blue":"175", "Orchid":"200", "Pink":"235"}
    ColorTable= {"Red":"0","Orange":"30", "Yellow":"60","Green":"90", "Spring Green":"150", "Cyan":"180", "Azure":"210", "Blue":"240", "Violet":"270", "Magenta":"300", "Rose":"330"}          
    ColorNames=["Red", "Orange", "Yellow", "Pear", "Green",  "Cyan",  "Blue", "Orchid", "Pink"]
    PrevColrsForDiscoMode={}
    '''
        Mainly useful for onoff cluster commands 
    '''
    def ClearPrevColorNodes():
        MatterBulbOp.PrevColrsForDiscoMode.clear()

    def CheckColor(nodeid, colorname):
        print(nodeid, colorname)
        sys.stdout.flush()
        if str(nodeid) in MatterBulbOp.PrevColrsForDiscoMode.keys():
            if MatterBulbOp.PrevColrsForDiscoMode[str(nodeid)] == colorname:
                print("color on nodeid::", nodeid, "is same as Prev Color So change color")
                return True
        MatterBulbOp.PrevColrsForDiscoMode[str(nodeid)] = colorname
        return False        
        
    def PerformBulbOpX(cmddescr, nodeid, chiptool_cmd):
        cmdlist = []
        print(cmddescr)
        sys.stdout.flush()
        if cmddescr["cmdname"] == "On" or cmddescr["cmdname"] == "Off":
            return MatterBulbOp.PerformBulbOp(cmddescr, nodeid, chiptool_cmd)
        elif cmddescr["cmdname"] == "HueSaturation":
            if cmddescr["color"] == "Random":
                pathvar=chiptool_cmd
                cmdparamlist=MatterBulbOp.CommandList["huesaturation"]
                colorname=random.choice(MatterBulbOp.ColorNames)
                count=0
                print("random color returned is::", colorname, MatterBulbOp.CorrectColorTable[colorname])
                while MatterBulbOp.CheckColor(nodeid, colorname) == True and count < 5:
                    colorname=random.choice(MatterBulbOp.ColorNames)
                    print("random color returned is::", colorname, MatterBulbOp.CorrectColorTable[colorname])
                    count=count+1
                #print(cmdparamlist)
                sys.stdout.flush()
                pathvar+=cmdparamlist[0] + " " + cmdparamlist[1] + " " + MatterBulbOp.CorrectColorTable[colorname] + " " + cmdparamlist[3] + " " 
                pathvar+=cmdparamlist[4] + " " + cmdparamlist[5] + " " + cmdparamlist[6] + " " + str(nodeid) + " " + str(cmddescr["endpoint"])
                cmdlist.append(pathvar) 
                return cmdlist    
            
    def PerformBulbOp(cmddescr, nodeid, chiptool_cmd):
        #chiptool="/extra-bin/chip-tool "
        pathvar=chiptool_cmd
        cmdparamlist=MatterBulbOp.CommandList[cmddescr["cmdname"]]
        pathvar+=cmdparamlist[0] + " " + cmdparamlist[1] + " " + str(nodeid)+ " " + str(cmddescr["endpoint"])
        print(pathvar)
        cmdlist = []
        cmdlist.append(pathvar)
        if "color" in cmddescr.keys():
            pathvar=chiptool_cmd
            cmdparamlist=MatterBulbOp.CommandList["color"]
            pathvar+=cmdparamlist[0] + " " + cmdparamlist[1] + " " + MatterBulbOp.ColorTable[cmddescr["color"]] + " " + cmdparamlist[3] + " " 
            pathvar+=cmdparamlist[4] + " " + cmdparamlist[5] + " " + cmdparamlist[6] + " " + str(nodeid) + " " + str(cmddescr["endpoint"])
            cmdlist.append(pathvar) 
        if "saturation" in cmddescr.keys():
            pathvar=chiptool_cmd
            cmdparamlist=MatterBulbOp.CommandList["saturation"]
            pathvar+=cmdparamlist[0] + " " + cmdparamlist[1] + " " + cmddescr["saturation"] + " " + cmdparamlist[3] + " " + cmdparamlist[4]
            pathvar+= " " + cmdparamlist[5] + " " + str(nodeid) + " " + str(cmddescr["endpoint"])
            cmdlist.append(pathvar) 
        if "brightness" in cmddescr.keys():
            pathvar=chiptool_cmd
            cmdparamlist=MatterBulbOp.CommandList["brightness"]
            pathvar+=cmdparamlist[0] + " " + cmdparamlist[1] + " " + cmddescr["brightness"] + " " + cmdparamlist[3] + " " + cmdparamlist[4]
            pathvar+= " " + cmdparamlist[5] + " " + str(nodeid) + " " + str(cmddescr["endpoint"])
            cmdlist.append(pathvar)
        
        print(cmdlist)
        sys.stdout.flush()
        return cmdlist    
