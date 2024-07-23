import random 
import json 
import pickle 
import numpy as np 
import nltk 
from keras.models import load_model 
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.layers import Input
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import PCA

lemmatizer = WordNetLemmatizer() 
intents = json.loads(open("templates/intense.json").read()) 
words = pickle.load(open('words.pkl', 'rb')) 
classes = pickle.load(open('classes.pkl', 'rb')) 
model = load_model('chatbotmodel.h5') 

def clean_up_sentences(sentence): 
	sentence_words = nltk.word_tokenize(sentence) 
	sentence_words = [lemmatizer.lemmatize(word) 
					for word in sentence_words] 
	return sentence_words 

def bagw(sentence): 
	sentence_words = clean_up_sentences(sentence) 
	bag = [0]*len(words) 
	for w in sentence_words: 
		for i, word in enumerate(words): 
			if word == w: 
				bag[i] = 1
	return np.array(bag) 

def predict_class(sentence):
    bow = bagw(sentence)
    pca = PCA(n_components=1)  # Set n_components to None
    bow_pca = pca.fit_transform([bow])  # Apply PCA transformation
    res = model.predict(bow_pca)[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

model = Sequential()
model.add(Input(shape=(1,)))  # Update the input layer to match the input shape
model.add(Dense(27, activation='relu'))  # Add a dense layer with 27 units
model.add(Dense(1, activation='sigmoid'))  # Add an output layer with 1 unit
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

def get_response(intents_list, intents_json): 
	tag = intents_list[0]['intent'] 
	list_of_intents = intents_json['intents'] 
	result = "" 
	for i in list_of_intents: 
		if i['tag'] == tag: 
			result = random.choice(i['responses']) 
			break
	return result 

print("Chatbot is up!") 

while True: 
	message = input("") 
	ints = predict_class(message) 
	res = get_response(ints, intents) 
	print(res) 
