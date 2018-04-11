import mido
from subprocess import call
def scale(OldValue,OldMin,OldMax,NewMin,NewMax):
	NewRange = (NewMax - NewMin)
	OldRange = (OldMax - OldMin)  
	if (OldRange == 0):
	    NewValue = NewMin
	else:  
	    NewValue =  (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	return NewValue

knobs = [
	{'channel':97,'camera':"/dev/video0",'param':"exposure_absolute=",'min':3,'max':1200},
	{'channel':89,'camera':"/dev/video0",'param':"focus_absolute=",'min':0,'max':250},
	{'channel':81,'camera':"/dev/video0",'param':"zoom_absolute=",'min':100,'max':120},
	{'channel':98,'camera':"/dev/video1",'param':"exposure_absolute=",'min':3,'max':1200},
	{'channel':90,'camera':"/dev/video1",'param':"focus_absolute=",'min':0,'max':250},
	{'channel':82,'camera':"/dev/video1",'param':"zoom_absolute=",'min':100,'max':120},
	{'channel':99,'camera':"/dev/video2",'param':"exposure_absolute=",'min':3,'max':1200},
	{'channel':91,'camera':"/dev/video2",'param':"focus_absolute=",'min':0,'max':250},
	{'channel':83,'camera':"/dev/video2",'param':"zoom_absolute=",'min':100,'max':120}
]

#Turn off auto focus and exposure on all cameras
#TODO: Iterate over cameras not knobs.
for knob in knobs:
	call(["v4l2-ctl","-d",knob['camera'],"-c","focus_auto=0"])
	call(["v4l2-ctl","-d",knob['camera'],"-c","exposure_auto=1"])

with mido.open_input('BCR2000:BCR2000 MIDI 1 32:0') as port:
    for message in port:
	daMessage = message.bytes()
	try:
		knobData = (knob for knob in knobs if knob["channel"] == daMessage[1]).next()
		param = knobData['param']+str(scale(daMessage[2],0,127,knobData['min'],knobData['max']) )
		print knobData['camera'] +" - "+ param
		call(["v4l2-ctl","-d",knobData['camera'],"-c",param])
	except:
		print message
