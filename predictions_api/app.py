import numpy as np
import pickle
from flask import Flask, request, jsonify, render_template
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
    input_text = request.args.get("value")
    max_sequence_len = request.args.get("max_sequence_len")
    nested_list_len = request.args.get("nested_list_len")
    
    if max_sequence_len is None or input_text is None or nested_list_len is None:
        return "Argument not provided"

    seeds_out = pred(input_text, int(max_sequence_len), int(nested_list_len))
    return jsonify(seeds_out)



def pred(input_text, max_sequence_len, nested_list_len): 

	seed_list = [input_text] * nested_list_len

	for _ in range(max_sequence_len):
		for i,s in enumerate(seed_list):
			# Convert the text into sequences
			token_list = tokenizer.texts_to_sequences([seed_list[i]])[0]
			
			# Pad the sequences
			token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')
			
			# Get the probabilities of predicting a word
			predicted = model.predict(token_list, verbose=0)
			# Choose the next word based on the maximum probability
			indices = np.argsort(predicted[0], axis=0)[-i-1]

			# Get the actual word from the word index
			output_word = tokenizer.index_word[indices]
			seed_list[i] = seed_list[i] + output_word

	return seed_list

	
if __name__=='__main__':
    app.run()
