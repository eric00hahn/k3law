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
  title = find_between(title, '<h1>', '<br')
  return title

def find_between(s, first, last):
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
      gesetze += [find_between(str(t), 'de/','/xml')]
  return gesetze

def writeIndexXML(filename) :
  url_index = 'https://www.gesetze-im-internet.de/gii-toc.xml'
  response = requests.get(url_index)
  myfile = open(filename, "w")
  myfile.write(response.text)
  return None

def getNumberOfParagraphs(soup) :
  paragraphen = soup.find_all('a')
  content = ''
  for p in paragraphen :
      content += p.text
  result = [e for e in re.split("[^0-9]", content) if e != '']
  if len(result) == 0 :
    return 0
  else :
    return max(map(int, result))

def getLinks(soup) :
  links = soup.find_all('a', href=True)
  res = []
  for l in links :
    res += [l['href']]
  return res

if __name__ == '__main__' :

  url0 = 'https://www.gesetze-im-internet.de/'
  g = 'parkettlmstrv'

  G = getGesetze()

  response = requests.get(url0 + 'tfg' + '/index.html')
  soup = BeautifulSoup(response.text, 'html')

  links = getLinks(soup)
  print(links)
