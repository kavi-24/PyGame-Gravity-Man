from pydub import AudioSegment

# Extract a particular time of audio from mp3 file
# song = AudioSegment.from_mp3("./jump.mp3")
# req = song[:1000]
# req.export("./jump2.mp3", format="mp3")

song = AudioSegment.from_ogg("./hit.ogg")
song.export("./hit.mp3", format="mp3")