import requests
from bs4 import BeautifulSoup, SoupStrainer
from lxml import etree
import time

def getParagraph(soup) :
  paragraph = soup.find_all('span')
  res = ''
  c = 0
  for p in paragraph :
    res += p.get_text()
    c += 1
    if c < len(paragraph) :
      res += ' '
  return res

def getContent(soup) :
  absätze = soup.find_all('div', class_='jurAbsatz')
  content = ''
  c = 0
  for absatz in absätze :
    content += absatz.get_text()
    c += 1
    if c < len(absätze) :
      content += '\n'
  return content

def getGesetz(soup) :
  title = str(soup.find('h1'))
  title = findBetween(title, '<h1>', '<br')
  return title

def findBetween(s, first, last):
  try:
    start = s.index(first) + len(first)
    end = s.index(last, start)
    return s[start:end]
  except ValueError:
    return ""

def getGesetze() :
  root = etree.parse('index.xml').getroot()
  text = root.xpath("//text()")
  gesetze = []
  for t in text :
    if 'http' in str(t) :
      gesetze += [findBetween(str(t), 'de/','/xml')]
  return gesetze

def writeIndexXML(filename) :
  url_index = 'https://www.gesetze-im-internet.de/gii-toc.xml'
  response = requests.get(url_index)
  myfile = open(filename, "w")
  myfile.write(response.text)
  return None

def getLinks(soup) :
  links = soup.find_all('a', href=True)
  res = []
  for l in links :
    res += [l['href']]
  return res

def getRelevantLinks(soup) :
  links = getLinks(soup)
  relevant_links = []
  for l in links :
    if '__' in l :
      relevant_links += [l]
  return relevant_links

if __name__ == '__main__' :

  url0 = 'https://www.gesetze-im-internet.de/'
  g = 'bgb'

  G = getGesetze()

  response = requests.get(url0 + g + '/index.html')
  soup = BeautifulSoup(response.text, 'html')
