import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/Flamingo"  # Replace with the website URL
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the relevant information from the website
intents = []
for element in soup.find_all('div', {'class': 'intent'}):
    name = element.find('h2').text.strip()
    description = element.find('p').text.strip()
    intents.append({'name': name, 'description': description})