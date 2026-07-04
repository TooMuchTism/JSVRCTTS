# JSVRCTTS
very simple TTS app for VRC; does exactly what it says it does; uses STDIO so can be used as a simple backend if ever wished (for whatever dumb reason lol, srsly idk why you'd use my code by alr).

# Setup
if wished you can use the IDRK_SETUP inside of the SETUP dir, warning though you'll have to use it every time you restart. Instead you should setup your config yourself. look [here](https://wiki.archlinux.org/title/PulseAudio#Configuration_files) for more info on that.

# Features
I've added some features that I was shocked I didnt see more of in other apps before I made this. Simple word replacment is the biggest feature here. it has three forms.
- gen word replacement (words are replaced both in the chatbox and in the TTS input; eg: 'TMB' --> "trust me bro")
- speech word replacement (words replaced only for speech eg "yk" --> "you know", helps the TTS be less confused)
- blacklisting (words that get replaced by a censor you can set for each word for eg "fuck" --> "\[censored\]")

Another feature is the ability to swap out the TTS command with whatever you want. Internally it runs the command inside of "GEN.CONF", by default it uses `edge-tts` but you are abile to swap this out with whatever TTS you want.

# Dependencys
By default `edge-tts` it should be in your package manager if you need it, a few examples for a few differing platforms are:
arch (btw): `yay -S python-edge-tts` (or whatever AUR handler you use)
debiain: `sudo apt intall pipx && pipx install edge-tts` <-- untested (I dont use that)
windows: `pipx install edge-tts` <-- you'll need to install pipx first though maybe using `winget install pipx`? (idk i dont use windows)
TODO: add more platforms here.
Side note: I really wouldnt recomend running commands from random github repos you find around the place.
Side side note: if you dont want to use `edge tts` just change out the command in "GEN.CONF" for whatever you wish to use.

Also you'll need python3 to run the script, thats it though.

# How to run?
assuming you've setup everything just type in `python3 VRC_TTS.py` and it should start assuming your in the same directory as it in the command line.
## how do I type in VR?
Personally I just type on my keyboard while in VR, but if your standing I guess your cooked? I might make a fix for this in the future if someone asks me to.
## how do I make it show over my VRC
This changes depending on OS and window manager, so I can only tell you for linux+KDE.
On KDE you right click on the window and click `keep above others`, now it will stay on top. On VRC you can click TAB to show your mouse and then click on the window, or use alt+tab to click into it. If your on VR I do not think you'll need to even be focused in the game but that is untested.
## what do I do if it doesnt work?
report it as an issue and I'll try to help you when I see it.


All code here was actually made by me Jenny, so if its bad im just dumb lmao. 
