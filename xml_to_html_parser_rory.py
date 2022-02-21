import re
import requests
import jinja2
from jinja2 import Template, Environment, FileSystemLoader
from bs4 import BeautifulSoup


env = Environment(loader=FileSystemLoader('templates'))

act = input('What act would you like to look at?' + '\n')
act = str(act)
text_file = open('xml_files/' + act)
xml_as_string = text_file.read()

soup = BeautifulSoup(xml_as_string, "xml")
labels = []
designators = []
info = []
text = []
text_dict = {}


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
        d_l_i = (item.designator, item.label, findLinks(item.designator))
        info.append(d_l_i)

def cleanTocLabel(this_string):
    this_string.encode('utf-8')
    this_string = this_string.replace('.', '')
    this_string = this_string.replace(u"\u2014", '')
    this_string = this_string.replace(u"\u201C", '')
    this_string = this_string.replace(u"\u201D", '')
    return this_string

def findLinks(this_designator):
    label = cleanTocLabel(this_designator.text)

    label_split = label.split()
    if (len(label_split) >= 2):
        label_value = label_split[1]
    else:
        label_value = label_split[0]

    for section in soup.find_all('section'):
        if section.find('num'):
            if section.num.has_attr('value'):
                if (section.num['value'] == label_value):
                    if (section.has_attr('identifier')):
                        text.append(section.text)
                        i = section['identifier']
                        i_split = i.split('/')
                        sec = i_split[len(i_split)-1]
                        return sec

# SOURCE: https://www.codegrepper.com/code-examples/whatever/save+html+to+file+jinja2
def createHTML(info):
    template1 = env.get_template('index_template.html')
    output_from_parsed_template1 = template1.render(info=info)
    with open("rendered_html/test_output.html", "w") as fh:
        fh.write(output_from_parsed_template1)

def createSectionHTML(info):
    template2 = env.get_template('section_template.html')
    index=0
    for d, l, i in info:
        if i != None and index < len(text):
            output_from_parsed_template2 = template2.render(sec=i, text=text[index])


            with open("rendered_html/section_" + str(i) + ".html", "w") as fh:
                fh.write(output_from_parsed_template2)
                fh.close()
            index += 1

create_Arrays()
createHTML(info)
createSectionHTML(info)
