import requests
from lxml import html

# ---------------------- registration
session_requests = requests.session()
regis_url = "http://127.0.0.1:8000/en/user/registration"
result = session_requests.get(regis_url)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
registration_data = {'username': 'joshua12345',
                     'password1': 'joshua',
                     'password2': 'joshua',
                     'email': 'kagenyi2@gmail.com',
                     'csrfmiddlewaretoken': authenticity_token}
result = session_requests.post(regis_url, data = registration_data)
print(result.status_code)
