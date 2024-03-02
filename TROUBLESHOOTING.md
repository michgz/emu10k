#### Scaling on playback is different from record

Samples internally in the EMU10K1 are 32 bit fixed-point, while hardware Playback/Record devices all use 16 bits.

Scaling of Record is very simple - it just uses the top 16 bits (effectively, dividing by 65536).

Scaling of Playback is a bit more complex. At default settings, both Standard and Multichannel playbacks end up about 1/4 th of full scale (that is, -12 dB). It means up to 4 signals can be
sent to the same bus with no chance of overload. There's also no loss of precision -- all 16 bits of precision are still there, it's just not in the topmost 16 bits.

The default setting for volume is 65535 and for "send volume" is 255. The internal bus value is *approximately* equal to:

```
<input value> * <volume> * <send volume> / 1024
```

with the bottom 8 bits being set to zero (only the top 24 bits are kept). With default settings, an input of 0x1000 will become *approximately* 0x03FBFC00 (approximately because there's some small
variation in the lesser bits that I haven't yet identified the cause of). When captured, this value will then become 0x03FC - so, reduced by 12 dB compared to the input.

If only one signal is being sent to each bus (in the code below, bus 0), and you want to approximately match levels between Playback and Record, the following multiply-by-four microcode should do so:

```
OP(icode, &ptr, iMACINT0, ..., C_00000000, FXBUS(0), C_00000004);
```

Scaling of "PT Playback" is even more wierd. It has an exponential character. I still need to work out what's going on with that, with an observation that in the ALSA driver code the following microcode is used for dealing with the left channel:

```
	gpr_map[gpr + 0] = 0xfffff000;
	gpr_map[gpr + 1] = 0xffff0000;
	gpr_map[gpr + 2] = 0x70000000;
	gpr_map[gpr + 3] = 0x00000007;
	/* 0c: */ OP(icode, &ptr, iANDXOR, GPR(tmp + 0), ETRAM_DATA(ipcm->etram[0]), GPR(gpr + 0), C_00000000);
	/* 0d: */ OP(icode, &ptr, iLOG, GPR(tmp + 0), GPR(tmp + 0), GPR(gpr + 3), C_00000000);
	/* 0e: */ OP(icode, &ptr, iANDXOR, GPR(8), GPR(tmp + 0), GPR(gpr + 1), GPR(gpr + 2));
	/* 0f: */ OP(icode, &ptr, iSKIP, C_00000000, GPR_COND, CC_REG_MINUS, C_00000001);
	/* 10: */ OP(icode, &ptr, iANDXOR, GPR(8), GPR(8), GPR(gpr + 1), GPR(gpr + 2));
```

and something similar for the right channel. Note in there that a logarithm of the data is being taken!

#### Two channels of Multichannel Playback produce no sound

Channels 13 & 14 end up silent. The reason seems to be an incorrect setup in the driver's default send routing:

```
~$ amixer -D hw:CARD=Live cget iface=PCM,name='Multichannel PCM Send Routing',device=3,index=13
numid=190,iface=PCM,name='Multichannel PCM Send Routing',index=13,device=3
  ; type=INTEGER,access=rwi-----,values=4,min=0,max=15,step=0
  : values=13,0,13,14
~$ amixer -D hw:CARD=Live cget iface=PCM,name='Multichannel PCM Send Routing',device=3,index=14
numid=191,iface=PCM,name='Multichannel PCM Send Routing',index=14,device=3
  ; type=INTEGER,access=rwi-----,values=4,min=0,max=15,step=0
  : values=14,0,13,14
```

All four routing values must be different from each other, so these two are illegal. The EMU10K1 seems to respond by just not sending *any* signals to those two buses.

The following commands sort this out:

```
~$ amixer -D hw:CARD=Live cset iface=PCM,name='Multichannel PCM Send Routing',device=3,index=13 13,0,11,12
~$ amixer -D hw:CARD=Live cset iface=PCM,name='Multichannel PCM Send Routing',device=3,index=14 14,0,11,12
```

#### Multichannel Capture has inconsistent ordering

```
~$ amixer -D hw:CARD=Live cget iface=PCM,name='Captured FX8010 Outputs',device=2
numid=42,iface=PCM,name='Captured FX8010 Outputs',device=2
  ; type=BOOLEAN,access=rw------,values=32
  : values=off,off,off,off,off,off,off,off,off,off,off,off,off,off,off,off,on,on,on,on,on,on,on,on,on,on,on,on,on,on,on,on
```

The setting above is the default, and it specifies 16 output channels to be captured: they are FXBUS(0) - FXBUS(15). With this setup, the captured channels have a
wierd ordering. Most commonly it is:

FXBUS2(14),FXBUS2(15),FXBUS2(0),FXBUS2(1),FXBUS2(2),FXBUS2(3),FXBUS2(4),FXBUS2(5),FXBUS2(6),FXBUS2(7),FXBUS2(8),FXBUS2(9),FXBUS2(10),FXBUS2(11),FXBUS2(12),FXBUS2(13)

but sometimes (seemingly randomly?) they are rotated round in a completely different way. There seems to be no consistent way to identify which channel is from which output.

I haven't found a solution to this, but have noticed it only happens when 16 or 32 channels are being captured. With 1, 2, 4 or 8 channel captured the Multichannel Capture works fine.
