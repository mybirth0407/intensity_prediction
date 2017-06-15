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
# Keras Optimizer for custom user
from keras import optimizers
# Keras Loss for custom user
from keras import losses
# Use Cosine Similarity
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
# Use Function for MSE
from sklearn.metrics import mean_squared_error
# Get System Argument
import sys
import math

# epochs, batch size, train data, test data, result file, rank file, stats file
def main(argv):
  epochs = int(argv[1])
  batch_size = int(argv[2])
  data_train = np.loadtxt(argv[3], dtype='float64')
  x_train = data_train[:, 0:722]
  y_train = data_train[:, -10:]

  data_test = np.loadtxt(argv[4], dtype='float64')
  x_test = data_test[:, 0:722]
  y_test = data_test[:, -10:]

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

  # fit the model
  model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

  # evaluate the model
  scores = model.evaluate(x_test, y_test)
  predict = model.predict(x_test, batch_size=batch_size)
  print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

  # get rank vector
  y_rank = set_rank(y_test)
  predict_rank = set_rank(predict)

  # write the result file
  result_file = open(argv[5], 'wt', encoding='utf-8')
  for i in range(len(y_test)):
    result_file.write(str(i + 1) + '.\n')
    result_file.write('real:\t' + str(y_test[i]) + '\n')
    result_file.write('pred:\t' + str(predict[i]) + '\n')
  result_file.close()

  # write the rank file
  rank_file = open(argv[6], 'wt', encoding='utf-8')
  for i in range(len(y_rank)):
    rank_file.write(str(i + 1) + '.\n')
    rank_file.write('real rank:\t' + str(y_rank[i]) + '\n')
    rank_file.write('pred rank:\t' + str(predict_rank[i]) + '\n')
  rank_file.close()

  # full predction value variance
  full_variance = np.var(predict - y_test)
  # full predction value rmses
  full_rmse = np.sqrt(mean_squared_error(y_test, predict))

  # b1, b2, ..., b10 error variance
  variance = np.zeros((10,), dtype='float64')
  # b1, b2, ..., b10 error rmse
  rmses = np.zeros((10,), dtype='float64')
  for i in range(0, 10):
    variance[i] = np.var(predict[:, i] - y_test[:, i])
    rmses[i] = np.sqrt(mean_squared_error(predict[:, i], y_test[:, i]))

  # rank info
  rank_full_rmse = np.sqrt(mean_squared_error(y_rank, predict_rank))
  rank_full_variance = np.var(predict_rank - y_rank)
  # b1, b2, ..., b10 rank error variance
  rank_variance = np.zeros((10,), dtype='float64')
  # b1, b2, ..., b10 rank error rmse
  rank_rmse = np.zeros((10,), dtype='float64')

  for i in range(0, 10):
    rank_variance[i] = np.var(predict_rank[:, i] - y_rank[:, i])
    rank_rmse[i] = np.sqrt(mean_squared_error(predict_rank[:, i], y_rank[:, i]))

  stats_file = open(argv[7], 'wt', encoding='utf-8')
  stats_file.write('test error\n')
  stats_file.write(str(np.sqrt(scores[1])) + '\n')
  stats_file.write('full variance\n')
  stats_file.write(str(full_variance) + '\n')
  stats_file.write('full rmses\n')
  stats_file.write(str(full_rmse) + '\n')
  
  stats_file.write('variance\n')
  stats_file.write(str(variance) + '\n')
  stats_file.write('rmses\n')
  stats_file.write(str(rmses) + '\n')

  stats_file.write('rank full variance\n')
  stats_file.write(str(rank_full_variance) + '\n')
  stats_file.write('rank full rmse\n')
  stats_file.write(str(rank_full_rmse) + '\n')

  stats_file.write('rank variance\n')
  stats_file.write(str(rank_variance) + '\n')
  stats_file.write('rank rmse\n')
  stats_file.write(str(rank_rmse) + '\n')

  stats_file.write('cosine similiarity\n')
  stats_file.write(str(np.mean(cos_sim(y_test, predict), axis=0)) + '\n')
  stats_file.close()


def set_rank(arr):
  ranks = np.zeros(arr.shape, dtype='int')
  for i in range(len(arr)):
    ranks[i] = 10 - arr[i].argsort().argsort()
    for j in range(len(arr[i])):
      if arr[i][j] == 0:
        pass
        # ranks[i][j] = 10
  return ranks

def cos_sim(pred, real):
  cos_sim = np.zeros(real.shape[0], dtype='float64')
  for i in range(len(real)):
    cos_sim[i] = 1 - cosine(pred[i], real[i])
    if math.isnan(cos_sim[i]):
      pass
  return cos_sim

if __name__ == '__main__':
  main(sys.argv)
  