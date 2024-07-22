import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# importing the required modules. 
import random 
import json 
import pickle 
import numpy as np 
import nltk
from keras.models import Sequential 
from nltk.stem import WordNetLemmatizer 
from keras.layers import Dense, Activation, Dropout 
from keras.optimizers import SGD 

lemmatizer = WordNetLemmatizer() 

# reading the json.intense file 
intents = json.loads(open("intense.json").read()) 

# creating empty lists to store data 
words = [] 
classes = [] 
documents = [] 
ignore_letters = ["?", "!", ".", ","] 
for intent in intents['intents']: 
	for pattern in intent['patterns']: 
		# separating words from patterns 
		word_list = nltk.word_tokenize(pattern) 
		words.extend(word_list) # and adding them to words list 
		
		# associating patterns with respective tags 
		documents.append(((word_list), intent['tag'])) 

		# appending the tags to the class list 
		if intent['tag'] not in classes: 
			classes.append(intent['tag']) 

# storing the root words or lemma 
words = [lemmatizer.lemmatize(word) 
		for word in words if word not in ignore_letters] 
words = sorted(set(words)) 

# saving the words and classes list to binary files 
pickle.dump(words, open('words.pkl', 'wb')) 
pickle.dump(classes, open('classes.pkl', 'wb')) 

training = [] 
output_empty = [0]*len(classes) 
for document in documents: 
    bag = [] 
    word_patterns = document[0] 
    word_patterns = [lemmatizer.lemmatize( 
        word.lower()) for word in word_patterns] 
    for word in words: 
        bag.append(1) if word in word_patterns else bag.append(0) 
          
    # making a copy of the output_empty 
    output_row = list(output_empty) 
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row]) 
random.shuffle(training) 

# Find the maximum length of the sublists
max_len = max(len(item[0]) for item in training)
max_out_len = max(len(item[1]) for item in training)

# Pad the shorter lists with zeros
padded_training = []
for item in training:
    padded_bag = item[0] + [0] * (max_len - len(item[0]))
    padded_output = item[1] + [0] * (max_out_len - len(item[1]))
    padded_training.append([padded_bag, padded_output])

# Convert the lists to NumPy arrays
train_x = np.array([item[0] for item in padded_training])
train_y = np.array([item[1] for item in padded_training])

# creating a Sequential machine learning model 
from keras.layers import Input

model = Sequential() 
model.add(Input(shape=(len(train_x[0]), ))) 
model.add(Dense(128, activation='relu')) 
model.add(Dropout(0.5)) 
model.add(Dense(64, activation='relu')) 
model.add(Dropout(0.5)) 
model.add(Dense(len(train_y[0]), activation='softmax')) 

# compiling the model 
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True) 
model.compile(loss='categorical_crossentropy', 
			optimizer=sgd, metrics=['accuracy']) 

# актуиализира с нова информация
def update_intents():
    with open('intense.json', 'r') as f:
        intense_json = json.load(f)
    intents = intense_json['intents']
    return intents

    intents = update_intents()

# saving the model 
model.save("chatbotmodel.h5", list) 

# print statement to show the 
# successful training of the Chatbot model 
print("Yay!") 
