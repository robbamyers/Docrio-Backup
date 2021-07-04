from os import access
import requests
import webbrowser
from requests.api import head
URL = 'https://login.salesforce.com/services/oauth2/token'

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

## read in authorization values from user
print("WELCOME TO THE DOCRIO BACKUP COMMANDLINE TOOL")
username = input('Enter Username: ')
password = input('Enter Password: ')
client_id = input('Enter Client Id: ')
client_secret = input('Enter Client Secret: ')

accessToken, instanceURL = salesforceAuthentication(username, password, client_id, client_secret)

## concatenate with proper formating for aws GET request
authorization = "Bearer " + accessToken

soqlQuery = input('Insert Your SOQL Query: ')
soqlQueryURL = instanceURL + '/services/data/v52.0/query/?q=' + soqlQuery
soqlQueryPayload = {
    'Authorization': authorization,
}

r = requests.get(soqlQueryURL, headers=soqlQueryPayload)


## url
orgIdURL = 'https://2xm5rfl2q0.execute-api.us-east-2.amazonaws.com/v1/orginfo'
orgIdPayload = {
    'Authorization': authorization,
}
r = requests.get(orgIdURL, headers=orgIdPayload)


filesPayload = {
    'accept': 'application/json',
    'Authorization': authorization,
}
r = requests.get('https://api.673389652915.genesisapi.com/v1/files?Id=a1I4W00000J1ghF', headers=filesPayload)

webbrowser.open(r.json()['Records'][0]['SignedUrl'])
## SELECT+Id+FROM+Account+LIMIT+1


