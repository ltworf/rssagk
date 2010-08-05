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

def wget(url):
    if not url.startswith('http://'):
        return None
    
    #Remove protocol part
    url=url[8:]
    
    
    
    
wget ('http://ciao.com:8080/index.rss')

'''ap_id=socket.select_access_point()
ap=socket.access_point(ap_id)

socket.set_default_access_point(ap)


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print ap.ip()

sock.connect(('www.sourceforge.net',80))
sock.send("GET / HTTP/0.9\r\n\r\n")
#print sock.recv(100)
#print dir(sock)
print sock.read(100)

sock.close()

#Release access point
ap.stop()
'''