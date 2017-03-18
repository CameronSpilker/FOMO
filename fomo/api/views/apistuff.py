# pip install requests
import requests

ret = requests.get('http://localhost:8000/api/users/1')
print(ret.json())