import xlrd
import os
import re
import requests
import pandas
from bs4 import BeautifulSoup


loc = os.path.abspath('websites.xlsx')
wb = xlrd.open_workbook(loc)
st = wb.sheet_by_index(0)
st.cell_value(0, 0)

site = input("Enter name: ")
url = ''

for i in range(st.nrows):
    if site == str(st.cell_value(i, 0)):
        url = str(st.cell_value(i, 1))
if url == '':
    url = "URL Not Found!"
print(url)

headers = {"Accept-Language": "en-US, en;q=0.5"}
r = requests.get(url, headers = headers)
txt = BeautifulSoup(r.text, 'html.parser')

links = []

for link in txt.findAll('a'):
    links.append(link.get('href'))
print(links)

mail_list = re.findall('[a-z0-9_\-\.]+@[a-z\.]+\.[a-z]{2,3}')
phone = re.findall('(\+(\d\-)?\d{2,3}[\s\-]?)?(\d{10}|(\(\d{3}\)([\s\-]?)\d{3}\5\d{4})|(\d{3}([\s\-]?)\d{3}\7\d{4}))')
