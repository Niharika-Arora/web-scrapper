import xlrd
import os
import re
import requests
import pandas
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import sys


headers = {"Accept-Language": "en-US, en;q=0.5"}


def find_link(url):
    r = requests.get(url, headers = headers)
    links = []
    links = re.findall('<a.*?href="(http.*?)".*?>', r.text)
    print(links)
    return r, links

def contact_check(url, links):
    url1 = ''
    for link in links:
        if str(link).casefold() == '/contact'.casefold() or str(link).casefold() == '/contact-us'.casefold() or str(link).casefold() == '/contactus'.casefold():
            url1 = url + link
        elif str(link) == str(url+'/contact') or str(link) == str(url+'/contact-us') or str(link) == str(url+'/contactus'):
            url1 = link
    return url1

def save_file(url):
    r = requests.get(url, headers = headers)
    mail_list = re.findall(r'[a-z0-9_\-\.]+@[a-z\.]+\.[a-z]{2,3}', str(r.text))
    print(mail_list)
    phone = re.findall(r'[:\+\][0-9]{3,5}[\ \-\][0-9]{4,6}[\ \-\][0-9]{5,6}', str(r.text))
    print(phone)
    dicn = {'link': url, 'email': mail_list, 'phone number': phone}
    df = pandas.DataFrame.from_dict(dicn, orient= 'index')
    df.transpose()
    df.to_csv('contact_info.csv')
    print("File Saved!!")

if __name__ == "__main__":
    loc = os.path.abspath('websites.xlsx')
    wb = xlrd.open_workbook(loc)
    st = wb.sheet_by_index(0)
    st.cell_value(0, 0)

    site = input("Enter name: ")
    url = ''

    for i in range(st.nrows):
        if site.casefold() == str(st.cell_value(i, 0)).casefold():
            url = str(st.cell_value(i, 1))
    if url == '':
        print("URL Not Found!")
        sys.exit(0)
    print(url)
    lin = []
    url2 = ''
    url1 = ''
    flag = True
    response, lin = find_link(url)
    url1 = contact_check(url, lin)
    ln = lin
    print(url1)
    if url1 != '':
        save_file(url1)
    else:
        while flag == True:
            for l in ln:
                url2 = url + l
                res = requests.get(url2, headers = headers)
                print(url2)
                if res.status_code == 404:
                    continue
                else:
                    res, ln = find_link(url2)
                    url2 = contact_check(url2, ln)
                    if url2 == '':
                        continue
                    else:
                        save_file(url2)
                        break
            flag = False
    sys.exit(0)
