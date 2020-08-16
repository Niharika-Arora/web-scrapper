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

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def find_link(url):
    r = requests.get(url, headers = headers)
    #txt = BeautifulSoup(r.text, 'html.parser')
    links = []
    links = re.findall('<a.*?href="(http.*?)".*?>', r.text)
    #for link in txt.findAll('a'):
        #links.append(link.get('href'))
    print("got links")
    print(links)
    return r, links

def contact_check(url, links):
    url1 = ''
    for link in links:
        if str(link).casefold() == '/contact'.casefold() or str(link).casefold() == '/contact-us'.casefold() or str(link).casefold() == '/contactus'.casefold():
            url1 = url + link
        elif str(link) == str(url+'/contact') or str(link) == str(url+'/contact-us') or str(link) == str(url+'/contactus'):
            url1 = link
    if url1 != '':
        print("got url")
    return url1

def save_file(url):
    print(url)
    r = requests.get(url, headers = headers)
    #txt = r.text
    #visible_texts = filter(tag_visible, txt)
    #print(str(visible_texts))
    mail_list = re.findall(r'[a-z0-9_\-\.]+@[a-z\.]+\.[a-z]{2,3}', str(r.text))
    print(mail_list)
    #phone = re.findall(r'<.+?>.*?((\+(\d\-\ )?\d{2,3}[\s\-]?)?(\d{10}|(\(\d{3}\)([\s\-]?)\d{3}\6\d{4})|(\d{3}([\s\-]?)\d{3}\8\d{4}))).*?</.*?>', str(r.text))
    #phone = list(x[2] for x in phone)
    phone = re.findall(r'[:\+\][0-9]{3,5}[\ \-\][0-9]{4,6}[\ \-\][0-9]{5,6}', str(r.text))
    #phone = re.findall(r'(\+(\d\-\ )?\d{2,3}[\s\-]?)?(\d{10}|(\(\d{3}\)([\s\-]?)\d{3}\5\d{4})|(\d{3}([\s\-]?)\d{3}\7\d{4})|(\d{4}[\s\-]?\d{4}))', str(r.text))
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
    print("url")
    url1 = contact_check(url, lin)
    print("url contact")
    ln = lin
    print(url1)
    if url1 != '':
        print("file to be saved")
        save_file(url1)
    else:
        while flag == True:
            for l in ln:
                url2 = url + l
                print("getting response")
                res = requests.get(url2, headers = headers)
                print(url2)
                if res.status_code == 404:
                    print("continue")
                    continue
                else:
                    res, ln = find_link(url2)
                    url2 = contact_check(url2, ln)
                    if url2 == '':
                        continue
                    else:
                        save_file(url2)
                        print("break")
                        break
            flag = False
    sys.exit(0)
