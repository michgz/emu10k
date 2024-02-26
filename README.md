# emu10k
Experimentations with the EMU10K1 soundcards which were produced by Creative Labs in the late '90s/early 2000's.

There's quite extensive support for these cards in current Linux/ALSA, which I'm exploring. My main goal is to use the effects processing on the cards in a "Send-Return" manner, i.e. to use the cards as a multi-channel hardware accelerator for DSP effects processing.

---

As at Feb'24: "main.c" overwrites the usual ACODE in the EMU10k1 with a much simpler set that just copies inputs to outputs, e.g. Input 0 -> Output 0, Input 1 -> Output 1 etc. "play_rec.py" then plays a 16-channel sound into 4 out of the inputs and records the 16-channel output. The following command sequence can be used:

```
; Restore default settings, including the usual ACODE
sudo alsactl restore

; Build "main.c"
make all

; Run "main.c": overwrites the ACODE with our simpler set
sudo ./a.out

; Try a simultaneous record/playback
python play_rec.py
```

This sort of works: as expected, 4 of the recorded channels contain sound but it's not consistently the same channels every time. I need to work out why not.


## AC'97 slot investigation

Investigating the association between EMU10K1 External Outs and AC'97 input slots has shown up the following, with the investigation running on a CT4760 soundcard which has a STAC9721 chip
and a SB0060 card which has a STAC9708 chip. The experiment was done using microcode to forward signals from the ADC playback device to various EXTOUTs on the EMU10K1 and finding
which settings on the AC'97 chip resulted in sound being produced.


| AC'97 slot  (name)    |   Channel  |   EXTOUT number  (name if known)   |   Required AC97SLOT mask value       |
|-----------------------|------------|------------------------------------|--------------------------------------|
|   3    ( PCM LEFT )   |   Left     |    0  ( EXTOUT_AC97_L )            |       none (00000000h)               |
|   4    ( PCM RIGHT )  |   Right    |    1  ( EXTOUT_AC97_R )            |       none (00000000h)               |
|   6    ( PCM CTR)     |   Left     |    13 ( EXTOUT_AC97_REAR_L )       |           00000001h                  |
|   9    ( PCM LFE )    |   Right    |    14 ( EXTOUT_AC97_REAR_R )       |           00000002h                  |
|   7    ( PCM LSURR)   |   Left     |    17 ( EXTOUT_ACENTER )           |           00000010h                  |
|   8    ( PCM RSURR )  |   Right    |    18 ( EXTOUT_ALFE )              |           00000020h                  |
|   10   ( PCM LALT )   |   Left     |    15                              |           00000004h                  |
|   11   ( PCM RALT )   |   Right    |    16                              |           00000008h                  |


It's clear that the EXTOUT naming scheme is not following the AC'97 naming in any way. Also, the following table of slot allocations is taken from the STAC9708 specification:

![multi_channel_reg](https://github.com/michgz/emu10k/multi_channel_reg.png)

Compare this against the connection of AC'97 outputs to external connectors on the SB0060 soundcard:

|  PCM Output     |   STAC9708 Pin    |   Connector   |
|-----------------|-------------------|---------------|
|  PCM OUT LEFT   |   LINE-OUT-L      |   Front L     |
|  PCM OUT RIGHT  |   LINE-OUT-R      |   Front R     |
|  PCM2 LEFT      |   DAC_OUT_L       |   Centre      |
|  PCM2 RIGHT     |   DAC_OUT_R       |   LFE         |

(Note: Rear channels come from the Philips DAC, not from the AC'97, so they do not appear here). 

Putting all this together, if MC1,MC0=0,0 then the EXTOUT naming is correct for the signals' functions, even though the AC'97 names are wrong.
This is the default setting for MC1,MC0 and the one used by the ALSA driver.


## Automatic routing

In the investigation above, I noticed that the EMU10K1 by default routes signals from the 32 "input" registers to the
32 "output" registers. The routing happens without even any microcode loaded and as far as I know it doesn't depend on being
configured. In the list below, signals are routed from the register on the left to the register on the right:


```
FXBUS(0)  -> EXTOUT(0)
FXBUS(1)  -> EXTOUT(1)
FXBUS(2)  -> EXTOUT(2)
FXBUS(3)  -> EXTOUT(3)
FXBUS(4)  -> EXTOUT(4)
FXBUS(5)  -> EXTOUT(5)
FXBUS(6)  -> EXTOUT(6)
FXBUS(7)  -> EXTOUT(7)
FXBUS(8)  -> EXTOUT(8)
FXBUS(9)  -> EXTOUT(9)
FXBUS(10) -> EXTOUT(10)
FXBUS(11) -> EXTOUT(11)
FXBUS(12) -> EXTOUT(12)
FXBUS(13) -> EXTOUT(13)
FXBUS(14) -> EXTOUT(14)
FXBUS(15) -> EXTOUT(15)
EXTIN(0)  -> FXBUS2(0)   -- a.k.a. EXTOUT(16)
EXTIN(1)  -> FXBUS2(1)   -- a.k.a. EXTOUT(17)
EXTIN(2)  -> FXBUS2(2)   -- a.k.a. EXTOUT(18)
EXTIN(3)  -> FXBUS2(3)
EXTIN(4)  -> FXBUS2(4)
EXTIN(5)  -> FXBUS2(5)
EXTIN(6)  -> FXBUS2(6)
EXTIN(7)  -> FXBUS2(7)
EXTIN(8)  -> FXBUS2(8)
EXTIN(9)  -> FXBUS2(9)
EXTIN(10) -> FXBUS2(10)
EXTIN(11) -> FXBUS2(11)
EXTIN(12) -> FXBUS2(12)
EXTIN(13) -> FXBUS2(13)
EXTIN(14) -> FXBUS2(14)
EXTIN(15) -> FXBUS2(15)
```


This makes sense - in a simple application where loading of microcode is not required, there needs to be some way to
get playback channels to physical outputs, and similarly physical inputs to record channels. A problem
arises though with certain AC'97 setups, because EXTIN(0) and EXTIN(1) are inputs from the AC'97, while EXTOUT(16) and
EXTOUT(17) are outputs to slots 11 and 7 of the AC'97. It's possible to set things up so that this automatic routing produces a nasty
feedback loop though the analogue of the AC'97.

Luckily resolving this problem is simple with microcode - simply write EXTOUT(16) and EXTOUT(17) to be the required signal, or
a zero value if silence is required. Any writes from microcode will override the routing.
