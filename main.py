# Must include the following
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re

def getTitle(url):
    try:
        # Default
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
        page_title = bs.title
    except HTTPError as e:
        print(e)
    except URLError as f:
        print('Server non-existent!')
    except AttributeError as g:
        print('Tag was not found')
    else:
        return page_title


def getSiteHtml(url):
    try:
        # Default
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
    except HTTPError as e:
        print(e)
    except URLError as f:
        print('The server could not be reached')
    else:
        return bs

def getTags(url, tag, attribute):
    try:
        # Default
        html_code = getSiteHtml(url)

        # Best method
        heading_list_alt = html_code.find_all(tag, attribute)
    except HTTPError as e:
        print(e)
    except URLError as f:
        print('The server could not be reached')
    else:
        return heading_list_alt

def getTag(url, tag, attribute):
    try:
        # Default
        html_code = getSiteHtml(url)
        # Best method
        heading = html_code.find(tag, attribute)
    except HTTPError as e:
        print(e)
    except URLError as f:
        print('The server could not be reached')
    else:
        return heading

def getEmails(url):
    html_code = getSiteHtml(url)
    email_format = re.compile('[A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net)')
    emails = [x.strip(' \n') for x in html_code.find_all(text=email_format)]
    return emails

def getPhoneNumbers(url):
    html_code = getSiteHtml(url)
    number_format = re.compile('[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]')
    numbers = [x.strip(' \n') for x  in html_code.find_all(text=number_format)]
    return numbers

def getLinks(url):
    html_code = getSiteHtml(url)
    return html_code.find_all(lambda tag: hasHref(tag.attrs))

def hasHref(attribute_list):
    bool = False
    for i in attribute_list:
        if i == 'href':
            bool = True
            break
    return bool

def getParents(tag, attribute,url):
    html_code = getSiteHtml(url)
    return [x for x in html_code.find(tag, attribute).parents]

def getNextSiblings(tag, attribute, url):
    html_code = getSiteHtml(url)
    return [x for x in html_code.find(tag, attribute).next_siblings]

def getPreviousSiblings(tag,attribute,url):
    html_code = getSiteHtml(url)
    return [x for x in html_code.find(tag, attribute).previous_siblings]

'''
Redundant methods
'''

def getNextSibling(tag, attribute, url):
    html_code = getSiteHtml(url)
    return html_code.find(tag, attribute).next_sibling

def getPreviousSibling(tag,attribute,url):
    html_code = getSiteHtml(url)
    return html_code.find(tag, attribute).previous_sibling

def main():
    test_url_one = 'https://en.wikipedia.org/wiki/Leopard_1'
    test_url_two = 'https://www.lipsum.com/'

    email_links = getEmails(test_url_two)
    phone_links = getPhoneNumbers(test_url_two)

    url_one = getSiteHtml(test_url_one)

    lamda_tag_test = url_one.find_all(lambda tag: tag.get_text() == 'Leopard 1')


    print(getLinks(test_url_one))

if __name__ == '__main__':
    main()

'''
Cheat sheet:

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
