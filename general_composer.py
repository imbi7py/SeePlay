# UTILITIES

roots = {
   "C" : 0,
   "C#" : 1,
   "D" : 2,
   "Eb" : 3,
   "E" : 4,
   "F" : 5,
   "F#" : 6,
   "G" : 7,
   "Ab" : 8,
   "A" : 9,
   "Bb" : 10,
   "B" : 11
}

lengths = {
    "se" : 0.25,
    "qu" : 0.5,
    "cr" : 1,
    "mi" : 2,
    "S1" : 4,
    "S2" : 8,
    "S3" : 12,
    "S4" : 16,
    "S6" : 24,
    "S8" : 32
}

def midi_to_genletter(note):
    revroots = dict((v,k) for k,v in roots.iteritems())
    return revroots[note % 12]

def midi_to_chord(scale, mode, octave):
    newscale = []
    revroots = dict((v,k) for k,v in roots.iteritems())

    for i in xrange(len(scale)):
        newscale.append(revroots[scale[i] % 12] + str(octave) + mode[i])

    return newscale

def midi_to_letter(scale, octave):
    newscale = []
    revroots = dict((v,k) for k,v in roots.iteritems())

    for note in scale:
        newscale.append(revroots[note % 12] + str(octave))

    return newscale

def make_chordscale(key, mode, octave):
    root = roots[key]
    majscale = [root, root+2, root+4, root+5, root+7, root+9, root+11, root+12]
    minscale = [root, root+2, root+3, root+5, root+7, root+8, root+10, root+12]

    majmode = ["+","-","-","-","+","+","-","-"]
    minmode = ["-","-","+","-","-","+","+","-"]

    if mode == "+":
        return midi_to_chord(majscale, majmode, octave)
    else:
        return midi_to_chord(minscale, minmode, octave)

def make_scale(key, mode, octave):
    root = roots[key]
    majscale = [root, root+2, root+4, root+5, root+7, root+9, root+11, root+12]
    minscale = [root, root+2, root+3, root+5, root+7, root+8, root+10, root+12]

    if mode == "+":
        return midi_to_letter(majscale, octave)
    else:
        return midi_to_letter(minscale, octave)

def make_chord(key, mode, octave):
    chordname = key + str(octave) + mode
    return chordname

def get_chord(chord):
    if len(chord) == 6:
        pitch = chord[:2]
    else:
        pitch = chord[:1]

    octave = int(chord[-4:-3]) * 12
    mode = str(chord[-3:-2])

    pitch = roots[pitch] + 24
    minoroffset = 3 if mode == "-" else 4
    chord = [pitch+octave, pitch+minoroffset+octave, pitch+7+octave, pitch+12+octave, pitch+12+minoroffset+octave, pitch+19+octave, pitch+24+octave]
    return chord
