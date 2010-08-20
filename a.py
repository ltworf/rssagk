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
import socket
import sys

html_escape_repl={'&Ecirc;': u'\xca', '&raquo;': u'\xbb', '&eth;': u'\xf0', '&divide;': u'\xf7', '&atilde;': u'\xe3','&sup1;': u'\xb9', '&THORN;': u'\xde', '&ETH;': u'\xd0', '&frac34;': u'\xbe', '&nbsp;': u',', '&Auml;': u'\xc4', '&Ouml;': u'\xd6', '&Egrave;': u'\xc8', '&acute;': u'\xb4', '&Icirc;': u'\xce', '&deg;': u'\xb0', '&middot;': u'\xb7', '&ocirc;': u'\xf4', '&Ugrave;': u'\xd9', '&gt;': u'>', '&ordf;': u'\xaa', '&uml;': u'\xa8', '&aring;': u'\xe5', '&frac12;': u'\xbd', '&iexcl;': u'\xa1', '&frac14;': u'\xbc', '&Aacute;': u'\xc1', '&szlig;': u'\xdf', '&igrave;': u'\xec', '&aelig;': u'\xe6', '&yen;': u'\xa5', '&times;': u'\xd7', '&para;': u'\xb6', '&oacute;': u'\xf3', '&Igrave;': u'\xcc', '&ucirc;': u'\xfb', '&brvbar;': u'\xa6', '&micro;': u'\xb5', '&agrave;': u'\xe0', '&thorn;': u'\xfe', '&Ucirc;': u'\xdb', '&amp;': u'&', '&uuml;': u'\xfc', '&ecirc;': u'\xea', '&not;': u'\xac', '&Ograve;': u'\xd2', '&oslash;': u'\xf8', '&Uuml;': u'\xdc', '&cedil;': u'\xb8', '&plusmn;': u'\xb1', '&AElig;': u'\xc6', '&icirc;': u'\xee', '&auml;': u'\xe4', '&ouml;': u'\xf6', '&Ccedil;': u'\xc7', '&euml;': u'\xeb', '&lt;': u'<', '&iquest;': u'\xbf', '&eacute;': u'\xe9', '&ntilde;': u'\xf1', '&pound;': u'\xa3', '&Iuml;': u'\xcf', '&Eacute;': u'\xc9', '&Ntilde;': u'\xd1', '&euro;': u'\u20ac', '&sup2;': u'\xb2', '&Acirc;': u'\xc2', '&ccedil;': u'\xe7', '&Iacute;': u'\xcd', '&quot;': u'"', '&Aring;': u'\xc5', '&macr;': u'\xaf', '&ordm;': u'\xba', '&Oslash;': u'\xd8', '&Otilde;': u'\xd5', '&Ocirc;': u'\xd4', '&reg;': u'\xae', '&Yacute;': u'\xdd', '&iuml;': u'\xef', '&ugrave;': u'\xf9', '&sup3;': u'\xb3', '&curren;': u'\xa4', '&copy;': u'\xa9', '&Atilde;': u'\xc3', '&egrave;': u'\xe8', '&Euml;': u'\xcb', '&uacute;': u'\xfa', '&ograve;': u'\xf2', '&acirc;': u'\xe2', '&aacute;': u'\xe1', '&Agrave;': u'\xc0', '&Oacute;': u'\xd3', '&sect;': u'\xa7', '&yacute;': u'\xfd', '&iacute;': u'\xed', '&cent;': u'\xa2', '&Uacute;': u'\xda', '&otilde;': u'\xf5'}

def wget(url,ap_id=None):
    '''Downloads a web resource with the HTTP protocol
    and returns the result
    
    ap_id is the access point to use.
    If it is None, the user will be prompted'''
    
    if not url.startswith('http://'):
        return None
    
    #Remove protocol part
    url=url[7:]
    
    #split GET and domain
    t=url.split('/',1)
    
    m=t[0].split(':',1)
    if len(m)==1:
        host=m[0]
        port=80
    else:
        host=m[0]
        try:
            port=int(m[1])
        except:
            port=80
    
    if len(t)>1:
        get='/' + t[1]
    else:
        get='/'
        
    hname=host
    if port!=80:
        hname+=":%d" % port
    
    #Download the file
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    sock.connect((host,port))
    sock.send("GET %s HTTP/1.1\r\nConnection: close\r\nHost: %s\r\nUser-Agent: RSS-agk\r\n\r\n" % (get,hname))
    
    
    data=''
    while True:
        r=sock.read(4000)
        if len(r)==0:
            break
        data+=r
    
    
    sock.close()

    #Release access point
    #ap.stop()
    
    #TODO Server didn't return ok
    if data[9:12]!='200':
        show_popup(u'Server returned %s instead of 200' % data[9:12])
        return None
    
    return data.split('\r\n\r\n',1)[1]

class feed_item:
    def __init__(self,item):
        if item==None:
            self.read=None
            self.title=None
            self.description=None
            self.author=None
            self.category=None
            self.comments=None
            self.enclosure=None
            self.pubDate=None
            self.source=None
            self.link=None
            self.guid=None
            return
        
        self.raw=item
        
        self.read=False
        self.title=self._get_tag_content('title')
        self.description=self._get_tag_content('description')
        self.author=self._get_tag_content('author')
        self.category=self._get_tag_content('category')
        self.comments=self._get_tag_content('comments')
        self.enclosure=self._get_tag_content('enclosure')
        self.pubDate=self._get_tag_content('pubDate')
        self.source=self._get_tag_content('source')        
        self.link=self._get_tag_content('link')        
        self.guid=self._get_tag_content('guid')
        
        #Setting link for the item
        if self.link == None and self.guid!=None and self.raw.find('guid isPermaLink="true"')>=0:
            self.link=self.guid
        
        #Converts description into text
        self.description=self._de_html(self.description)
        self.title=self._de_html(self.title)
                
    def _de_html(self,data):
        if data==None:
            return None
            
        #Removing the CDATA tag around the description
        if data.startswith('<![CDATA[') and data.endswith(']]>'):
            data=data[9:-3]
        
        #Replacing some tags into text
        data=data.replace('<br>','\n')
        data=data.replace('<br/>','\n')
        data=data.replace('<br />','\n')
        data=data.replace('<hr>','---')
        data=data.replace('<hr/>','---')
        data=data.replace('<hr />','---')
        data=data.replace('</p>','</p>\n')
        
        #Removing tags and using their text
        while data.find('<')!=-1:
            s=data.find('<')
            e=data.find('>')
            data=data[0:s] + data[e+1:]

        
        for i in html_escape_repl.keys():
            data=data.replace(i,html_escape_repl[i])

        #Converting escape chars
        while data.find('&#')!=-1:
            s=data.find('&#')+2
            e=data[s:].find(';')
            if e>6 or e<0:
                break
            code=data[s:s+e].strip()
            data=data[0:s-2] + unichr(int(code)) + data[s+e+1:]
        return data
        
    def _get_tag_content(self,tag):
        '''Gets the content of a tag'''
        start_item=self.raw.find('<%s' % tag)
        end_start_item=self.raw[start_item:].find('>')
        end_item=self.raw[start_item:].find('</%s>' % tag)

        if start_item>=0 and end_start_item>=0 and end_item>=0:
            return self.raw[1+start_item+end_start_item:start_item+end_item]
        else:
            return ''

class feed:
    def __init__(self,url):
        self.title=url.split("/")[2]
        self.url=url
        self.link=''
        self.items=[]
        
        self.update_feed()
    def _get_tag_content(self,tag):
        '''Gets the content of a tag'''
        start_item=self.raw.find('<%s' % tag)
        end_start_item=self.raw[start_item:].find('>')
        end_item=self.raw[start_item:].find('</%s>' % tag)

        if start_item>=0 and end_start_item>=0 and end_item>=0:
            return self.raw[1+start_item+end_start_item:start_item+end_item]
        else:
            return ''

    def update_feed(self):
        try:
            html = wget(self.url) #TODO use default AP
        except:
            return

        if html==None or html=='':
            show_popup(u"Unable to fetch the feed %s"%self.title)
            return
        
        #some servers appear to send some junk before the actual XML
        html=html[html.find('<?xml'):]
        
        #find encoding
        first_line=html[0:html.find('\n')]
        print "1st line: ",first_line
        
        enc_s=first_line.find('encoding="')+10
        if enc_s!=-1:
            enc_e=first_line[enc_s:].find('"')
            
            print "enc_s=%d   enc_e=%d" % (enc_s,enc_e)
            
            
            encoding=first_line[enc_s:enc_s+enc_e]
            
            try:
                html=unicode(html,encoding)#html.decode(encoding)
            except:
                print "NO MODULE FOR '%s'"% encoding
                sys.exit(1)

        #Used to keep all the html which is not into items
        preitems=html[0:html.find('<item')]
        
        while html.find('<item')>=0:
            start_item=html.find('<item')
            end_start_item=html[start_item:].find('>')
            end_item=html[start_item:].find('</item>')

            item=html[start_item+end_start_item:start_item+end_item]
            #Moves to the next item
            html=html[start_item+end_item:] 
            #adds item
            self.items.append(feed_item(item))
        
        self.raw=preitems+html
        title=self._get_tag_content('title')
        if title!='':
            self.title=title
        self.link=self._get_tag_content('link')
        
    def get_unread(self):
        '''Returns the amount of unread items'''
        count=0
        for i in self.items:
            if i.read==False:
                count+=1
        return count
        
    def get_title(self):
        '''Returns the title of the feed'''
        return self.title
        
    def get_articles(self):
        '''Returns a list of articles'''
        articles=[]
        for i in self.items:
            
            #Cuts too long names
            if len(i.title)>30:
                t=i.title[0:30]
            else:
                t=i.title
                
            #Adds a trailing * for unread articles
            if i.read==False:
                t='*%s'%t
            articles.append(t)
        if len(articles)==0:
            articles.append(u'No items...')
        return articles
    def __str__(self):
        return u"%s (%d)" %(self.get_title(),self.get_unread())

class global_vars:
    def __init__(self):
        self.current_feed=0
        self.current_article=0
        self.view_state=0 #0 is list of feeds, 1 is list of news and 2 is text of the new


ap_id=socket.select_access_point()
ap=socket.access_point(ap_id)
socket.set_default_access_point(ap)

gvars=global_vars()

feeds=[]
feeds.append(feed(u'http://www.ft.com/rss/companies/technology'))
feeds.append(feed(u'http://supersalvus.altervista.org/rss.php'))
feeds.append(feed(u'http://feeds.feedburner.com/Spinoza'))
feeds.append(feed(u'http://twitter.com/statuses/user_timeline/41667342.rss'))
#feeds.append(feed(u'http://www.uaar.it/news/feed/'))


def open_link(url):
    '''Opens a link in the external browser'''
    
    '''apprun = u'z:\\system\\programs\\apprun.exe'
    browser = u'z:\\System\\Apps\\Browser\\Browser.app'
    #url = 'http://www.google.com'
    print url
    e32.start_exe(apprun, browser + u' "%s"' %url , 1)'''
    
    browserApp ='BrowserNG.exe'
    #url = 'www.google.com'
    e32.start_exe(browserApp, ' "4 %s"' %url, 1)


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
    elif gvars.view_state==1 and len(feeds[gvars.current_feed].items)==0:
        pass #There is only a placeholder item that shows that there aren't items
    elif gvars.view_state==1: #Goes to state 2 to read the article
        gvars.current_article=main_list.current() #Sets the index for the current article
        feeds[gvars.current_feed].items[gvars.current_article].read=True #Marks the article as read
        gvars.view_state=2
        update_view()
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
    elif gvars.view_state==1:
        main_list.set_list(feeds[gvars.current_feed].get_articles())
        appuifw.app.body=main_list #Sets this in case we are coming back from state 2
    elif gvars.view_state==2:
        article=feeds[gvars.current_feed].items[gvars.current_article]
        #self.source=self._get_tag_content('source')        
        #self.link=self._get_tag_content('link')        
        #self.guid=self._get_tag_content('guid')
        main_txt.set('%s\n---------\n%s\n\n%s\n%s' %(article.title,article.description,article.author,article.pubDate))
        main_txt.set_pos(0)
        appuifw.app.body=main_txt
        
def open_in_browser():
    '''Opens the selected item in an external browser'''
    url=''
    
    if gvars.view_state==0 and len(feeds)>0: 
        url=feeds[main_list.current()].link
    elif (gvars.view_state==1 and len(feeds[gvars.current_feed].items)>0) or gvars.view_state==2:
        article=feeds[gvars.current_feed].items[gvars.current_article]
        url=article.link
        article.read=True #Marks the article as read, even if viewed externally
        if gvars.view_state==1: update_view() #Updates view in case we are listing the articles
        
    if url!='':
        open_link(url)
    else:
        show_popup(u'Item doesn\'t provide any link')

def mark_feed_read():
    '''Marks the current feed as read'''
    if len(feeds)==0: 
        return
    for i in feeds[main_list.current()].items:
        i.read=True
    update_view()

def mark_all_feeds_read():
    for f in feeds:
        for i in f.items:
            i.read=True
    update_view()

def init_menu():
    appuifw.app.menu = [(u"Options",(
        (u"View in browser", open_in_browser),
        (u"Update feed", do_nothing),
        (u"Update all feeds", do_nothing),
        (u"Add feed", add_feed),
        (u"Remove feed", remove_feed),
        (u"Mark feed as read", mark_feed_read),
        (u"Mark all feeds as read", mark_all_feeds_read),
        (u"About", about),
        (u"Exit", exit_key_handler),
        ))
    ]

def about():
    show_popup(u"RSS-agk by Salvo 'LtWorf' Tomaselli")

app=appuifw.app
app.title=u"RSS-agk"
app.screen='normal'


# create your content list of your listbox including the icons to be used for each entry
main_list = appuifw.Listbox(get_feeds_entries(),list_click)
main_txt = appuifw.Text()

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
