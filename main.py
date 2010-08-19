# -*- coding: utf-8 -*-
# Relational
# Copyright (C) 2010  Salvo "LtWorf" Tomaselli
# 
# Relational is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

import appuifw
import e32

class feed:
    def __init__(self,url):
        self.title=url #TODO TEMPORARY

    def update_feed(self):
        pass
    def get_unread(self):
        return 1
    def get_title(self):
        return self.title
    def get_articles(self):
        return [u'art',u'bart',self.title]
    def __str__(self):
        return u"%s (%d)" %(self.get_title(),self.get_unread())

class global_vars:
    def __init__(self):
        self.current_feed=0
        self.view_state=0 #0 is list of feeds, 1 is list of news and 2 is text of the new

feeds=[]
feeds.append(feed(u'ciao'))
gvars=global_vars()

def do_nothing():
    '''This function does nothing'''
    pass

def show_popup(text):
    appuifw.note(text, "info")

def exit_key_handler():
    app_lock.signal()
    
def back_one_level():
    if gvars.view_state==0:
        exit_key_handler()
    gvars.view_state-=1
    update_view()

# define a callback function
def list_click():
    if gvars.view_state==0 and len(feeds)>0: 
        gvars.current_feed = main_list.current()
        gvars.view_state=1
        update_view()
    elif gvars.view_state==0 and len(feeds)==0:
        add_feed()
#    elif gvars.view_state==1:
#        pass
#    elif gvars.view_state==2:
#        pass

def get_feeds_entries():
    result=[]
    for i in feeds:
        result.append(i.__str__())
    if len(result)>0:
        return result
    else:
        gvars.current_feed=-1
        return [u'Add a feed first...']

def add_feed():
    uri=appuifw.query(u"Insert feed's URL:", "text")
    
    if uri==None:
        return
        
    try:
        new_feed=feed(uri)
        feeds.append(new_feed)
        update_view()
    except:
        show_popup(u'Unable to insert the feed')
        
def remove_feed():
    if gvars.view_state==0:
        index = main_list.current()
    else:
        index= gvars.current_feed
        gvars.view_state=0
    
    try:
        feeds.pop(index)
        update_view()
    except:
        show_popup(u'Unable to remove the feed')

def update_view():
    '''Updates the current view, depending on the current view state'''
    if gvars.view_state==0:
        main_list.set_list(get_feeds_entries())
    if gvars.view_state==1:
        main_list.set_list(feeds[gvars.current_feed].get_articles())

def init_menu():
    appuifw.app.menu = [
        (u"Options", do_nothing),
        (u"Add feed", add_feed),
        (u"Remove feed", remove_feed),
        (u"Mark feed as read", do_nothing),
        (u"Mark all feeds as read", do_nothing),
        (u"About", about),
        (u"Exit", exit_key_handler),
    ]

def about():
    show_popup(u"RSS-agk by Salvo 'LtWorf' Tomaselli")







app=appuifw.app
app.title=u"RSS-agk"
app.screen='normal'


# create your content list of your listbox including the icons to be used for each entry
main_list = appuifw.Listbox(get_feeds_entries(),list_click)


# create an instance of appuifw.Listbox(), include the content list "entries" and the callback function "shout"
# and set the instance of Listbox now as the application body
appuifw.app.body = main_list

init_menu()

#appuifw.app.menu = [(u"Options", add_feed),(u"Submenu 1",
#((u"Add feed", add_feed),
#(u"Remove feed", add_feed)))]

appuifw.app.exit_key_handler = back_one_level


# create an Active Object
app_lock = e32.Ao_lock()
app_lock.wait()
