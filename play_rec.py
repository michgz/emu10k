
"""
Investigate the channels routings in SBLive soundcard, by playing a WAV file
into it and seeing what comes back out.

Command line ALSA tools are used for this. There is a low-level API (maybe
check out https://pypi.org/project/pyalsaaudio/), but I'm not sure exactly
how the controls work with them. Command line works, so go with that!
"""



import sys
import wave
import subprocess
import datetime
import pathlib
import re
import operator
import time

import numpy



__VERSION__ = "0.0.0"

DATE_TIME = datetime.datetime.now()
LOG_FILE = "play_rec_log_{0}{1:04X}.txt".format(DATE_TIME.strftime("%Y%m%d%H%M%S"), 0)


"""
Capture the linux kernel version
"""
X = subprocess.run(['uname', '-or'], capture_output=True)
LINUX_KERNEL_VERSION = X.stdout.decode('ascii').rstrip()



"""
Capture Python versions
"""
PYTHON_VERSION = sys.version
NUMPY_VERSION = numpy.__version__


"""
Capture ALSA version
"""
X = subprocess.run(['cat', '/proc/asound/version'], capture_output=True)
ALSA_VERSION = X.stdout.decode('ascii').rstrip()



"""
Capture the snd_emu10k1 module version.
For more distinguishing fields can look at "modinfo snd_emu10k1", but
there's not much more there.
"""
X = subprocess.run(['cat', '/sys/module/snd_emu10k1/srcversion'], capture_output=True)
SND_MODULE_VERSION = X.stdout.decode('ascii').rstrip()




"""
Find the card in the /sys/class/sound folder
"""
CARD_ID = None
for SND in pathlib.Path("/sys", "class", "sound").glob("card?"):   # Does this limit us to 10 cards??
	
	#print(SND)
	#print(SND.joinpath("id").read_text())
	
	ID = SND.joinpath("id").read_text().rstrip()
	if ID == "Live":
		# Found it!
		CARD_ID = SND.name
		CARD_NUMBER = SND.joinpath("number").read_text().rstrip()
		DEVICE_REVISION = SND.joinpath("device", "revision").read_text().rstrip()
		DEVICE_DEVICE = SND.joinpath("device", "device").read_text().rstrip()
		DEVICE_VENDOR = SND.joinpath("device", "vendor").read_text().rstrip()
		DEVICE_SUBSYSTEM_DEVICE = SND.joinpath("device", "subsystem_device").read_text().rstrip()
		DEVICE_SUBSYSTEM_VENDOR = SND.joinpath("device", "subsystem_vendor").read_text().rstrip()
		break
	
	
		
"""
Confirm it on the /proc side
"""
if pathlib.Path("/proc", "asound", CARD_ID, "id").read_text().rstrip() != "Live":
	raise Exception("Error! Haven't managed to find the card")



"""
Find the card on the PCI bus
"""
X = subprocess.run(['lspci', '-d', '1102:0002', '-v'], capture_output=True) # verbose & specifying device/vendor
PCI_INFO = X.stdout.decode('ascii').rstrip()




"""
Output the information that we've gleaned so far
"""
with open(pathlib.Path("Logs", LOG_FILE), "w") as f_log:
	f_log.write(f"Result of running script {__file__} version {__VERSION__}\nDate/time: {DATE_TIME.isoformat()}\n\n")
	f_log.write(f"Linux kernel version:\n{LINUX_KERNEL_VERSION}\n\n")
	f_log.write(f"Python version:\n{PYTHON_VERSION}\nNumpy version:\n{NUMPY_VERSION}\n\n")
	f_log.write(f"ALSA library version:\n{ALSA_VERSION}\n\n")
	f_log.write(f"EMU10K1 module source version:\n{SND_MODULE_VERSION}\n\n")
	f_log.write(f"Card number: {CARD_NUMBER}\nCard name: {CARD_ID}\nCard revision: {DEVICE_REVISION}\n")
	f_log.write(f"Vendor/device: {DEVICE_VENDOR} {DEVICE_DEVICE}\n")
	f_log.write(f"Subsystem vendor/subsystem device: {DEVICE_SUBSYSTEM_VENDOR} {DEVICE_SUBSYSTEM_DEVICE}\n")
	f_log.write(f"\n\nPCI info:\n{PCI_INFO}\n\n")



"""
Parse the mixer contents
"""
AMIXER_CONTENTS = []

X = subprocess.run(['amixer', '-c', str(int(CARD_NUMBER)), '-i', 'contents'], capture_output=True)
LINES = X.stdout.decode('ascii').split('\n')
CURRENT_CTL = None
for LINE in LINES:
	pass
	
	# First try to match the head line for each control
	m = re.match("numid=(\d+),iface=([A-Z]+),name='(.*)'", LINE)
	if m is not None:
		CURRENT_CTL = {'id': int(m.group(1)), 'name': m.group(3)}
	else:
		# Otherwise try to match the one that says how many values there are
		m = re.match(".*type=([A-Z]+).*values=(\d+)", LINE)
		if m is not None:
			if CURRENT_CTL is not None:
				CURRENT_CTL.update({'value_count': int(m.group(2))})
		else:
			# Finally, try to match the list of values
			m = re.match(".*values=(.*)", LINE)
			if m is not None:
				VALS = m.group(1).split(",")
				if CURRENT_CTL is not None:
					CURRENT_CTL.update({'value_count_2': len(VALS)})

	if CURRENT_CTL is not None:
		if 'id' in CURRENT_CTL and 'name' in CURRENT_CTL and 'value_count' in CURRENT_CTL and 'value_count_2' in CURRENT_CTL:
			if CURRENT_CTL['value_count'] != CURRENT_CTL['value_count_2']:
				print(CURRENT_CTL)
				raise Exception("Mismatch of amixer values!")
			AMIXER_CONTENTS.append( (CURRENT_CTL['id'], CURRENT_CTL['name'], CURRENT_CTL['value_count']) )
			CURRENT_CTL = None

AMIXER_CONTENTS.sort(key=operator.itemgetter(0))
print(AMIXER_CONTENTS)

"""
Parse the Mixer controls
"""
AMIXER_CONTROLS = []
X = subprocess.run(['amixer', '-c', str(int(CARD_NUMBER)), '-i', 'controls'], capture_output=True)
LINES = X.stdout.decode('ascii').split('\n')
for LINE in LINES:
	m = re.match("numid=(\d+),iface=([A-Z]+),name='(.*)'.*", LINE)
	if m is not None:
		AMIXER_CONTROLS.append( (int(m.group(1)), m.group(3), -1)  )

AMIXER_CONTROLS.sort(key=operator.itemgetter(0))


"""
Check that the results are the same
"""
if len(AMIXER_CONTENTS) != len(AMIXER_CONTROLS):
	raise Exception
for I in range(len(AMIXER_CONTROLS)):
	if AMIXER_CONTROLS[I][0] != AMIXER_CONTENTS[I][0]:
		raise Exception
	if AMIXER_CONTROLS[I][1] != AMIXER_CONTENTS[I][1]:
		raise Exception





"""
List of controls that need to be set. For now, require that both number and
name both match. I suspect that numbering may change arbitrarily so consider
that for future.
"""

CONTROLS = [
# Set up capture
(43, 'Master Playback Switch', 'on'),
(44, 'Master Playback Volume', 16),
(62, 'PCM Playback Switch', 'on'),
(63, 'PCM Playback Volume', 35),
(1,  'Wave Playback Volume', 73),
(51, 'Mic Playback Switch','off'),
(64, 'Capture Source', 5),
(65, 'Capture Switch', 'on'),
(66,'Capture Volume', 3),
#(60,'Aux Playback Switch', 'on'),
# These two values are apparently required
(19,'AC97 Capture Volume',100),
(18,'AC97 Playback Volume',0)
]


for C in CONTROLS:
	Q = [QQ for QQ in AMIXER_CONTROLS if QQ[0]==C[0] and QQ[1]==C[1]]
	if len(Q) != 1:
		raise Exception
	Q = [QQ for QQ in AMIXER_CONTENTS if QQ[0]==C[0] and QQ[1]==C[1]]
	if len(Q) != 1:
		raise Exception
		
	S = ""
	
	
	if type(C[2]) == str:
		S = "{0}".format(C[2])
	else:
		# assume integer
		S = str(C[2])
    
	# do repetition
	S = ",".join(   [S]*Q[0][2]   )
	print(S)

	X = subprocess.run(['amixer', '-c', str(int(CARD_NUMBER)), 'cset', 'numid={0}'.format(C[0]), S], capture_output=True)
	print(X.stdout)
	print(X.stderr)




"""
Create a WAV file with a suitable pattern - triangle wave at 1kHz.
Triangle has more harmonic interest than a sine wave, but shows clipping
unlike a square or pulse wave.
"""

with wave.open("1.wav", "wb") as f:
	FRAME_COUNT = 48000
	CHANNEL_COUNT = 16
	FREQ = 1000.
	AMPL = 32767.
	f.setnchannels(CHANNEL_COUNT)
	f.setsampwidth(2) # S16_LE format
	f.setframerate(48000)
	
	
	M = numpy.zeros([FRAME_COUNT, CHANNEL_COUNT], dtype=numpy.int16)
	
	# Triangle wave is absolute value of sawtooth
	T = numpy.linspace(0., float(FRAME_COUNT)/48000., num=FRAME_COUNT)
	R = numpy.fabs(((T * (4*AMPL*FREQ)) % (4*AMPL)) - (2*AMPL)) - AMPL
	
	M[:, 0] = R.astype(numpy.int16)  # 0 = left, 1 = right
	
	f.writeframes(M.view())


P1 = subprocess.Popen(['arecord', '-D', 'plughw:CARD=Live,DEV=2', '-r', '48000', '-f', 'S16_LE', '-c', '16', '-d', '2', '2.wav'], stdout=subprocess.PIPE)

time.sleep(0.25)

P2 = subprocess.Popen(['aplay', '-D', 'plughw:CARD=Live,DEV=3', '-v', '-M', '1.wav'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# The above plays a 16-channel WAV file into the 16-channel Multi-channel
# playback. For some reason "plughw" is required rather than "hw" -- I'm
# not sure why. Try using the "-v" option to investigate a bit more.

#  UPDATE: the answer is to use "-M" option.


(P2_out, P2_err) = P2.communicate()
P1.wait()


print(P1.stdout.read())
print(P2_out)
print(P2_err)
print(P1.returncode)
print(P2.returncode)

N = None

with wave.open("2.wav", "rb") as f2:
	if f2.getsampwidth() != 2:
		raise Exception("Recorded WAV is not S16_LE!")
	
	N = numpy.ndarray([f2.getnframes(), f2.getnchannels()], dtype=numpy.int16, buffer=f2.readframes(f2.getnframes()))
	print(N.shape)
	print(N[:, 0:100])

VOLS = N.max(0)-N.min(0)
print(VOLS)

"""
Output the final result to the log file
"""
with open(pathlib.Path("Logs", LOG_FILE), "a") as f_log:
	f_log.write("Signals on recorded channels:\n{0}\n\n".format( str(VOLS)  ))
