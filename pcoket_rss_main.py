
# Prompt - how do i write python code that authenticates with pocket

import requests

def authenticate_with_pocket(consumer_key, redirect_uri):
    request_token_url = 'https://getpocket.com/v3/oauth/request'
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'X-Accept': 'application/x-www-form-urlencoded'}
    data = {'consumer_key': consumer_key, 'redirect_uri': redirect_uri}
    request_token_response = requests.post(request_token_url, headers=headers, data=data)
    request_token = request_token_response.text.split('=')[1]
    authorize_url = f'https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri={redirect_uri}'
    print(f'Go to the following URL in your browser: {authorize_url}')
    print('After you authorize the app, you will be redirected to a URL like: ' + redirect_uri + '?code=XXXXXX')
    pocket_code = input('Enter the code parameter from the URL: ')
    access_token_url = 'https://getpocket.com/v3/oauth/authorize'
    headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'X-Accept': 'application/x-www-form-urlencoded'}
    data = {'consumer_key': consumer_key, 'code': pocket_code}
    access_token_response = requests.post(access_token_url, headers=headers, data=data)
    access_token = access_token_response.text.split('=')[1]
    return access_token

if __name__ == '__main__':
    consumer_key = 'YOUR_CONSUMER_KEY'
    redirect_uri = 'YOUR_REDIRECT_URI'
    access_token = authenticate_with_pocket(consumer_key, redirect_uri)
    print(f'Your access token: {access_token}')