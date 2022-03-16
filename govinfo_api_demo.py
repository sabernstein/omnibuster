'''quick test'''
import json
import requests

BASE_URL='https://api.govinfo.gov/'
header_key = {'X-Api-key': '3xT3giki8mkXRecDcd7fssW6R1KhhSyl51g91iF5'}

def list_collections():
    '''list the collections'''
    response = requests.get(
        BASE_URL+'collections',
        headers = header_key
        )
    collection_list=json.loads(response.text)
    print('here is a list of collection codes available from the API')
    for collection in collection_list['collections']:
        print(collection['collectionCode'])
print("This script will demonstrate basic govinfo API functionality for a simple use case using the collections and packages endpoints.")

list_collections()


start_date = input('Enter a starting date in YYYY-MM-DD format: ')


def get_packages(collection_code,sdate,billVersion='',docClass='',congress_number=''):
    '''get a list of results for a given collection'''
    response = requests.get(
        BASE_URL+'collections/'+collection_code+'/'+sdate+'T00:00:00Z?offset=0&pageSize=100&billVersion='+billVersion+'&docClass='+docClass+'&congress='+congress_number,
        # params = {'offset': '0', 'pageSize':'100'},
        headers = header_key
        )
    results=json.loads(response.text)
    print(f"total results for the {collection_code} collection: {results['count']}")
    for item in results['packages']:
        print(item['packageId'])

def package_data(package_id):
    '''request JSON summary of the package and return list of download options'''
    response = requests.get(
        BASE_URL+'packages/'+package_id+'/summary',
        headers = header_key
        )
    summary=json.loads(response.text)
    print(f"Title: {summary['title']}")
    print(f"This package was originally published on {summary['dateIssued']}")
    if summary['relatedLink']:
        print(f"There are relationships available at {summary['relatedLink']}")
        print()
    print('Available download types:')
    for link_type in summary['download']:
        print(link_type,summary['download'][link_type])
    file_type=input("Which file type do you want? ")
    link = summary['download'][file_type]

    return link

def get_file(file_link):
    '''print requested file type from package_data'''
    response = requests.get(
        file_link,
        headers = header_key
        )
    print(response.text)

collection_request = input("Enter a collection code to get a recent list of packages: ")
print('Available parameters include billVersion, docClass, congress')
filters = input("Do you want to add any additional parameters to narrow your results? [Y/N]:")
if filters.lower() == "y":
    doc_class = input("docClass: ")
    congress = input("Congress: ")
    if collection_request=="BILLS":
        bill_version = input("billVersion: ")
        get_packages(collection_request,start_date,bill_version,doc_class,congress)
    else:        
        get_packages(collection_request,start_date,'',doc_class,congress)
else:
    get_packages(collection_request, start_date)

print('------------')
package = input("Choose a package from above: ")
download=package_data(package)

get_file(download)