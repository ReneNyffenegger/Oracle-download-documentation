#!/usr/bin/env python3

import os
from bs4 import BeautifulSoup
import requests

url_root='https://docs.oracle.com/en/database/oracle/oracle-database/'

if not os.path.exists('docu'):
    os.makedirs('docu')

def hrefs_at(url):

    res  = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    links = soup.find_all('a')

    return [link.get('href') for link in links]
    

def download_file(url):

    print(url)

    local_filename = 'docu/' + os.path.basename(url) 
    if os.path.exists(local_filename):
       print(f'{url} was already downloaded')
       return

    res = requests.get(url)

    if res.status_code == 200:
       with open(local_filename, 'wb') as file:
            file.write(res.content)
            print(f'downloaded: {url}')
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

def download_pdfs(rel_path):
    hrefs = hrefs_at(url_root + rel_path)
    for href in hrefs:
        if href != None and href.endswith('.pdf'):
           download_file(os.path.dirname(url_root + rel_path) + '/' + href)

hrefs = hrefs_at(url_root)
for href in hrefs:

    if href.startswith('23/'): # Only interested in 23c documentation, at the moment!
       download_pdfs(href)

#
#  Additional files
#  Can the link to the most current version extracted from
#     https://docs.oracle.com/en/database/oracle/sql-developer-command-line/index.html
#  automatically?
#
download_file('https://docs.oracle.com/en/database/oracle/sql-developer-command-line/23.4/sqcug/oracle-sqlcl-users-guide.pdf')
