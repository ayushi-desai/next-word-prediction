import numpy as np
import pickle
import pandas as pd
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf


app=Flask(__name__)

model = tf.keras.models.load_model("NextWord_Generation_EDA.h5")

# loading
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
    
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=["POST"])
def predict():
    """
    For rendering results on HTML GUI
    """
    seeds_out = {} 
    seeds = request.args.get("value")
    seeds_out = pred(seeds)	
    return seeds_out


def pred(seed_text): 
    next_words = 5		
    for _ in range(next_words):
        # Convert the text into sequences
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        # Pad the sequences
        token_list = pad_sequences([token_list], maxlen=5, padding='pre')
        # Get the probabilities of predicting a word
        predicted = model.predict(token_list, verbose=0)
        # Choose the next word based on the maximum probability
        predicted = np.argmax(predicted, axis=-1).item()
        # Get the actual word from the word index
        output_word = tokenizer.index_word[predicted]
        # Append to the current text
        seed_text += " " + output_word

    return seed_text
	
if __name__=='__main__':
    app.run()