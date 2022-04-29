import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D

def singleFeature(dataVec):
    M = np.shape(dataVec)[0]
    N = np.shape(dataVec)[1]

    # k-fold cross validation
    k = 3
    in_len = 10
    out_len = 1
    stride = int(np.floor(N / k))
    mse = 0
    mse_b = 0
    momentum_correct = 0
    guesses = 0

    for i in range(k):
        # split into training and testing sequences
        data_train = np.hstack((dataVec[:, 0 : i * stride ], dataVec[:, (i + 1) * stride :]))
        data_test = dataVec[:, i * stride : (i + 1) * stride]

        # decompose sequences into samples using moving window
        X_train = [] 
        y_train = []

        N_train = np.shape(data_train)[1]
        for m in range(M):
            for n in range(N_train - (in_len + out_len)):
                X_train.append(data_train[m, n : n + in_len])
                y_train.append(data_train[m, n + in_len : n + in_len + out_len])
        
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        num_features = 1
        X_train = np.reshape(X_train, (np.shape(X_train)[0], np.shape(X_train)[1], num_features))

        model = Sequential()
        model.add(Conv1D(filters=128, kernel_size=3, activation='relu', input_shape=(in_len, num_features)))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Flatten())
        model.add(Dense(100, activation='relu'))
        model.add(Dense(50, activation='relu'))
        model.add(Dense(out_len))
        opt = keras.optimizers.Adam(learning_rate=0.01)
        model.compile(optimizer=opt, loss='mse')

        # fit model
        model.fit(X_train, y_train, epochs=5, verbose=1)

        # test model
        N_test = np.shape(data_test)[1]
        for m in range(M):
            print(str(m) + '/' + str(M), end='\r')
            for n in range(N_test - (in_len + out_len)):

                x_test = data_test[m, n : n + in_len]
                x_test = x_test.reshape((1, in_len, num_features))
                y_hat = model.predict(x_test, verbose=0)
                y_true = data_test[m, n + in_len : n + in_len + out_len]
                baseline = np.ones(np.shape(y_true)) * x_test[0, -1, 0]

                # mean squared error calculation
                mse += np.linalg.norm(y_hat[0, :] - y_true)**2 / (3 * M * (N_test - (in_len + out_len)))
                mse_b += np.linalg.norm(baseline - y_true)**2 / (3 * M * (N_test - (in_len + out_len)))

                thresh = 0.4
                if (y_hat[0, 0] - x_test[0, -1, 0] > thresh):
                    guesses += 1
                    if (y_true[0] - x_test[0, -1, 0] > 0):
                        momentum_correct += 1

    print(mse)
    print(mse_b)
    print('done')