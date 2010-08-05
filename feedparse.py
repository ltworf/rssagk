#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=UTF-8
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

class feed_item:
    def __init__(self,item):
        self.raw=item
        
        print item
        
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
        if self.link == None and self.guid!=None and self.raw.find('guid isPermaLink="true"')>=0:
            self.link=self.guid
        
        
        
        
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
#response = urllib2.urlopen('http://supersalvus.altervista.org/rss.php')
response = urllib2.urlopen('http://www.ft.com/rss/companies/technology')
html = response.read()

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
