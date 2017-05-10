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
# Get System Argument
import sys

def main(argv):
  epochs = int(argv[1])
  batch_size = int(argv[2])
  data_train = np.loadtxt(argv[3], dtype='float32')
  x_train = data_train[:, 0:722]
  y_train = data_train[:, -10:]

  data_test = np.loadtxt(argv[4], dtype='float32')
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
  model.add(Dense(10, activation='linear'))

  adam = optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999,
                         epsilon=1e-08, decay=0.0)
  model.compile(loss='mean_squared_error', optimizer=adam,
                metrics=[metrics.mean_squared_error])

  # Fit the model
  model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)

  # evaluate the model
  scores = model.evaluate(x_test, y_test)
  predict = model.predict(x_test, batch_size=batch_size)
  print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

  # write the result file
  f = open(argv[5], 'wt', encoding='utf-8')
  for i in range(len(y_test)):
    f.write(str(i + 1) + '.\n')
    f.write('real:\t' + str(y_test[i]) + '\n')
    f.write('pred:\t' + str(predict[i]) + '\n')
  f.close()

if __name__ == '__main__':
  main(sys.argv)
  