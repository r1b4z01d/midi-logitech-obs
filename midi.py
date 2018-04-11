import mido
from subprocess import call
from pyautogui import hotkey

def scale(OldValue,OldMin,OldMax,NewMin,NewMax):
	NewRange = (NewMax - NewMin)
	OldRange = (OldMax - OldMin)  
	if (OldRange == 0):
	    NewValue = NewMin
	else:  
	    NewValue =  (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	return NewValue

def turnOnLED(channel,control):
	msg = mido.Message('control_change', channel=channel, control=control, value=127, time=0)
	oPort = mido.open_output('BCR2000:BCR2000 MIDI 1 32:0')
	oPort.send(msg)

def turnOffLEDs():
	oPort = mido.open_output('BCR2000:BCR2000 MIDI 1 32:0')
	msg = mido.Message('control_change', channel=7, control=108, value=0, time=0)
	oPort.send(msg)
	msg = mido.Message('control_change', channel=7, control=107, value=0, time=0)
	oPort.send(msg)
	msg = mido.Message('control_change', channel=7, control=106, value=0, time=0)
	oPort.send(msg)

cameras = ["/dev/video0","/dev/video1","/dev/video2"]
knobs = [
	{'control':97,'camera':"/dev/video0",'param':"exposure_absolute=",'min':3,'max':1200},
	{'control':89,'camera':"/dev/video0",'param':"focus_absolute=",'min':0,'max':250},
	{'control':81,'camera':"/dev/video0",'param':"zoom_absolute=",'min':100,'max':120},
	{'control':98,'camera':"/dev/video1",'param':"exposure_absolute=",'min':3,'max':1200},
	{'control':90,'camera':"/dev/video1",'param':"focus_absolute=",'min':0,'max':250},
	{'control':82,'camera':"/dev/video1",'param':"zoom_absolute=",'min':100,'max':120},
	{'control':99,'camera':"/dev/video2",'param':"exposure_absolute=",'min':3,'max':1200},
	{'control':91,'camera':"/dev/video2",'param':"focus_absolute=",'min':0,'max':250},
	{'control':83,'camera':"/dev/video2",'param':"zoom_absolute=",'min':100,'max':120}
]
hotkeys = [{'key':"b",'control':107},{'key':"g",'control':108}]

#Turn off auto focus and exposure on all cameras
for camera in cameras:
	call(["v4l2-ctl","-d",camera,"-c","focus_auto=0"])
	call(["v4l2-ctl","-d",camera,"-c","exposure_auto=1"])

with mido.open_input('BCR2000:BCR2000 MIDI 1 32:0') as port:
    for message in port:
	daMessage = message.bytes()
	try:
		if daMessage[1] == 107:
			hotkey('ctrl', 'b')
			turnOffLEDs()
			turnOnLED(7,107)
		elif daMessage[1] == 108:
			hotkey('ctrl', 'g')
			turnOffLEDs()
			turnOnLED(7,108)
		elif daMessage[1] == 106:
			hotkey('ctrl', 'l')
			turnOffLEDs()
			turnOnLED(7,106)

		else:
			knobData = (knob for knob in knobs if knob["control"] == daMessage[1]).next()
			param = knobData['param']+str(scale(daMessage[2],0,127,knobData['min'],knobData['max']) )
			print knobData['camera'] +" - "+ param
			call(["v4l2-ctl","-d",knobData['camera'],"-c",param])
	except Exception as e:
		print message
		print e