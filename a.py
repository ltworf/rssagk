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
import cPickle


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

    #Release access point
    #ap.stop()
    
    #TODO Server didn't return ok
    if data[9:12]!='200':
        show_popup(u'Server returned %s instead of 200' % data[9:12])
        return None
    
    return data.split('\r\n\r\n',1)[1]

class feed_item:
    def __init__(self,item):
        
        #In case we are loading the item from a dictionary
        if isinstance(item,dict):
            self.raw=None
            self.read=item['read']
            self.title=item['title']
            self.description=item['description']
            self.author=item['author']
            self.category=item['category']
            self.comments=item['comments']
            self.enclosure=item['enclosure']
            self.pubDate=item['pubDate']
            self.source=item['source']
            self.link=item['link']
            self.guid=item['guid']
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
    def to_dic(self):
        '''Returns a dict that can be used to generate the object again'''
        d={}
        d['read']=self.read
        d['title']=self.title
        d['description']=self.description
        d['author']=self.author
        d['category']=self.category
        d['comments']=self.comments
        d['enclosure']=self.enclosure
        d['pubDate']=self.pubDate
        d['source']=self.source
        d['link']=self.link
        d['guid']=self.guid
        return d
        
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
    def __eq__(self,other):
        '''Compares two items basing on their guid'''
        if not isinstance(other,feed_item):
            return False
        return self.guid==other.guid
        
class feed:
    def __init__(self,url):
        '''Inits a feed object.
        Can accept a string containing an url or
        a dictionary containing a stored feed object'''
        
        self.items=[]
        self.id_map=None
        
        if isinstance(url,dict):
            self.url=url['url']
            self.link=url['link']
            self.title=url['title']
            
            for i in url['items']:
                self.items.append(feed_item(i))
            return
        
        self.title=url.split("/")[2]
        self.url=url
        self.link=''
        
        self.update_feed()
    def to_dic(self):
        d={}
        d['url']=self.url
        d['link']=self.link
        d['title']=self.title
        itms=[]
        for i in self.items:
            itms.append(i.to_dic())
        d['items']=itms
        return d
        
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
        #print "1st line: ",first_line
        
        
        enc_s=first_line.find('encoding=')
        if enc_s!=-1:
            enc_s+=10
            quot=first_line[enc_s-1]
            enc_e=first_line[enc_s:].find(quot)
            
            #print "enc_s=%d   enc_e=%d quot %s" % (enc_s,enc_e,quot)
            
            
            encoding=first_line[enc_s:enc_s+enc_e]
            
            try:
                html=unicode(html,encoding)#html.decode(encoding)
            except:
                print "NO MODULE FOR '%s'"% encoding
                sys.exit(1)

        #Used to keep all the html which is not into items
        preitems=html[0:html.find('<item')]
        
        items=[]
        
        while html.find('<item')>=0:
            start_item=html.find('<item')
            end_start_item=html[start_item:].find('>')
            end_item=html[start_item:].find('</item>')

            item=html[start_item+end_start_item:start_item+end_item]
            #Moves to the next item
            html=html[start_item+end_item:] 
            #adds item
            new_item=feed_item(item)
            if new_item not in self.items:
                items.append(new_item)
        
        #Merge items lists
        self.items=items+self.items
        
        #TODO delete items if they exceed       settings['items_per_feed']
        
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
        self.id_map=[]
        for i in range(len(self.items)):
            if settings['show_read']==False and self.items[i].read==True:
                continue
                
            #Cuts too long names
            if len(self.items[i].title)>settings['chars_per_line']:
                t=self.items[i].title[0:settings['chars_per_line']]
            else:
                t=self.items[i].title
                
            #Adds a trailing * for unread articles
            if self.items[i].read==False:
                t=u'*%s'%t
                
            self.id_map.append(i) #Real index of the item
            articles.append(t)
        if len(articles)==0:
            articles.append(u'No items...')
        return articles
    def __str__(self):
        
        #TODO if len(self.items[i].title)>settings['chars_per_line']:
        #        t=self.items[i].title[0:settings['chars_per_line']]
        #    else:
        #        t=self.items[i].title
                
        return u"%s (%d)" %(self.get_title(),self.get_unread())

class global_vars:
    
    
    def __init__(self):
        self.current_feed=0
        self.current_article=0
        self.view_state=0 #0 is list of feeds, 1 is list of news and 2 is text of the new

class global_db:
    '''This class handles loading and storing all the data'''
    
    
    def __init__(self):
        try:
            pkl_file = open("feed.dat", 'r')
            sett = cPickle.load(pkl_file)
            pkl_file.close()
        except:
            return
        
        for i in sett['feeds']:
            feeds.append(feed(i))
        sett['feeds']=None #Releases since it's no longer in use
        
        for i in sett:
            settings[i]=sett[i]
        
        
        #Default settings
        if 'show_read' not in settings:
            settings['show_read']=True
        if 'update_on_open' not in settings:
            settings['update_on_open']=False
        if 'default_ap' not in settings:
            settings['default_ap']='---None---'
        if 'items_per_feed' not in settings:
            settings['items_per_feed']=200
        if 'chars_per_line' not in settings:
            settings['chars_per_line']=40
            
    def close(self):
        
        f=[]
        for i in feeds:
            f.append(i.to_dic())
        
        '''Closes the db'''
        output = open("feed.dat", 'wb')
        
        settings['feeds']=f

        # Pickle dictionary using protocol 0.
        cPickle.dump(settings, output)

        output.close()
        
    def load_feed(self):
        pass
    def add_feed(self,new_feed):
        pass
    def del_feed(self,f):
        pass


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
    '''Exits the application'''
    gdb.close() #Closes the database
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
        feeds[gvars.current_feed].items[feeds[gvars.current_feed].id_map[gvars.current_article]].read=True #Marks the article as read
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
        
    #Doesn't add existing feeds    
    for i in feeds:
        if i.url==uri:
            show_popup(u'Feed already imported')
            return
    try:
        new_feed=feed(uri)
        feeds.append(new_feed)
        gdb.add_feed(new_feed)
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
        gdb.del_feed(feeds[index]) #Deletes the feed from the db
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
        article=feeds[gvars.current_feed].items[feeds[gvars.current_feed].id_map[gvars.current_article]]
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
        article=feeds[gvars.current_feed].items[feeds[gvars.current_feed].id_map[gvars.current_article]]
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

def update_feed():
    '''Updates the current feed'''
    if len(feeds)==0: 
        return
    feeds[main_list.current()].update_feed()
    update_view()

def update_all_feeds():
    for f in feeds:
        f.update_feed()
    update_view()

    
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
    show_popup(u"RSS-agk by Salvo 'LtWorf' Tomaselli")

def associate_ap():
    ap_id=None
    
    for i in btsocket.access_points():
        if i['name']==settings['default_ap']:
            ap_id=i['iapid']
            break
        
    if ap_id==None:
        return
        
    #ap_id=btsocket.select_access_point() #Selects the access point and returns its id
    ap=btsocket.access_point(ap_id)      #Create the access point object
    btsocket.set_default_access_point(ap)


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

feeds=[]
settings={}


gvars=global_vars()
gdb=global_db()


#feeds.append(feed(u'http://www.ft.com/rss/companies/technology'))
#feeds.append(feed(u'http://supersalvus.altervista.org/rss.php'))
#feeds.append(feed(u'http://feeds.feedburner.com/Spinoza'))
#feeds.append(feed(u'http://twitter.com/statuses/user_timeline/41667342.rss'))
#feeds.append(feed(u'http://www.uaar.it/news/feed/'))



associate_ap()




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



#Stuff to do once the GUI is loaded
if settings['update_on_open']:
    update_all_feeds()




# create an Active Object
app_lock = e32.Ao_lock()
app_lock.wait()
