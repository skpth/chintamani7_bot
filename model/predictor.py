import numpy as np
import random
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# RNN Model
def build_rnn_model(input_shape=(5, 2)):
    model = Sequential()
    model.add(LSTM(64, input_shape=input_shape))
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Load or Initialize Models
try:
    rnn_model = build_rnn_model()
    rnn_model.load_weights('model/rnn_model.h5')
except:
    rnn_model = build_rnn_model()

try:
    with open('model/markov_matrix.pkl', 'rb') as f:
        markov_matrix = pickle.load(f)
except:
    markov_matrix = {}

# Prediction Functions
def predict_next(last_5_outcomes):
    rnn_pred = predict_rnn(last_5_outcomes)
    markov_pred = predict_markov(last_5_outcomes)
    
    if rnn_pred == markov_pred:
        return rnn_pred
    else:
        return rnn_pred  # Ya weighted voting, abhi ke liye rnn

def predict_rnn(last_5_outcomes):
    mapping = {'B': [1, 0], 'S': [0, 1]}
    X = np.array([mapping[o] for o in last_5_outcomes]).reshape(1, 5, 2)
    prediction = rnn_model.predict(X, verbose=0)
    return 'B' if prediction[0][0] > prediction[0][1] else 'S'

def predict_markov(last_5_outcomes):
    seq = ''.join(last_5_outcomes)
    probs = markov_matrix.get(seq, {'B': 0.5, 'S': 0.5})
    return 'B' if probs['B'] >= probs['S'] else 'S'
