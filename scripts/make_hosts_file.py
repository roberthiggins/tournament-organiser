#!/usr/bin/env python

"""
Make a basic hosts file. This should help avoid some security loopholes. You
can then append the contents of the file to whichever hosts files you need to.
"""

from bs4 import BeautifulSoup
import requests

REQUEST = requests.get('http://someonewhocares.org/hosts/').text
HTML = BeautifulSoup(REQUEST, 'html.parser')

with open("hosts", "w") as t_file:
    t_file.write(HTML.body.find('div', class_='BODY').pre.text.encode('utf8'))
