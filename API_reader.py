import requests
import json

api_url = 'https://cat-fact.herokuapp.com/facts/random'
api_response = requests.get(api_url)
api_response.content
api_data = json.loads(api_response.content)
type(api_data)
len(api_data)
api_data[2]
api_data[0]
