'''
Necessary libraries for this program to function. BeautifulSoup must be installed locally; to do so, type pip install bs4 into your
terminal.
'''
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import sys
import subprocess
import requests

class Executive:
    '''
    Getter methods used to extract specific data from an html source
    '''
    def __init__(self):
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
        self.email_format = re.compile('[A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net)')
        self.number_format = re.compile('[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]')


    def start(self):
        user_input = input('Paste a valid url: \n')
        if(user_input != None):
            self.loop(user_input)
        else:
            print('Invalid entry, please try again. \n')
            self.start()

    def loop(self, inp):
        choice = ''
        while (choice != '6'):
            self.menu()
            choice = input('Enter an option:\n')
            if choice == '1':
                print(self.getSiteHtml(inp))
            elif choice == '2':
                print(self.specificTags())
            elif choice == '3':
                print(*self.getLinks(inp), sep='\n')
            elif choice == '4':
                print(self.getEmails(inp))
            elif choice == '5':
                print(self.getPhoneNumbers(inp))
            elif choice != '6':
                print('Invalid entry, please try again. \n')
                self.loop(inp)

    def specificTags(self, url):
        tag_type = input('Enter a tag type: ')
        attribute = input('Enter the tag attribute: ')


    def getTitle(self, url):
        try:
            html_code = self.getSiteHtml(url)
            page_title = html_code.title
        except HTTPError as e:
            print(e)
        except URLError as f:
            print('Server non-existent!')
        except AttributeError as g:
            print('Tag was not found')
        else:
            return page_title.get_text()


    def getSiteHtml(self, url):
        try:
            html = urlopen(url)
            bs = BeautifulSoup(html, 'html.parser')
        except HTTPError as e:
            print(e)
        except URLError as f:
            print('The server could not be reached')
        else:
            return bs

    def getTags(self, url, tag, attribute):
        try:
            html_code = self.getSiteHtml(url)
            heading_list_alt = html_code.find_all(tag, attribute)
        except HTTPError as e:
            print(e)
        except URLError as f:
            print('The server could not be reached')
        else:
            return heading_list_alt

    def getTag(self, url, tag, attribute):
        try:
            html_code = self.getSiteHtml(url)
            heading = html_code.find(tag, attribute)
        except HTTPError as e:
            print(e)
        except URLError as f:
            print('The server could not be reached')
        else:
            return heading

    def getEmails(self, url):
        html_code = self.getSiteHtml(url)
        emails = [x.strip(' \n') for x in html_code.find_all(text=self.email_format)]
        return (["None"] if self.isEmpty(emails) == True else emails)

    def getPhoneNumbers(self, url):
        html_code = self.getSiteHtml(url)
        numbers = [x.strip(' \n') for x  in html_code.find_all(text=self.number_format)]
        return (["None"] if self.isEmpty(numbers) == True else numbers)

    def getLinks(self, url):
        html_code = self.getSiteHtml(url)
        links = [x.attrs['href'] for x in html_code.find_all((lambda tag: self.hasHref(tag.attrs)))]
        return (["None"] if self.isEmpty(links) == True else links)

    def getParents(self, tag, attribute,url):
        html_code = self.getSiteHtml(url)
        return [x for x in html_code.find(tag, attribute).parents]

    def getNextSiblings(self, tag, attribute, url):
        html_code = self.getSiteHtml(url)
        return [x for x in html_code.find(tag, attribute).next_siblings]

    def getPreviousSiblings(self, tag, attribute, url):
        html_code = self.getSiteHtml(url)
        return [x for x in html_code.find(tag, attribute).previous_siblings]

    '''
    Boolean methods
    '''
    def isEmpty(self, some_list):
        return (True if len(some_list) == 0 else False)

    def hasHref(self, attribute_list):
        bool = False
        for i in attribute_list:
            if i == 'href':
                bool = True
                break
        return bool

    '''
    Other methods
    '''
    def numTags(self, html_code):
        count = 0
        for i in html_code:
            count += 1
        return count

    '''
    Test methods
    '''
    def execFunc(self, function, param_one, param_two):
        return function(param_one, param_two)

    def valid_links(self, link):
        req = requests.get(link)
        if (req.status_code == '200'):
            print('HTTP request successful')

    '''
    Redundant methods
    '''
    def getNextSibling(self, tag, attribute, url):
        html_code = self.getSiteHtml(url)
        return html_code.find(tag, attribute).next_sibling

    def getPreviousSibling(self, tag,attribute,url):
        html_code = self.getSiteHtml(url)
        return html_code.find(tag, attribute).previous_sibling

    '''
    Menu needs to be completed
    '''

    def menu(self):
        print('1. Retrieve HTML Code\n')
        print('2. Retrieve tags of a specified type\n')
        print('3. Retrieve links\n')
        print('4. Retrieve emails\n')
        print('5. Retrieve phone numbers\n')
        print('6. Exit')

'''

Personal Cheat Sheet:

html_code = BeautifulSoup(urlopen(url), 'html.parser') --> returns the html code of a website

tag = html_code.{tag type} --> returns only the first html code block that is the specified tag type

tag_list = html_code.find_all(tag, attributes, recursive, text, limit, keywords) --> returns a list of all the specified tags
- tag => tag type (e.x. 'h1', 'span', etc)
- attributes => the specific attributes of a tag (e.x. {class: {more attributes}}). To add multiple attributes: {attribute1: {value}, attribute2: {value}, ...}
- recursive => defaulted to true
- text => specific text that appears on a tag line (e.x. text= 'some string')
- limit => how many times do you want this method to grab the specific tag?
- keywords => select tags that contain a particular attribute or set of attributes (e.x. id='title', class_=text)

- Note: the attribute tag is an 'or' filter meaning that whatever attribute you select to find, it will find all of the attributes. To
filter these attributes, a keyword must be used. 

for name in  tag_list:
    print(name.get_text()) --> get_text() strips the html format and only returns the text value of each tag

children = html_code.find(tag, attribute, ...).children --> returns the list of children of the specified tag     

nextSiblings = html_code.find(tag,attribute, ...).{specific_tag}.next_siblings --> returns the list of next siblings of the specified tag
nextSibling = html_code.find(tag,attribute, ...).{specific_tag}.next_sibling --> returns only one sibling

previousSiblings = html_code.find(tag,attribute, ...).{specific_tag}.previous_siblings --> returns the list of next siblings of the specified tag
previousSibling = html_code.find(tag,attribute, ...).{specific_tag}.previous_sibling --> returns only one sibling

parents = html_code.find(tag, attribute, ...).{specific tag}.parents --> returns the list of parents   
parent = html_code.find(tag, attribute, ...).{specific tag}.parent --> returns a single parent tag

tag.attrs --> returns the attributes of a tag in the form of a dictionary

some_tag = html_code.find_all(lamda tag: {some condition with a tag argument}) --> convenient way of accessing tags only through boolean conditions

'''
