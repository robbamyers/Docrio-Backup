import requests

## URL and Payload for SF Access Token post request
url = 'https://login.salesforce.com/services/oauth2/token'
payload = {
    'port': 443,
    'method': 'POST',
    'headers': {'Content-Type': 'application/x-www-form-urlencoded'},
    'username': '',
    'password': '',
    'client_id': '',
    'client_secret': '',
    'grant_type': 'password'
}

## read in authorization values from user
##payload['username'] = input('Enter Username: ')
##payload['password'] = input('Enter Password: ')
##payload['client_id'] = input('Enter Client Id: ')
##payload['client_secret'] = input('Enter Client Secret: ')

## post request to return access toekn
r = requests.post(url, data=payload)
accessToken = r.json()['access_token']

## concatenate with proper formating for aws GET request
authorization = "bearer " + accessToken

## url
orgIdURL = 'https://2xm5rfl2q0.execute-api.us-east-2.amazonaws.com/v1/orginfo'
orgIdPayload = {
    'Authorization': authorization
}


orgIdr = requests.get(orgIdURL, headers=orgIdPayload)
print(orgIdr.json()['BucketName'])