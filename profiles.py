import watchman
import performer
import mixer
import stabs
import threading

# Standard profile (motion drives tempo)
def standard_a(parent, img):
    brightness = watchman.get_brightness(img.histogram(250), 20)
    [red_brightness, green_brightness, blue_brightness] = watchman.count_colours(img)
    motion = watchman.get_motion()

    # if performer.bar % 4 == 0:
        # facecount = watchman.get_facecount(img)

    if motion > 10: 
        watchman.activity_boost = 1
        stabs.multifire(motion)
        
        tempomod = max(min(2, 1 + (motion / 100)), 1)
        parent.set_user_tempo_modifier(tempomod)
    else:
        watchman.activity_boost = 0
        parent.set_user_tempo_modifier(1)

    watchman.change_activity("bass", red_brightness)
    watchman.change_activity("drums", green_brightness)
    watchman.change_activity("melody", red_brightness)
    watchman.change_activity("chords", green_brightness)

    if blue_brightness > 0.5: 
        if parent.user_mode == "+": parent.set_user_mode("Minor")
    else:
        if parent.user_mode == "-": parent.set_user_mode("Major")

    mixer.set_volume(parent, "bass", 80 * (1 - brightness))
    mixer.set_volume(parent, "drums", 80 * (1 - brightness))
    mixer.set_volume(parent, "chords", 127 * brightness)
    mixer.set_volume(parent, "melody", 127 * brightness)
    mixer.set_volume(parent, "stabs", 127 * brightness)

# Alternate profile (motion drives volume)
def standard_b(parent, img):
    brightness = watchman.get_brightness(img.histogram(250), 20)
    [red_brightness, green_brightness, blue_brightness] = watchman.count_colours(img)
    motion = watchman.get_motion()

    # if performer.bar % 4 == 0:
        # facecount = watchman.get_facecount(img)

    motion_threshold = 10

    if motion > motion_threshold:  
        watchman.activity_boost = 1
        stabs.multifire(motion)
    else:
        watchman.activity_boost = 0
        
    mixer.set_volume(parent, "bass", 127 * watchman.invlerp(motion_threshold, 200, motion))
    mixer.set_volume(parent, "drums", 127 * watchman.invlerp(motion_threshold, 200, motion))
    mixer.set_volume(parent, "chords", 127 * watchman.invlerp(motion_threshold, 200, motion))
    mixer.set_volume(parent, "melody", 127 * watchman.invlerp(motion_threshold, 200, motion))
    mixer.set_volume(parent, "stabs", 127 * watchman.invlerp(motion_threshold, 200, motion))

    parent.set_user_tempo_modifier(0.5 + brightness)

    watchman.change_activity("bass", red_brightness)
    watchman.change_activity("drums", green_brightness)
    watchman.change_activity("melody", red_brightness)
    watchman.change_activity("chords", blue_brightness)

    if blue_brightness > 0.5: 
        if parent.user_mode == "+": parent.set_user_mode("Minor")
    else:
        if parent.user_mode == "-": parent.set_user_mode("Major")

    
