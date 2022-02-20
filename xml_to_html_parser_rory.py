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


# scrape subsection text from USC
def getUSCsubsection(ref_soup, subsection):
    for subsection_element in ref_soup.find_all('div'):
        if subsection_element.find('a'):
            if subsection_element.a.has_attr('name'): 
                if (subsection_element.a['name'] == subsection):
                    return subsection_element

# scrape subsection text from CFR
def getCFRsubsection(ref_soup, subsection):
    for subsection_element in ref_soup.find_all('p'):
        if subsection_element.find('span'):
            if subsection_element.span.has_attr('id'): 
                if (subsection_element.span['id'] == subsection):
                    return subsection_element


def getExternalLink(ref_tag):
    ref_tags = ref_tag.split('/')
    doc = ref_tags[2]
    title = ref_tags[3][1:]
    section = ref_tags[4][1:]

    # get URL
    if (doc == 'usc'):
        url = 'https://www.law.cornell.edu/uscode/text/%s/%s' % (title, section)
    elif (doc == 'cfr'):
        url = 'https://www.law.cornell.edu/cfr/text/%s/%s' % (title, section)

    # need to decide whether we just want a url or scraping text
    # if no subsection is listed, just return link
    if len(ref_tags) < 6:
        return url

    # this will indicate the div element to grab
    subsection = ref_tags[5]
    for tag in ref_tags[6:]:
        subsection += '_'
        subsection += tag

    # pull text from law.cornell.edu/uscode
    page = requests.get(url)
    ref_soup = BeautifulSoup(page.content, 'html.parser')

    html_scrape = ''
    if (doc == 'usc'):
        html_scrape = getUSCsubsection(ref_soup, subsection)
    elif (doc == 'cfr'):
        html_scrape = getCFRsubsection(ref_soup, subsection)
    
    return html_scrape


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
                        break


# SOURCE: https://www.codegrepper.com/code-examples/whatever/save+html+to+file+jinja2
def createHTML(designators_labels):
    template = env.get_template('index_template.html')
    output_from_parsed_template = template.render(designators_labels=designators_labels)
    with open("rendered_html/test_output.html", "w") as fh:
        fh.write(output_from_parsed_template)

create_Arrays()
# findTocLinks()
createHTML(designators_labels)

print(getExternalLink('/us/cfr/t42/s412.622/a/3/ii'))
# print(getExternalLink('/us/cfr/t45/s164.520'))
# print(getExternalLink('/us/usc/t29/s203/m/2/A'))
# print(getExternalLink('/us/usc/t29/s203'))

