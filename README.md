# Next Word-Prediction
This Repository is intended to Develop Word Prediction system.

Implemented GloVe word embeddings with LSTM and GRU to get better result accuracy</br>

Steps to download glove embeddings:-</br>

Download GloVe word embeddings</br>
!wget http://nlp.stanford.edu/data/glove.6B.zip</br>

Unzip word embeddings and use only the top 50000 word embeddings for speed</br>
!unzip glove.6B.zip</br>

Downloading GPT-2</br>
There are three released sizes of GPT-2:

124M (default): the "small" model, 500MB on disk.</br>
355M: the "medium" model, 1.5GB on disk.</br>
774M: the "large" model, cannot currently be finetuned with Colaboratory but can be used to generate text from the pretrained model</br>
1558M: the "extra large", true model. Will not work if a K80/P4 GPU is attached to the notebook.</br>
Larger models have more knowledge, but take longer to finetune and longer to generate text. You can specify which base model to use by changing model_name in the cells below.</br>
Ex: gpt2.download_gpt2(model_name="124M")</br>

Finetune GPT-2</br>
Other optional-but-helpful parameters for `gpt2.finetune`:

restore_from: Set to `fresh` to start training from the base GPT-2, or set to `latest` to restart training from an existing checkpoint.</br>
sample_every: Number of steps to print example output</br>
print_every: Number of steps to print training progress.</br>
learning_rate:  Learning rate for the training. (default `1e-4`, can lower to `1e-5` if you have <1MB input data)</br>
run_name: subfolder within `checkpoint` to save the model. This is useful if you want to work with multiple models (will also need to specify  `run_name` when loading the model)</br>
overwrite: Set to `True` if you want to continue finetuning an existing model (w/ `restore_from='latest'`) without creating duplicate copies.</br> 

---------------

API for next word prdiction : http://127.0.0.1:5000/predict?value=I would like to ride


Task of Caching
Intended creation and deployment of code that will store the next word prediction in user cache memory.
The code will have no cache for a new word prediction, and this will be the first hit, which will be
stored in client side cache so that the next time the same word is to be predicted, it will not be a
new hit, but will instead use the cache memory to predict the word.
Progressing work on client-side caching, but a new approach is using flask api to store
the same cache in our database, which will be eliminated to improve processing speed and
time.
