# -*- coding: utf-8 -*-

import appuifw
def ciao():
    print "ciao"

app=appuifw.app

app.title=u"Suca"
app.screen='full'


appuifw.app.menu = [(u"Item 1", ciao),(u"Submenu 1",
((u"Subitem 1", ciao),
(u"Subitem 2", ciao)))]


appuifw.query(u"Type a word:", "text")

