# -*- coding: utf-8 -*-
import appuifw
import audio

#        Input text
#text = appuifw.query(u"Type a word:", "text")

#        Show popup
#i=appuifw.InfoPopup()
#i.show(u"Here is the tip.", (0, 0), 5000, 0, appuifw.EHRightVCenter)


def read_text(txt):
    '''Reads a text'''
    import audio
    audio.say(txt)

