from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:R3qNe4wbhfKi1K@localhost/diongpt'
db = SQLAlchemy(app)

class Intent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

def scrape_data(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    intents = []
    intent_elements = soup.find_all('div', {'class': 'intent'})
    for element in intent_elements:
        name = element.find('h2').text.strip()
        description = element.find('p').text.strip()
        intents.append({'name': name, 'description': description})
    return intents

url = 'https://help.instagram.com/424737657584573/?helpref=related_articles'  # Replace with the URL of the website you want to scrape
intents = scrape_data(url)

with app.app_context():
    for intent in intents:
        try:
            new_intent = Intent(name=intent['name'], description=intent['description'])
            db.session.add(new_intent)
            db.session.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")