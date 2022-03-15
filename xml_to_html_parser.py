import re
#import requests
import jinja2
from jinja2 import Template, Environment, FileSystemLoader
from bs4 import BeautifulSoup


env = Environment(loader=FileSystemLoader('templates'))

act = input('What act would you like to look at?' + '\n')
act = str(act)
text_file = open('xml_files/' + act, errors = 'ignore')
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


def getExternalURL(ref_tag):
    ref_tags = ref_tag.split('/')
    doc = ref_tags[2]
    title = ref_tags[3][1:]
    section = ref_tags[4][1:]

    # get URL
    if (doc == 'usc'):
        # url = 'https://www.law.cornell.edu/uscode/text/%s/%s' % (title, section) # cornell link
        url = 'https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title%s-section%s&num=0&edition=prelim' % (title, section)
    elif (doc == 'cfr'):
        url = 'https://www.law.cornell.edu/cfr/text/%s/%s' % (title, section)

    # need to decide whether we just want a url or scraping text
    # if no subsection is listed, just return link
    return url

    # if len(ref_tags) < 6:
    #     return url

    # # this will indicate the div element to grab
    # subsection = ref_tags[5]
    # for tag in ref_tags[6:]:
    #     subsection += '_'
    #     subsection += tag

    # # pull text from law.cornell.edu/uscode
    # page = requests.get(url)
    # ref_soup = BeautifulSoup(page.content, 'html.parser')

    # html_scrape = ''
    # if (doc == 'usc'):
    #     html_scrape = getUSCsubsection(ref_soup, subsection)
    # elif (doc == 'cfr'):
    #     html_scrape = getCFRsubsection(ref_soup, subsection)
    
    # return html_scrape

def findExternalLinks():
    for ref in soup.find_all('ref'):
        if ref.has_attr('href'):
            current_href = ref['href'].split('/')
            if (len(current_href) > 4):
                doc = current_href[2] 
                if (doc == 'usc' or doc == 'cfr'):
                    a_tag = soup.new_tag('a')
                    a_tag['href'] = getExternalURL(ref['href'])
                    a_tag['target'] = '_blank'
                    ref.wrap(a_tag)

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
                        text.append(section)
                        i = section['identifier']
                        i_split = i.split('/')
                        sec = i_split[len(i_split)-1]
                        return sec


def addButtons():
    # <button type="button" class="collapsible"></button>
    for num in soup.find_all('num'):
        button_tag = soup.new_tag('button')
        button_tag['type']='button'
        button_tag['class']='collapsible'
        button_tag.string = ''

        # temp_tag = soup.new_tag('temp')
        # num.insert_before(temp_tag)
        # temp_tag.wrap(button_tag)
        # temp_tag.extract()

        num.insert_before(button_tag)

def getCrumbs(this_identifier):
    # d = division
    # t = title
    # st = subtitle
    # pt = part
    # spt = subpart
    # s = section
    crumbs = []

    for i in this_identifier.split('/'):
        this_crumb = ''

        if (i.find('d', 0, 1) == 0):
            this_crumb = 'Division %s' % i[1:]
            crumbs.append(this_crumb)

        elif (i.find('t', 0, 1) == 0):
            this_crumb = 'Title %s' % i[1:]
            crumbs.append(this_crumb)

        elif (i.find('st', 0, 2) == 0):
            this_crumb = 'Subtitle %s' % i[2:]
            crumbs.append(this_crumb)

        elif (i.find('pt', 0, 2) == 0):
            this_crumb = 'Part %s' % i[2:]
            crumbs.append(this_crumb)

        elif (i.find('spt', 0, 3) == 0):
            this_crumb = 'Subpart %s' % i[3:]
            crumbs.append(this_crumb)

        elif (i.find('s', 0, 3) == 0):
            this_crumb = 'Section %s' % i[1:]
            crumbs.append(this_crumb)
             
    return crumbs


# SOURCE: https://www.codegrepper.com/code-examples/whatever/save+html+to+file+jinja2
def createHTML(info):
    template1 = env.get_template('index_template.html')
    output_from_parsed_template1 = template1.render(info=info)
    with open("rendered_html/index.html", "w") as fh:
        fh.write(output_from_parsed_template1)

def createSectionHTML(info):
    template2 = env.get_template('section_template.html')
    index=0

    j = 0

    for d, l, i in info:
        if i != None and index < len(text):
            # print(text[index]['identifier'])
            # getCrumbs(text[index]['identifier'])

            secprev = 'None'
            secnext = 'None'
            if (j > 0):
                secprev = info[j-1][2]

            if (j < (len(info)-1) ):
                secnext = info[j+1][2]

            # TODO: need to handle none cases

            output_from_parsed_template2 = template2.render(sec=i, text=text[index], crumbs=getCrumbs(text[index]['identifier']), ps=secprev, ns=secnext)

            with open("rendered_html/section_" + str(i) + ".html", "w") as fh:
                fh.write(output_from_parsed_template2)
                fh.close()
                
            index += 1

        j+=1

findExternalLinks()
# addButtons()
create_Arrays()
createHTML(info)
createSectionHTML(info)
