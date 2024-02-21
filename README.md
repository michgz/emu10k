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

Investigating the association between EMU10K1 External Outs and AC'97 input slots has shown up the following. This was found on a CT4760 soundcard which has a STAC9721 chip:

| AC'97 slot  ( name )  |   MC1,MC0    |   Channel  |   EMU10K1 EXTOUT   (name if known)   |   Required AC97SLOT register mask    |  Notes             |
|-----------------------|--------------|------------|--------------------------------------|--------------------------------------|--------------------|
|   3    ( PCM LEFT )   |     0,0      |     Left   |    0 (EXTOUT_AC97_L)                 |       none (00000000h)               |                     |
|   4    ( PCM RIGHT )  |     0,0      |     Right  |    1 (EXTOUT_AC97_R)                 |       none (00000000h)               |                     |
|   6    ( PCM CTR)     |     1,0      |     Left   |    13 (EXTOUT_AC97_REAR_L)            |           00000003h                  | AC97SLOT=0x01 is not sufficient for this channel. Note mismatch between STAC7921 & EMU10k1 naming  |
|   9    (PCM LFE )     |     1,0      |     Right  |    14 (EXTOUT_AC97_REAR_R)            |           00000002h                  | Note mismatch between STAC7921 & EMU10k1 naming                    |
|   7    ( PCM LSURR)     |     0,1      |     Left   |    17 (EXTOUT_ACENTER)            |           00000030h                  | Note mismatch between STAC7921 & EMU10k1 naming |
|   8    (PCM RSURR )     |     0,1      |     Right* |    18 (EXTOUT_ALFE)            |           00000030h                  | Note mismatch between STAC7921 & EMU10k1 naming. This channel has significant stereo leakage    |
|   10    (PCM LALT )     |     1,1      |     Left* |    15                       |           0000000Ch                  |  This channel uses a EXTOUT that is not documented in EMU10K1 header files. This channel has significant stereo leakage    |
|   11    (PCM RALT )     |     1,1      |     Right |    16                       |           0000000Ch                  |   This channel uses a EXTOUT that is not documented in EMU10K1 header files   |

The outcome had some unexpected findings. Firstly, the EXTOUT naming which is known from header files used in the ALSA and Linux projects (which seem to have originated from inside Creative Inc.) doesn't at all match the naming of AC'97 slots.
Further, two EXTOUTs (15 and 16) are not documented as existing at all and yet they are associated with slots.

More concerning, the 8 and 10 slots have very significant stereo leakage. The volume of the leakage sound is controlled by both Left & Right attenuation settings of the PCM Out Volume register -- as if the signal is passing through the correct attenuator, and after that
incorrectly being fed back to the input of the opposite attenuator. With an attenuator setting of 10 or less, the volume of sound in the "other" channel is actually higher than the volume in the correct channel!

The stereo leakage issue feels mostly likely to be a fault in the STAC9721 chip design. It is not a problem for these soundcards, since even the 5.1 cards use a maximum of four channels through the AC'97 device -- and slots 3, 4, 6 and 9 are perfectly well behaved.
I'm looking forward to redo this experiment on a soundcard with a STAC9708 chip to see if anything is different.
