For experimenting with older Creative software, we need some way of emulating. I
chose to use a Windows 95 installation. Two emulation tools were used in collaboration
with each other:

 * 86Box: for creating a Windows 95 image with Creative drivers installed. QEMU
          didn't do this successfully, probably due to known issues with emulating
          this age of machine.
          
 * QEMU:  for doing PCI pass-through. 86Box doesn't have that capability.
 
Attached a configuration file for 86Box version 4.2.1, suitable for running an
emulated Windows 95 with CD-ROM drive. Additionally two CD-ROM images are
required:

 * Windows 95 Installer
 
 * Creative SoundBlaster Live! Installation disk