from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import datetime
import pickle
import nltk
import codecs
from nltk.corpus import words
import numpy
import re
'''
simple_get determines whether or not the url is usable. If it is,
then we get the url as output. Else we get None value. 
Input: String URL
Return: String URL or None
'''
def simple_get(url):
    try:
        with closing(get(url, stream = True)) as resp:
            if is_good_response(resp):
                return resp.text
            else:
                return None
    except RequestException as e:
        log_error('Error during request to {0} : {1}'.format(url, str(e)))
        return None
'''
is_good_response determines the whether or not the HTTP is good. Code 200 means
delivers the response 'ok' 
Input: context manager that closes on completion 
Output: 'ok' response 
'''
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return(resp.status_code == 200
           and content_type is not None
           and content_type.find('html') > -1)
'''
prints error
Input: String
Output: String
'''
def log_error(e):
    print(e)

'''
Saves a list to a .p file.
Input: list, String
'''
def pickle_save(list, name):
    pickle.dump(list, open(name + ".p","wb",))
'''
Loads a .p file to a list
Input: list, String
'''
def pickle_load(list, name):
    list = pickle.load(open(name + ".p", "rb"))
'''
Looks through through every link in http://www.newyorksocialdiary.com/party-pictures
before December 1st, 2014 and takes all photocaptions that contain the names of people
who appear at the party. 
'''
def scrape():
    l1 = list()
    l2 = list()
    l3 = list()
    l4 = list()
    d = {}
    global globnum
    global globcount
    global beforedate
    globcount = 0
    #try/except block contains all the code that finds the links in newyroksocialdiary.com/party-pictures
    try:
        raw_html = simple_get('http://www.newyorksocialdiary.com/party-pictures')
        html = BeautifulSoup(raw_html, 'html.parser')
        for li in html.findAll('li', attrs={'class': 'pager__item--last'}):
            lastlink = (li.find('a')['href'])
            globnum = int(lastlink[-2:])
        for x in range(0, globnum + 1):
            if(x == 0):
                raw_html = simple_get('http://www.newyorksocialdiary.com/party-pictures')
            raw_html = simple_get('http://www.newyorksocialdiary.com/party-pictures' + '?page=' + str(x))
            html = BeautifulSoup(raw_html, 'html.parser')
            if(x == globnum):
                for li in html.findAll('div', attrs={'class': 'views-row'}):
                    globcount += 1
                for i, li in enumerate(html.select('a')):
                    if (i >= 19 and i < 19 + globcount):
                        l1.append(li.get('href'))
                for ind in range(1,globcount + 1):
                    l2.append(datetime.datetime.strptime(html.find("div", class_=("views-row" + "-" + str(ind))).find("span",
                                                                                   class_="views-field-created").text,' %A, %B %d, %Y '))

            else:
                for i, li in enumerate(html.select('a')):
                    if(i >= 19 and i <= 68):
                        l1.append(li.get('href'))
                for ind in range(1, 51):
                    l2.append(datetime.datetime.strptime(html.find("div", class_=("views-row" + "-" + str(ind))).find("span",
                                                                                   class_="views-field-created").text,' %A, %B %d, %Y '))

            pickle_save(l1, 'l1')
            pickle_save(l2, 'l2')
    except:
        pass
    #Looking for all the links that are before December 1st, 2014
    pickle_load(l1, 'l1')
    pickle_load(l2, 'l2')
    for x in l2:
        if x < datetime.datetime.strptime(" Monday, December 1, 2014 ", ' %A, %B %d, %Y '):
            l3.append(x)
    for x in l2:
        if x == datetime.datetime.strptime(" Monday, December 1, 2014 ", ' %A, %B %d, %Y '):
            globaldate = l2.index(x)
    for x in range(globaldate+1, len(l1)):
        l4.append(l1[x])
    for x in range(0,len(l4)):
        d[l4[x]] = l3[x]
    pickle_save(d,'dict')
    captions = list()
    l5 = list()
    #Get all of the photocaptions and convert the raw_html to text
    for x in l4:
        l5.append('http://www.newyorksocialdiary.com' + x)
    '''for i, x in enumerate(l5):
        try:
            raw_html = simple_get(x)
            html = BeautifulSoup(raw_html, 'html.parser')
            print(i,x)
        except:
            pass'''
    captionfile = codecs.open('captions.txt', "w+", "utf-8")

    for x in l5:
        try:
            raw_html = simple_get(x)
            html = BeautifulSoup(raw_html, 'lxml')
            print(x)
        except:
            pass
        for wrapper in html.findAll('div', class_='photocaption'):
            captionfile.write(wrapper.text.strip()+ "\n"+ " ")
        for caption in html.findAll('table', cellpadding = 1):
            captionfile.write(" ".join(caption.text.split())+ "\n"  + " ")
    captionfile.close()
'''
The Parser function. Parses the files that are already created by the scraper.
Prints out all of the unique names within the photocaptions as well the name 
that pops up the most often. 
'''
def parse():
    clist = [] #container for lines within a file
    dlist = [] #container for lines within a file
    elist = [] #container for lines within a file
    flist = [] #container for lines within a file
    poplist = []
    names = set()
    test_patterns = r"'s|’s|'d|'|&" #filter out these patterns
    test_patterns2 = r"," #filter out these patterns
    sfile = codecs.open('captionsfinal.txt', "r", "utf-8")
    tfile = codecs.open('newcaption.txt' , "w", "utf-8")
    linelist = sfile.readlines()
    for line in linelist:
        if(len(line) < 250):
            clist.append(line)
    for x in clist:
        j = re.sub(test_patterns,'',x)
        dlist.append(j)
        tfile.write(j) # james and bob smith
    for x in dlist:
        namelist = x.split()
        # and John and Molly Garone
        if len(namelist) == 4 and ( namelist[1] == 'and' or namelist[1] == 'AND'):
            elist.append(namelist[0] + " " + namelist[3])
            elist.append(namelist[2] + " " + namelist[3])
        j = re.split(test_patterns2, x)
        for i in j:
            elist.append(i)
    rfile = codecs.open('test.txt', "w" , "utf-8")
    for x in elist:
        xlist = x.split()
        leng = len(xlist)
        if len(xlist) == 5 and (xlist[0] == "and" or xlist[0] == "AND"):
            elist.append(xlist[1] + " " + xlist[4])
            elist.append(xlist[3] + " " + xlist[4])
        if len(xlist) == 3 and (xlist[0]) == "and":
            elist.remove(x)
            elist.append(xlist[1] + xlist[2])
    for x in elist:
        xlist = x.split()
        if len(xlist) > 1 and len(xlist) < 4:
            rfile.write(x)
            poplist.append(x)
            names.add(x)
    pickle_save(names, 'names')
    pickle_save(poplist, 'poplist')

def main():
    #scrape()
    #parse()
    poplist = pickle.load(open("poplist.p", "rb")) #total number of names
    names = pickle.load(open("names.p", "rb")) #total number of unique names
    for people in names:
        print(people)
    print("There are a total of " + str(len(names)) + " unique names")
    #The total number of unique names is 61257
if __name__ == "__main__":
    main()

