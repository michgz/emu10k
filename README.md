# emu10k
Experimentations with the EMU10K1 soundcards which were produced by Creative Labs in the late '90s/early 2000's.

There's quite extensive support for these cards in current Linux/ALSA, which I'm exploring. My main goal is to use the effects processing on the cards in a "Send-Return" manner, i.e. to use the cards as a multi-channel hardware accelerator for DSP effects processing.

---

As at Feb'24: "main.c" overwrites the usual ACODE in the EMU10k1 with a much simpler set that just copies inputs to outputs, e.g. Input 0 -> Output 0, Input 1 -> Output 1 etc. "play_rec.py" then plays a 16-channel sound into 4 out of the inputs and records the 16-channel output. The following command sequence can be used:

; Restore default settings, including the usual ACODE
sudo alsactl restore

; Build "main.c"
make all

; Run "main.c": overwrites the ACODE with our simpler set
sudo ./a.out

; Try a simultaneous record/playback
python play_rec.py


As expected, 4 of the recorded channels contain sound but it's not consistently the same channels every time. I need to work out why not.
