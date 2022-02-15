from jinja2 import Template, Environment, FileSystemLoader
from bs4 import BeautifulSoup

# TODO: 1.) make it work for multiple acts
#       2.) more than just table of contents
#       3.) abstract it to multiple templates instead of just index_template


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

def create_Arrays():
    referenceItems = soup.find_all('referenceItem')
    for item in referenceItems:
        designator_label = (item.designator, item.label)
        designators_labels.append(designator_label)

# SOURCE: https://www.codegrepper.com/code-examples/whatever/save+html+to+file+jinja2
def createHTML(designators_labels):
    template = env.get_template('index_template.html')
    output_from_parsed_template = template.render(designators_labels=designators_labels)
    with open("rendered_html/test_output.html", "w") as fh:
        fh.write(output_from_parsed_template)

create_Arrays()
createHTML(designators_labels)