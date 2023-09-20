import requests
import os

url = os.environ.get('UPDATE_URL')
token = os.environ.get('UPDATE_TOKEN')

requests.get(url,headers={'Update-Token':token})