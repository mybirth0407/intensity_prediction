# Numeric Python Library.
import numpy as np

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
# Use Cosine Similarity.
from sklearn.metrics import pairwise_distances
# Use Function for MSE.
from sklearn.metrics import mean_squared_error
# Get System Argument.
import sys
# Use Python Math
import math
# Use K-fold
from sklearn.model_selection import KFold


# epochs, batch size
# data(include '.txt'),
# result file(exclude '.txt'), rank file(exclude '.txt'),
# stats file(exclude '.txt'), k fold
def main(argv):
  epochs = int(argv[1])
  batch_size = int(argv[2])
  k = int(argv[7])
  # x is features vector,
  # y is intensities vector
  features, intensities = load_data(argv[3])
  skf = KFold(n_splits=k, shuffle=True, random_state=None)

  predicts = [0] * k
  scores = [0] * k
  history = [0] * k

  for i, (train, test) in zip(range(k), skf.split(features)):
    print(train)
    print(test)
    print('Running Fold', i + 1, '/', k)
    model = None # Clearing the NN.
    model = create_model()
    predicts[i], scores[i], history[i] = train_and_evaluate(
        model, epochs, batch_size,
        features[train], intensities[train],
        features[test], intensities[test])
    write_result(argv[4], i + 1, intensities[test], predicts[i])

  for i in range(0, k):
    write_stats(argv[6], i + 1, scores[i])


def load_data(data_file):
  data = np.loadtxt(data_file, dtype='float64')
  x = data[:, 0:722]
  y = data[:, -10:]
  return x, y

def create_model():
  # create model
  model = Sequential()
  
  model.add(Dense(722, input_dim=722, init='uniform', activation='relu'))
  model.add(Dense(600, init='uniform', activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(550, init='uniform', activation='relu'))
  model.add(Dense(500, init='uniform', activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(450, init='uniform', activation='relu'))
  model.add(Dense(400, init='uniform', activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(350, init='uniform', activation='relu'))
  model.add(Dense(300, init='uniform', activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(250, init='uniform', activation='relu'))
  model.add(Dense(200, init='uniform', activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(100, init='uniform', activation='relu'))
  model.add(Dense(50, init='uniform', activation='relu'))
  model.add(Dense(10, activation='relu'))

  adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999,
                         epsilon=1e-08, decay=0.1)
  model.compile(loss='mean_squared_error', optimizer=adam,
                metrics=[metrics.mean_squared_error])

  return model

def train_and_evaluate(model, epochs, batch_size,
                       x_train, y_train, x_test, y_test):

  # fit and evaluate here.
  history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

  # evaluate the model
  scores = model.evaluate(x_test, y_test)
  predicts = model.predict(x_test, batch_size=batch_size)
  print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

  return predicts, scores, history

# argv[4]
def write_result(file_name, n, y, predict):
  # write the result file
  result_file = open(file_name + '_' + str(n) + '.txt', 'wt', encoding='utf-8')
  for i in range(len(y)):
    result_file.write(str(i + 1) + '.\n')
    result_file.write('real:\t' + str(y[i]).replace('\n', '') + '\n')
    result_file.write('pred:\t' + str(predict[i]).replace('\n', '') + '\n')
  result_file.close()

# argv[5]
# TODO: merge to write_result
def write_rank(file_name, n, y, predict):
  # write the rank file
  rank_file = open(file_name + '_' + str(n) + '.txt', 'wt', encoding='utf-8')
  for i in range(len(y)):
    rank_file.write(str(i + 1) + '.\n')
    rank_file.write('real rank:\t' + str(y[i]).replace('\n', '') + '\n')
    rank_file.write('pred rank:\t' + str(predict[i]).replace('\n', '') + '\n')
  rank_file.close()

# argv[6]
def write_stats(file_name, score):
  stats_file = open(file_name + '_' + str(n) + '.txt', 'wt', encoding='utf-8')
  stats_file.write('test error\n')
  stats_file.write(str(np.sqrt(score[1])) + '\n')
  stats_file.close()

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


if __name__ == '__main__':
  main(sys.argv)
  