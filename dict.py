# -*- coding: utf-8 -*-
# RSS-agk
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
import btsocket
import sys
import e32db


def wget(url,ap_id=None):

    #Download the file
    sock = btsocket.socket(btsocket.AF_INET,btsocket.SOCK_STREAM)

    sock.connect((host,port))
    sock.send("GET %s HTTP/1.1\r\nConnection: close\r\nHost: %s\r\nUser-Agent: RSS-agk\r\n\r\n" % (get,hname))
    
    data=''
    while True:
        r=sock.read(4000)
        if len(r)==0:
            break
        data+=r
    
    sock.close()

    #TODO Server didn't return ok
    if data[9:12]!='200':
        appuifw.note(u'Server returned %s instead of 200' % data[9:12], "info")
        return None
    
    return data.split('\r\n\r\n',1)[1]




def do_nothing():
    '''This function does nothing'''
    pass

def exit_key_handler():
    '''Exits the application'''
    app_lock.signal()
    
def back_one_level():
    exit_key_handler()

def init_menu():
    appuifw.app.menu = [
        (u"Update all feeds", update_all_feeds),
        (u"View in browser", open_in_browser),
        
        (u"Manage feeds",(
        
            (u"Update feed", update_feed),
            (u"Add feed", add_feed),
            (u"Remove feed", remove_feed),
            (u"Mark feed as read", mark_feed_read),
            (u"Mark all feeds as read", mark_all_feeds_read),
            (u"Import feeds", do_nothing),
            (u"Export feeds", do_nothing),
        
        )),
        
        (u"Settings",show_settings),
        
        (u"About", about),
        (u"Exit", exit_key_handler)
    ]

def about():
    appuifw.note(u"RSS-agk by Salvo 'LtWorf' Tomaselli", "info")

def show_settings():
    ap_list=[u'---None---']
    for i in btsocket.access_points():
        ap_list.append(i['name'])
        
    try:
        ap_default=ap_list.index(settings['default_ap'])
    except:
        ap_default=0
    
    
    form=appuifw.Form(
        [
            (u'Show read Articles','combo', ([u'No', u'Yes'],int(settings['show_read']))),
            (u'Default access point','combo', (ap_list,ap_default)),
            (u'Update feeds on open','combo', ([u'No', u'Yes'],int(settings['update_on_open']))),
            (u'Items to store per feed','number',settings['items_per_feed']),
            (u'Max chars per line','number',settings['chars_per_line']),
            #(u'txt','text', u'default'),
            #(u'number','number', 123),
            #(u'date','date'),
            #(u'time','time'),
        ],
    appuifw.FFormDoubleSpaced | appuifw.FFormEditModeOnly)
    
    form.execute()
    
    settings['show_read']=bool(form[0][2][1])
    settings['default_ap']=ap_list[form[1][2][1]]
    settings['update_on_open']=bool(form[2][2][1])
    settings['items_per_feed']=int(form[3][2])
    settings['chars_per_line']=int(form[4][2])

#################################################### The order of those lines is IMPORTANT

app=appuifw.app
app.title=u"Dict"
app.screen='normal'

#associate_ap()

# Sets the list as body of the app
appuifw.app.body = main_list

init_menu()

appuifw.app.exit_key_handler = back_one_level

# create an Active Object
app_lock = e32.Ao_lock()
app_lock.wait()
