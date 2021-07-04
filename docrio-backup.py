from os import access
import os
import time
import requests
import webbrowser
from requests.api import head
URL = 'https://login.salesforce.com/services/oauth2/token'
accessToken = ""

def salesforceAuthentication(username, password, client_id, client_secret):
    payload = {
    'port': 443,
    'method': 'POST',
    'headers': {'Content-Type': 'application/x-www-form-urlencoded'},
    'username': username,
    'password': password,
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'password'
    }
    r = requests.post(URL, data=payload)
    accessToken = r.json()['access_token']
    instanceURL = r.json()['instance_url']
    return accessToken, instanceURL
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
def displayHeading():
    print("-----------WELCOME TO THE DOCRIO BACKUP COMMANDLINE TOOL---------\n")
def displayMenu():
    print("1) Authorize with your Salesforce Credentials\n2) Enter a SOQL query\n3) Download file(s)")
def displayMenuWithOutAuthentication():
    print("1) Enter a SOQL query\n2) Download file(s)")

while True:
    cls()
    displayHeading()
    displayMenu()
    menuOption = input("Please enter the number for the menu option\n")

    while (menuOption == '1'):
        cls()
        displayHeading()
        username = input('Enter Salesforce Username: ')
        password = input('Enter Salesforce Password: ')
        client_id = input('Enter Client Id: ')
        client_secret = input('Enter Client Secret: ')
        accessToken, instanceURL = salesforceAuthentication(username, password, client_id, client_secret)
        authorization = "Bearer " + accessToken
        if(accessToken != ""):
            print("Authentication Successful...")
            time.sleep(5)
            cls()
            displayHeading()
        menuOption = '0'

    while(menuOption == '2'):
        while(accessToken == ''):
            cls()
            displayHeading()
            print("Please authenticate before running a SOQL Query.")
            username = input('Enter Salesforce Username: ')
            password = input('Enter Salesforce Password: ')
            client_id = input('Enter Client Id: ')
            client_secret = input('Enter Client Secret: ')
            accessToken, instanceURL = salesforceAuthentication(username, password, client_id, client_secret)
            authorization = "Bearer " + accessToken
        soqlQuery = input('Insert Your SOQL Query (be sure to include Id): ')
        formattedSoqlQuery = soqlQuery.replace(" ","+")
        print(formattedSoqlQuery)
        soqlQueryURL = instanceURL + '/services/data/v52.0/query/?q=' + formattedSoqlQuery
        soqlQueryPayload = {
            'Authorization': authorization,
        }
        r = requests.get(soqlQueryURL, headers=soqlQueryPayload)
        for i in range(r.json()['totalSize']):
            print(r.json()['records'][i]['Id']) ## Maybe don't hard code the Id
        continuation = input('Would you like to run another query? y/n: ')
        if(continuation.upper() == 'Y'):
            menuOption = '2'
        else:
            menuOption = '0'
        
    while(menuOption == '3'):
        while(accessToken == ''):
            cls()
            displayHeading()
            print("Please authenticate before downloading any files.")
            username = input('Enter Salesforce Username: ')
            password = input('Enter Salesforce Password: ')
            client_id = input('Enter Client Id: ')
            client_secret = input('Enter Client Secret: ')
            accessToken, instanceURL = salesforceAuthentication(username, password, client_id, client_secret)
            authorization = "Bearer " + accessToken
        orgIdURL = input('Please enter your Setup API URL ex. <https://2xm5rfl2q0.execute-api.us-east-2.amazonaws.com/v1/orginfo>')
        orgIdPayload = {
            'Authorization': authorization,
        }
        r = requests.get(orgIdURL, headers=orgIdPayload)
        downloadOneOrMultipleFiles = input("Would you like to download one or multiple files? Enter \"1\" for one file and \"2\" for multiple: ")
        if(downloadOneOrMultipleFiles == '1'):
            fileInfoRecordId = input('Please enter the File Info record Id: ')
            filesPayload = {
                'accept': 'application/json',
                'Authorization': authorization,
            }
            r = requests.get('https://api.673389652915.genesisapi.com/v1/files?Id=' + fileInfoRecordId, headers=filesPayload)
            print("Downloading your file...")
            webbrowser.open(r.json()['Records'][0]['SignedUrl'])
            menuOption = '0'
        elif(downloadOneOrMultipleFiles == '2'):
            fileInfoRecordIds = input('Please enter the File Info record Id: ')
            filesPayload = {
                'accept': 'application/json',
                'Authorization': authorization,
            }
            print("Downloading your files...")
            r = requests.get('https://api.673389652915.genesisapi.com/v1/files?Id=' + fileInfoRecordIds, headers=filesPayload)
            numberOfRecords = len(r.json()['Records'])
            for i in range(numberOfRecords):
                s = requests.get(r.json()['Records'][i]['SignedUrl'])
                path = "./Downloads/" + r.json()['Records'][i]['Id'] + ""
                open(path, 'wb').write(s.content)
            menuOption = '0'

