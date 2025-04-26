import numpy as np
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Helper
def build_rnn_model(input_shape=(5, 2)):
    model = Sequential()
    model.add(LSTM(64, input_shape=input_shape))
    model.add(Dense(2, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Train RNN
def train_rnn(outcomes):
    mapping = {'B': [1, 0], 'S': [0, 1]}
    X, y = [], []
    for i in range(len(outcomes) - 5):
        seq = outcomes[i:i+5]
        target = outcomes[i+5]
        X.append([mapping[o] for o in seq])
        y.append(mapping[target])
    
    X = np.array(X)
    y = np.array(y)

    model = build_rnn_model()
    model.fit(X, y, epochs=10, batch_size=32, verbose=1)
    model.save('model/rnn_model.h5')

# Train Markov
def train_markov(outcomes):
    matrix = {}
    for i in range(len(outcomes) - 5):
        seq = ''.join(outcomes[i:i+5])
        next_outcome = outcomes[i+5]
        if seq not in matrix:
            matrix[seq] = {'B': 0, 'S': 0}
        matrix[seq][next_outcome] += 1

    # Normalize
    for seq in matrix:
        total = matrix[seq]['B'] + matrix[seq]['S']
        matrix[seq]['B'] /= total
        matrix[seq]['S'] /= total

    with open('model/markov_matrix.pkl', 'wb') as f:
        pickle.dump(matrix, f)
