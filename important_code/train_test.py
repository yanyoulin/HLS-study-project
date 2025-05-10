# train_mlp_h5.py
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 固定 random seed
np.random.seed(0)
tf.random.set_seed(0)

# 假設是非常簡單的資料
X_train = np.random.rand(1000, 4).astype(np.float32)
y_train = np.random.rand(1000, 4).astype(np.float32)

# 建立小型模型
model = keras.Sequential([
    layers.Input(shape=(4,), name='input'),
    layers.Dense(4, activation='linear', name='dense1'),
    layers.Activation('gelu', name='gelu'),
    layers.Dense(4, activation='linear', name='dense2')
])

# 編譯
model.compile(optimizer='adam', loss='mse')

# 訓練
model.fit(X_train, y_train, epochs=50, batch_size=32)

# 存成 .h5 格式
model.save('small_mlp.h5')
print("Saved model as small_mlp.h5")
