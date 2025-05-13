import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os
import sys

output_dir = sys.argv[1] if len(sys.argv) > 1 else "generated_code/default_output"
os.makedirs(output_dir, exist_ok=True)

X_train = np.random.rand(1000, 4).astype(np.float32)
y_train = np.random.rand(1000, 4).astype(np.float32)

model = keras.Sequential([
    layers.Input(shape=(4,), name='input'),
    layers.Dense(4, activation='linear', name='dense1'),
    layers.Activation('gelu', name='gelu'),
    layers.Dense(4, activation='linear', name='dense2')
])

model.compile(optimizer='adam', loss='mse')

model.fit(X_train, y_train, epochs=50, batch_size=32)

model_path = os.path.join(output_dir, 'model.h5')
model.save(model_path)
print(f"Saved model as {model_path}")
