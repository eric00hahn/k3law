import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re

def findBetween(s, first, last):
  try:
    start = s.index(first) + len(first)
    end = s.index(last, start)
    return s[start:end]
  except ValueError:
    return ''

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

def getGesetzestitel(soup) :
  title = str(soup.find('h1'))
  title = findBetween(title, '<h1>', '<br')
  return title

def getGesetze(xml_filename) :
  root = etree.parse(xml_filename).getroot()
  text = root.xpath('//text()')
  gesetze = []
  for t in text :
    if 'http' in str(t) :
      gesetze += [findBetween(str(t), 'de/','/xml')]
  return gesetze

def writeIndexXML(filename) :
  url_index = 'https://www.gesetze-im-internet.de/gii-toc.xml'
  response = requests.get(url_index)
  myfile = open(filename, 'w')
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

def appendToDictionary(dictionary, soup, g) :
  gesetzestitel = getGesetzestitel(soup)
  paragraphentitel = getParagraph(soup)
  paragraph = getContent(soup)

  if len(paragraph) > 2 :
    paragraphnummer = re.search(r'\d+', paragraphentitel).group()
    dictionary['gesetze'].append({'gesetzestitel' : gesetzestitel,
                                  'gesetzeskürzel' : g,
                                  'paragraphtitel' : paragraphentitel,
                                  'paragraphnummer' : paragraphnummer,
                                  'paragraph' : paragraph
                                })
  return None

if __name__ == '__main__' :

  url0 = 'https://www.gesetze-im-internet.de/'

  bund = {}
  bund['gesetze'] = []

  G = getGesetze('index.xml')
  counter = 1
  for g in G :
    print(counter, g)
    counter += 1

    response = requests.get(url0 + g + '/index.html')
    index_soup = BeautifulSoup(response.text, 'html')

    for l in getRelevantLinks(index_soup) :
      content_response = requests.get(url0 + g + '/' + l)
      content_soup = BeautifulSoup(content_response.text, 'html')
      appendToDictionary(bund, content_soup, g)

  with open('bund.json', 'w') as outfile :
    json.dump(bund, outfile)
