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

# Peraring dataset
# Imports csv into pandas DataFrame object.
dataset = np.loadtxt('./train_test.txt', dtype='float64')
# split into input (X) and output (Y) variables
x_train = dataset[:, 0:722]
y_train = dataset[:, -10:]


test_dataset = np.loadtxt('./02CompRef_P5_VU_11_2_0.01.txt', dtype='float64')
x_test = test_dataset[:, 0:722]
y_test = test_dataset[:, -10:]

# create model
model = Sequential()

model.add(Dense(722, input_dim=722, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(182, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(45, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(10, activation='linear'))

# Compile model
model.compile(loss='mean_squared_error', optimizer='adam',
              metrics=[metrics.mean_squared_error])
# Fit the model
model.fit(x_train, y_train, epochs=2, batch_size=32)

# evaluate the model
scores = model.evaluate(x_test, y_test)
predict = model.predict(x_test, batch_size=32)
print("\n%s: %.5f%%" % (model.metrics_names[1], scores[1] * 100))

# write the result file
f = open('result.txt', 'wt', encoding='utf-8')
for i in range(len(y_test)):
  f.write(str(i + 1) + '.\n')
  f.write('real:\t' + str(y_test[i]) + '\n')
  f.write('pred:\t' + str(predict[i]) + '\n')
f.close()

print(predict)