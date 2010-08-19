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

import socket

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
    
    #TODO handle IPv6 addresses
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
    if ap_id==None:
        ap_id=socket.select_access_point()
    ap=socket.access_point(ap_id)
    #socket.set_default_access_point(ap)
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
    ap.stop()
    
    return data.split('\r\n\r\n',1)[1]

print wget ('http://10.50:8080/film/altri/')
