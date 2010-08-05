#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=UTF-8
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

class feed_item:
    def __init__(self,item):
        self.raw=item
        
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
        
        print self.description
        
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
            
            
        data=data.replace(u"&euro;",u"€")
        data=data.replace(u"&nbsp;",u" ")
        data=data.replace(u"&quot;",u"\"")
        data=data.replace(u"&amp;",u"&")
        data=data.replace(u"&lt;",u"<")
        data=data.replace(u"&gt;",u">")
        data=data.replace(u"&iexcl;",u"¡")
        data=data.replace(u"&cent;",u"¢")
        data=data.replace(u"&pound;",u"£")
        data=data.replace(u"&curren;",u"¤")
        data=data.replace(u"&yen;",u"¥")
        data=data.replace(u"&brvbar;",u"¦")
        data=data.replace(u"&sect;",u"§")
        data=data.replace(u"&uml;",u"¨")
        data=data.replace(u"&copy;",u"©")
        data=data.replace(u"&ordf;",u"ª")
        data=data.replace(u"&not;",u"¬")
        data=data.replace(u"&reg;",u"®")
        data=data.replace(u"&macr;",u"¯")
        data=data.replace(u"&deg;",u"°")
        data=data.replace(u"&plusmn;",u"±")
        data=data.replace(u"&sup2;",u"²")
        data=data.replace(u"&sup3;",u"³")
        data=data.replace(u"&acute;",u"´")
        data=data.replace(u"&micro;",u"µ")
        data=data.replace(u"&para;",u"¶")
        data=data.replace(u"&middot;",u"·")
        data=data.replace(u"&cedil;",u"¸")
        data=data.replace(u"&sup1;",u"¹")
        data=data.replace(u"&ordm;",u"º")
        data=data.replace(u"&raquo;",u"»")
        data=data.replace(u"&frac14;",u"¼")
        data=data.replace(u"&frac12;",u"½")
        data=data.replace(u"&frac34;",u"¾")
        data=data.replace(u"&iquest;",u"¿")
        data=data.replace(u"&Agrave;",u"À")
        data=data.replace(u"&Aacute;",u"Á")
        data=data.replace(u"&Acirc;",u"Â")
        data=data.replace(u"&Atilde;",u"Ã")
        data=data.replace(u"&Auml;",u"Ä")
        data=data.replace(u"&Aring;",u"Å")
        data=data.replace(u"&AElig;",u"Æ")
        data=data.replace(u"&Ccedil;",u"Ç")
        data=data.replace(u"&Egrave;",u"È")
        data=data.replace(u"&Eacute;",u"É")
        data=data.replace(u"&Ecirc;",u"Ê")
        data=data.replace(u"&Euml;",u"Ë")
        data=data.replace(u"&Igrave;",u"Ì")
        data=data.replace(u"&Iacute;",u"Í")
        data=data.replace(u"&Icirc;",u"Î")
        data=data.replace(u"&Iuml;",u"Ï")
        data=data.replace(u"&ETH;",u"Ð")
        data=data.replace(u"&Ntilde;",u"Ñ")
        data=data.replace(u"&Ograve;",u"Ò")
        data=data.replace(u"&Oacute;",u"Ó")
        data=data.replace(u"&Ocirc;",u"Ô")
        data=data.replace(u"&Otilde;",u"Õ")
        data=data.replace(u"&Ouml;",u"Ö")
        data=data.replace(u"&times;",u"×")
        data=data.replace(u"&Oslash;",u"Ø")
        data=data.replace(u"&Ugrave;",u"Ù")
        data=data.replace(u"&Uacute;",u"Ú")
        data=data.replace(u"&Ucirc;",u"Û")
        data=data.replace(u"&Uuml;",u"Ü")
        data=data.replace(u"&Yacute;",u"Ý")
        data=data.replace(u"&THORN;",u"Þ")
        data=data.replace(u"&szlig;",u"ß")
        data=data.replace(u"&agrave;",u"à")
        data=data.replace(u"&aacute;",u"á")
        data=data.replace(u"&acirc;",u"â")
        data=data.replace(u"&atilde;",u"ã")
        data=data.replace(u"&auml;",u"ä")
        data=data.replace(u"&aring;",u"å")
        data=data.replace(u"&aelig;",u"æ")
        data=data.replace(u"&ccedil;",u"ç")
        data=data.replace(u"&egrave;",u"è")
        data=data.replace(u"&eacute;",u"é")
        data=data.replace(u"&ecirc;",u"ê")
        data=data.replace(u"&euml;",u"ë")
        data=data.replace(u"&igrave;",u"ì")
        data=data.replace(u"&iacute;",u"í")
        data=data.replace(u"&icirc;",u"î")
        data=data.replace(u"&iuml;",u"ï")
        data=data.replace(u"&eth;",u"ð")
        data=data.replace(u"&ntilde;",u"ñ")
        data=data.replace(u"&ograve;",u"ò")
        data=data.replace(u"&oacute;",u"ó")
        data=data.replace(u"&ocirc;",u"ô")
        data=data.replace(u"&otilde;",u"õ")
        data=data.replace(u"&ouml;",u"ö")
        data=data.replace(u"&divide;",u"÷")
        data=data.replace(u"&oslash;",u"ø")
        data=data.replace(u"&ugrave;",u"ù")
        data=data.replace(u"&uacute;",u"ú")
        data=data.replace(u"&ucirc;",u"û")
        data=data.replace(u"&uuml;",u"ü")
        data=data.replace(u"&yacute;",u"ý")
        data=data.replace(u"&thorn;",u"þ")
        
        
        #Converting escape chars
        while data.find('&#')!=-1:
            print ">===\n"
            
            s=data.find('&#')+2
            e=data[s:].find(';')
            print s,e
            if e>6 or e<0:
                break
            #print "----",data[s:e]
            #print data[0:s]
            #print data
            code=data[s:s+e].strip()
            print 
            data=data[0:s] + unichr(int(code)) + data[e+1:]
            print "<===\n\n\n"
        return data
        
    def get_description(self):
        pass
    
    def _get_tag_content(self,tag):
        '''Gets the content of a tag'''
        start_item=self.raw.find('<%s' % tag)
        end_start_item=self.raw[start_item:].find('>')
        end_item=self.raw[start_item:].find('</%s>' % tag)

        if start_item>=0 and end_start_item>=0 and end_item>=0:
            return self.raw[1+start_item+end_start_item:start_item+end_item]
        else:
            return None




import urllib2
response = urllib2.urlopen('http://supersalvus.altervista.org/rss.php')
#response = urllib2.urlopen('http://www.ft.com/rss/companies/technology')
#response = urllib2.urlopen('http://www.uaar.it/news/feed/')
html = response.read()

#find encoding
enc_s=html[0:html.find('\n')].find('encoding="')+10
enc_e=html[enc_s:html.find('\n')].find('"')
encoding=html[enc_s:enc_s+enc_e]

#
html=html.decode(encoding)

while html.find('<item')>=0:
    start_item=html.find('<item')
    end_start_item=html[start_item:].find('>')
    end_item=html[start_item:].find('</item>')

    item=html[start_item+end_start_item:start_item+end_item]
    #Moves to the next item
    html=html[start_item+end_item:] 
    #print item
    print feed_item(item)
    print
