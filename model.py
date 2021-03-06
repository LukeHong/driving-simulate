import cv2
import numpy as np
import csv

samples = []
with open('./data/driving_log.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        samples.append(line)


from sklearn.model_selection import train_test_split
train_samples, validation_samples = train_test_split(samples, test_size=0.2)

import sklearn

def generator(samples, batch_size=32):
    num_samples = len(samples)
    while 1: # Loop forever so the generator never terminates
        np.random.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset+batch_size]

            images = []
            angles = []
            for batch_sample in batch_samples:

                # add slightly correction to side camera
                correction = 0.2
                steering = float(batch_sample[3])
                steering_left = steering + correction
                steering_right = steering - correction

                # get center, left, right camera images
                folder = "./data/IMG/"
                img_center = cv2.imread(folder + batch_sample[0].split("\\")[-1])
                img_left = cv2.imread(folder + batch_sample[1].split("\\")[-1])
                img_right = cv2.imread(folder + batch_sample[2].split("\\")[-1])

                images.extend([img_center, img_left, img_right])
                angles.extend([steering, steering_left, steering_right])

            X_train = np.append(np.array(images), np.fliplr(np.array(images)), axis=0)
            y_train = np.append(np.array(angles), -np.array(angles), axis=0)
            yield sklearn.utils.shuffle(X_train, y_train)

batch_size = 32
train_generator = generator(train_samples, batch_size=batch_size)
validation_generator = generator(validation_samples, batch_size=batch_size)


from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Lambda
from keras.layers import Conv2D, MaxPooling2D, Cropping2D
from keras.optimizers import  Adam

import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.7
#config.gpu_options.visible_device_list = "0"
set_session(tf.Session(config=config))

model = Sequential()
model.add(Lambda(lambda x: (x / 127.5) - 1., input_shape=(160, 320, 3)))
model.add(Cropping2D(cropping=((50,20), (0,0)), input_shape=(160,320,3)))
model.add(Conv2D(24, (5, 5), strides=(2, 2), activation="relu"))
model.add(Conv2D(36, (5, 5), strides=(2, 2), activation="relu"))
model.add(Conv2D(48, (5, 5), strides=(2, 2), activation="relu"))
model.add(Conv2D(64, (3, 3), strides=(2, 2), activation="relu"))
model.add(Conv2D(64, (3, 3), strides=(2, 2), activation="relu"))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(10))
model.add(Dense(1))

model.compile(loss="mse", optimizer="adam")
model.fit_generator(train_generator, steps_per_epoch=len(train_samples)/batch_size,
                    validation_data=validation_generator, validation_steps=len(validation_samples),
                    epochs=3)

model.save("model.h5")
