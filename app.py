import numpy as np
import pickle
import json
from flask import Flask, request, jsonify, render_template
from flaskext.mysql import MySQL
from flask_cors import CORS
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from db_connect import DB_Connect

app=Flask(__name__)
CORS(app)

model = tf.keras.models.load_model("NextWord_Generation_EDA.h5")

db_connect= DB_Connect(app)

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
        return jsonify(
            message="Argument not provided",
            category="error",
            status=404
        )

    #print(input_text)
    seeds_out = pred(input_text, int(max_sequence_len), int(nested_list_len))
    seeds_out = sorted(seeds_out.items(), key = lambda kv: kv[1], reverse=True)
    print("no data found to store in database") if (len(seeds_out) ==0) else db_connect.store("ARJOO",input_text,seeds_out)
    return jsonify(
                message="Data fetched successfully.",
                category="success",
                data=seeds_out,
                status=200
            )

def pred(input_text, max_sequence_len, nested_list_len): 
	seed_list = [input_text] * nested_list_len
	seed_prob=[0] * nested_list_len

	for i,s in enumerate(seed_list):
		prob = 0
		for _ in range(max_sequence_len):
		
			# Convert the text into sequences
			token_list = tokenizer.texts_to_sequences([seed_list[i]])[0]

			# Pad the sequences
			token_list = pad_sequences([token_list], maxlen=5, padding='pre')
			# Get the probabilities of predicting a word
			predicted = model.predict(token_list, verbose=0)
			# Choose the next word based on the maximum probability
			indices = np.argsort(predicted[0], axis=0)[-i-1]

			# Get the actual word from the word index
			output_word = tokenizer.index_word[indices]
			seed_list[i] = seed_list[i] +  " " +  output_word
			prob = np.max(predicted[0], axis=0) + prob
        
		if (prob < 0.8):
			prob = prob + .20

		seed_prob[i] = prob/max_sequence_len
	return dict (zip(seed_list, seed_prob))
	
if __name__=='__main__':
    app.run(debug=True)


