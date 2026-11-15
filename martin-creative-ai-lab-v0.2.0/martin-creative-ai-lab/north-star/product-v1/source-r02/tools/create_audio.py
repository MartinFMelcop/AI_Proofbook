"""Original, purely procedural cinematic *animatic placeholder*; no copyrighted stems."""
import math, wave
import numpy as np
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'artifacts'/'opening_original_score.wav'
sr=22050;dur=18.0;n=int(sr*dur)
y=np.zeros(n,dtype=np.float64)
chords=[(52,55,59,64),(48,52,55,60),(55,59,62,67),(50,54,57,62)]
def freq(midi):return 440.0*2**((midi-69)/12)
for c in range(8):
 start=c*2.25;notes=chords[c%4]
 # Warm low-string pad and plucked high-register fragments
 for ni,midi in enumerate(notes):
  t0=int(start*sr);t1=min(n,int((start+2.6)*sr));t=np.arange(t1-t0)/sr
  a=0.13*(1-np.exp(-t*5))*np.exp(-t*.45)
  wavepad=np.sin(2*np.pi*freq(midi)*t)+.25*np.sin(2*np.pi*freq(midi)*2*t+.2)+.12*np.sin(2*np.pi*freq(midi)*3*t)
  y[t0:t1]+=a*wavepad
 for beat in range(4):
  j=int((start+beat*0.5625)*sr)
  if j>=n:continue
  size=min(int(.55*sr),n-j);t=np.arange(size)/sr
  pitch=freq(notes[(beat+c)%4]+12)
  y[j:j+size]+=.17*np.exp(-t*7)*(np.sin(2*np.pi*pitch*t)+.22*np.sin(2*np.pi*2*pitch*t))
 # subdued bass pulse
 for beat in range(4):
  j=int((start+beat*0.5625)*sr);size=min(int(.23*sr),n-j)
  if size>0:
   t=np.arange(size)/sr
   y[j:j+size]+=.15*np.exp(-t*13)*np.sin(2*np.pi*freq(notes[0]-24)*t)
# envelope, delay ambience and gentle limiter
wet=y.copy();delay=int(.24*sr);wet[delay:]+=.18*y[:-delay]
envelope=np.minimum(1,np.arange(n)/(sr*.8))*np.minimum(1,(n-np.arange(n))/(sr*1.8));wet*=envelope
wet=np.tanh(wet*1.45)*.52
pcm=(np.clip(wet,-.99,.99)*32767).astype('<i2')
with wave.open(str(p),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(pcm.tobytes())
print(str(p),len(pcm))
