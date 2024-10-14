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

 * Creative SoundBlaster Live! Installation CD
 * Microsoft Windows 95 installation CD
 * Windows 95 boot floppy
 * CD-ROM drivers. I managed to find a set online called CD1.SYS, CD2.SYS, CD3.SYS, CD4.SYS and found that CD4.SYS worked well for both 86box and QEMU (although I didn't try them all -- maybe others would also work).

The CD-ROM hardware must be enabled by creating two files with the following content:

C:\CONFIG.SYS:
```
DEVICE=C:\CD4.SYS /D:MSCD001
```

C:\AUTOEXEC.BAT:
```
C:\WINDOWS\COMMAND\MSCDEX.EXE /D:MSCD001 /L:D
```
