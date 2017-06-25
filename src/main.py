# Numeric Python Library.
import numpy as np
# Keras metrics method
from keras import metrics
# Keras perceptron neuron layer implementation.
from keras.layers import Dense
# Keras Dropout layer implementation.
from keras.layers import Dropout
# Keras Activation Function layer implementation.
from keras.layers import Activation
# Keras Model object.
from keras.models import Sequential
# Keras Optimizer for custom user.
from keras import optimizers
# Keras Loss for custom user.
from keras import losses
# Use Function for MSE.
from sklearn.metrics import mean_squared_error
# Get System Argument.
import sys
# Use Python Math
import math
# Use K-fold
from sklearn.model_selection import KFold
# Use plot
import matplotlib.pyplot as plt

FEATURES_LEN = 772


# epochs, batch size, learning rate, k(for k-fold)
# data(include '.txt'),
# result file(exclude '.txt')
# loss history file(exclude '.txt')
def main(argv):
  epochs = int(argv[1])
  batch_size = int(argv[2])
  learning_rate = float(argv[3])
  k = int(argv[4])
  # x is features vector,
  # y is intensities vector
  features, intensities = load_data(argv[5])
  skf = KFold(n_splits=k, shuffle=True, random_state=None)

  predicts = [0] * k
  scores = [0] * k
  histories = [0] * k

  for i, (train, test) in zip(range(k), skf.split(features)):
    print('Running Fold', i + 1, '/', k)
    model = None # Clearing the NN.
    model = create_model(learning_rate)
    predicts[i], scores[i], histories[i] = train_and_evaluate(
        model, epochs, batch_size,
        features[train], intensities[train],
        features[test], intensities[test])

    write_result(argv[6], i + 1, intensities[test], predicts[i])
    write_loss_history(argv[7], i + 1, histories[i], scores[i])


def load_data(data_file):
  data = np.loadtxt(data_file, dtype='float64')
  x = data[:, 0:FEATURES_LEN]
  y = data[:, -10:]
  return x, y

def create_model(learning_rate):
  model = Sequential()
  
  model.add(Dense(FEATURES_LEN, input_dim=FEATURES_LEN,
      init='uniform', activation='relu'))
  model.add(Dense(600, init='uniform', activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(500, init='uniform', activation='relu'))
  model.add(Dense(500, init='uniform', activation='relu'))
  model.add(Dense(500, init='uniform', activation='relu'))
  model.add(Dense(500, init='uniform', activation='relu'))
  model.add(Dense(500, init='uniform', activation='relu'))
  model.add(Dense(500, init='uniform', activation='relu'))
  model.add(Dense(500, init='uniform', activation='relu'))
  model.add(Dense(500, init='uniform', activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(100, init='uniform', activation='relu'))
  model.add(Dense(10, activation='relu'))

  adam = optimizers.Adam(lr=learning_rate, beta_1=0.9, beta_2=0.999,
      epsilon=1e-08, decay=0.1)
  model.compile(loss='mean_squared_error', optimizer=adam, 
      metrics=[metrics.mean_squared_error])

  return model

# fit and evaluate here.
def train_and_evaluate(model, epochs, batch_size,
                       x_train, y_train, x_test, y_test):

  history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

  # evaluate the model
  score = model.evaluate(x_test, y_test)
  predict = model.predict(x_test, batch_size=batch_size)
  print("\n%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))

  return predict, score, history

# argv[6]
# write the result file.
def write_result(file_name, n, y, predict):
  result_file = open(file_name + '_' + str(n) + '.txt', 'wt', encoding='utf-8')
  for i in range(len(y)):
    result_file.write(str(i + 1) + '.\n')
    result_file.write('real:\t' + str(y[i]).replace('\n', '') + '\n')
    result_file.write('pred:\t' + str(predict[i]).replace('\n', '') + '\n')
  result_file.close()

# argv[7]
# write the loss history file.
def write_loss_history(file_name, n, history, score):
  history_file = open(file_name + '_' + str(n) + '.txt', 'wt', encoding='utf-8')
  loss_history = history.history['loss']
  history_file.write('train error history\n')
  for loss in loss_history:
    history_file.write(str(np.sqrt(loss)) + '\n')
  history_file.write('\ntest error\n')
  history_file.write(str(np.sqrt(score[1])) + '\n')
  history_file.close()

"""
# TODO: merge to write_result
def write_rank(file_name, n, y, predict):
  # write the rank file
  rank_file = open(file_name + '_' + str(n) + '.txt', 'wt', encoding='utf-8')
  for i in range(len(y)):
    rank_file.write(str(i + 1) + '.\n')
    rank_file.write('real rank:\t' + str(y[i]).replace('\n', '') + '\n')
    rank_file.write('pred rank:\t' + str(predict[i]).replace('\n', '') + '\n')
  rank_file.close()

# TODO: Need to modify..
def set_rank(arr):
  ranks = np.zeros(arr.shape, dtype='int')
  for i in range(len(arr)):
    ranks[i] = 10 - arr[i].argsort().argsort()
    for j in range(len(arr[i])):
      if arr[i][j] == 0:
        pass
        # ranks[i][j] = 10
  return ranks
"""

if __name__ == '__main__':
  main(sys.argv)
  