from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from difflib import get_close_matches

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:R3qNe4wbhfKi1K@localhost/diongpt'

db = SQLAlchemy(app)

class Intent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_intent_page', methods=['GET'])
def add_intent_page():
    return render_template('add_intent.html')

@app.route('/ask_page', methods=['GET'])
def ask_page():
    return render_template('ask.html')

@app.route('/add_intent', methods=['POST'])
def add_intent():
    intent_name = request.form['name']
    intent_description = request.form['description']
    new_intent = Intent(name=intent_name, description=intent_description)
    db.session.add(new_intent)
    db.session.commit()
    return redirect(url_for('add_intent'))

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.form['query']
    intents = Intent.query.all()
    responses = [intent.description for intent in intents]

    # Find close matches to the user's query
    close_matches = get_close_matches(user_query.lower(), [intent.name.lower() for intent in intents], n=7, cutoff=0.6)

    if close_matches:
        # Return the description of the closest match
        closest_match = close_matches[0]
        for intent in intents:
            if intent.name.lower() == closest_match:
                return jsonify({'response': intent.description})
    else:
        # If no close matches, return a default response
        return jsonify({'response': "I'm not sure I understand. Can you please rephrase your question?"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)