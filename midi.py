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

cameraParams = ["exposure_absolute=","focus_absolute=","zoom_absolute="]
paramsMin = [3,0,100]
ParamsMax = [1200,250,140]
paramsChannel = [97,89,81]

with mido.open_input('BCR2000:BCR2000 MIDI 1 32:0') as port:
    for message in port:
	daMessage = message.bytes()
	try:
		daIndex = paramsChannel.index(daMessage[1])
		param = cameraParams[daIndex]+str(scale(daMessage[2],0,127,paramsMin[daIndex],ParamsMax[daIndex]) )
		print param
		call(["v4l2-ctl","-c",param])
	except:
		print message
