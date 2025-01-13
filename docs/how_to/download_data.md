# Downloading data

## Download a JSON file from GUI

To download a JSON file with the data of the ion you have uploaded, follow the steps below:

<iframe src="https://scribehow.com/shared/Downlaod_an_ion_file_in_your_own_upload__r6kSVRioQYC7qH3S4eXlbA" width="100%" height="640" allowfullscreen frameborder="0"></iframe>

<!-- ## Use the API

```py
import requests

def get_authentication_token(nomad_url, username, password):
    '''Get the token for accessing your NOMAD unpublished uploads remotely'''
    try:
        response = requests.get(
            nomad_url + 'auth/token', params=dict(username=username, password=password), timeout=10)
        token = response.json().get('access_token')
        if token:
            return token

        print('response is missing token: ')
        print(response.json())
        return
    except Exception:
        print('something went wrong trying to get authentication token')
        return

def get_archive(nomad_url, token, upload_id, entry_id):
    '''Get an archive'''
    try:
        response = requests.post(
            nomad_url+f'uploads/{upload_id}/archive/{entry_id}',
            headers={
                'Authorization': f'Bearer {token}', 
                'Accept': 'application/json',
            },
            timeout=30,
        )
        return response
    except Exception:
        print('something went wrong trying to get the entry' entry_id)
        return
```

```py
username = 'nomad_email@affiliation.edu'
password = 'password'
nomad_url = 'https://nomad-lab.eu/prod/v1/api/v1/'

token = get_authentication_token(nomad_url, username, password)

-->