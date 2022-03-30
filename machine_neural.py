from keras.models import Sequential
from keras.layers import Dense

import machine_classifiers


def machine(x, y_train, x_test, y_test):
    # Define arquitetura do modelo (MLP)
    # Por enquanto esta configuracao gerou menor eqm. Testar outras.
    model = Sequential()
    model.add(Dense(20, input_dim=20, activation='relu'))
    model.add(Dense(6, activation='relu'))
    model.add(Dense(6, activation='relu'))
    model.add(Dense(8, kernel_initializer='normal'))
    # Roda o modelo
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x, y_train, validation_split=0.33, epochs=100, batch_size=32, verbose=0)

    # Para avaliar o erro quadratico medio
    eqm = model.evaluate(x_test, y_test)

    # Para gerar valores preditos
    # ab = model.predict(np.array(x_test))
    print(eqm)


if __name__ == '__main__':
    X_train, X_test, y_train, y_test = machine_classifiers.basics()
    machine(X_train, y_train, X_test, y_test)
