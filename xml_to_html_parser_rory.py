from jinja2 import Template, Environment, FileSystemLoader
from bs4 import BeautifulSoup
import re
import requests


env = Environment(loader=FileSystemLoader('templates'))

act = input('What act would you like to look at?' + '\n')
act = str(act)
text_file = open('xml_files/' + act)
xml_as_string = text_file.read()

soup = BeautifulSoup(xml_as_string, "xml")
labels = []
designators = []
designators_labels = []
text = []


def getUSC(usc_tag):
    URL = 'https://www.law.cornell.edu/uscode/text/29/203'
    page = requests.get(URL)
    usc_soup = BeautifulSoup(page.content, 'html.parser')
    for section in usc_soup.find_all('div'):
        if section.find('a'):
            if section.a.has_attr('name'): 
                print(section.a['name'])


def create_Arrays():
    referenceItems = soup.find_all('referenceItem')
    for item in referenceItems:
        designator_label = (item.designator, item.label)
        designators_labels.append(designator_label)

def cleanTocLabel(this_string):
    this_string.encode('utf-8')
    this_string = this_string.replace('.', '')
    this_string = this_string.replace(u"\u2014", '')
    this_string = this_string.replace(u"\u201C", '')
    this_string = this_string.replace(u"\u201D", '')
    return this_string

def findTocLinks():
    for designator_label in designators_labels:
        label = designator_label[0].text
        label = cleanTocLabel(label)
        label_value = label.split()[1]

        for section in soup.find_all('section'):
            if section.find('num'):
                if section.num.has_attr('value'):
                    if (section.num['value'] == label_value):
                        print(section['identifier'])


# SOURCE: https://www.codegrepper.com/code-examples/whatever/save+html+to+file+jinja2
def createHTML(designators_labels):
    template = env.get_template('index_template.html')
    output_from_parsed_template = template.render(designators_labels=designators_labels)
    with open("rendered_html/test_output.html", "w") as fh:
        fh.write(output_from_parsed_template)

create_Arrays()
# findTocLinks()
createHTML(designators_labels)

getUSC('/us/usc/t29/s203/m/2/A')