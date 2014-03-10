import time
import rtmidi
import threading
import gui
import performer
import conductor
import os
import lily
import recorder
from SimpleCV import *

fps = 1
scale = 0.5
active = False
activity = 0

home = os.path.join(os.path.expanduser('~'))
imgbank = []
imglimit = 5
imgscale = 0.5

def change_activity(val):
    global activity

    if val == "up":
        activity += 1
    elif val == "down":
        activity -= 1
    else: 
        activity = val

    conductor.gen_templates(activity)

def take(parent): 
    intype = parent.user_inputsrc
    os.system("screencapture -xdaro " + home + "/sp_0.tiff")

def get_dominant_colour():
    current = imgbank[0]
    
    if len(imgbank) > 1:
        older = imgbank[1]
    else:
        older = current

    newpeak = current.huePeaks()[0]
    oldpeak = older.huePeaks()[0]
    #print newpeak, oldpeak

    #avgpeak = (newpeak + oldpeak) / 2
    #print avgpeak

def get_motion():
    current = imgbank[0]
    
    if len(imgbank) > 1:
        older = imgbank[1]
    else:
        older = current

    diff = current - older

    matrix = diff.getNumpy()
    mean = matrix.mean()

    return mean

def get_histograms():
    for img in imgbank:
        histo = img.histogram()
        print histo

def add_to_imgbank(img):
    global imgbank
    while len(imgbank) >= imglimit:
        imgbank.pop()
    imgbank.insert(0,img)

def watch(parent):
    if active == True:
        # take(parent)

        # img = Image(home + "/sp_0.tiff").resize(int(parent.screen_x * imgscale), int(parent.screen_y * imgscale))

        # if parent.user_inputsrc == "manual":
        #     [x,y,w,h] = parent.user_inputregion
        #     img = img.crop(x * imgscale, y * imgscale, w * imgscale, h * imgscale)
        
        # add_to_imgbank(img)

        # motion = get_motion()
        # get_dominant_colour()

        # if motion > 10: change_activity(1)

        threading.Timer(performer.tempo_in_time, watch, [parent]).start()

def start_watching(parent):
    midiout = rtmidi.MidiOut(1)
    threading.Timer(0,performer.start,[midiout,parent]).start()

    if parent.user_sheetmusic:
        lily.init()

    if parent.user_midioutput:
        recorder.init()

    conductor.init_values(parent)

    threading.Timer(0,watch,[parent]).start()
    threading.Timer(0,conductor.conduct,[parent]).start()

    time.sleep(1)
    change_activity(0)
    #del midiout

if __name__ == '__main__':
    start_watching()    

