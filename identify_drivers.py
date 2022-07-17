# Tries to find the EMU-related drivers and devices in a Linux system.


import pathlib




# Find all drivers that are something to do with EMU. Normally there are two:
#    snd_emu10k1
#    Emu10k1_gameport
#

EMU_DRIVERS = []

for PP in pathlib.Path("/sys/bus/pci/drivers").iterdir():
  
    if str(PP.name).lower().find("emu10k") >= 0:
        EMU_DRIVERS.append(PP.name)
  


# Now find all devices that use one of the drivers above. Do it by resolving the
# "driver" symbolic link


EMU_DEVICES = []

for PP in pathlib.Path("/sys/bus/pci/devices").iterdir():
    
    if PP.joinpath("driver").resolve().name in EMU_DRIVERS:
        EMU_DEVICES.append(PP.name)


with open("Devices.txt", "w") as f1:
    f1.write("Name     device   vendor   enabled\n\n")
    for N in EMU_DEVICES:
        f1.write("{0}      {1}   {2}   {3}\n".format(
              N,
              pathlib.Path("/sys/bus/pci/devices").joinpath(N, "device").read_text().strip(),
              pathlib.Path("/sys/bus/pci/devices").joinpath(N, "vendor").read_text().strip(),
              pathlib.Path("/sys/bus/pci/devices").joinpath(N, "enable").read_text().strip()
              
        ))
