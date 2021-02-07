import numpy as np
from sklearn.model_selection import  train_test_split
import cv2
from os import listdir
from os.path import isfile, join
import image_manipulation as im
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD
import datetime

def read_test_data(path, label):
    data = []
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    for file in onlyfiles:
        test_image = cv2.imread(path+file)
        test_image = im.prepare_image(test_image)  
        data.append(test_image)

    labels = [label for element in data]
    return data, labels

# define cnn model
def define_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(128, 128, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(10, activation='softmax'))
    # compile model
    opt = SGD(lr=0.01, momentum=0.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    return model

print('---- loading sample files')

sample_data = []
sample_labels = []

# ## Sample001 = Zeros
# print('---- loading Zeros')
# path = './datasets/Char74K/English/Fnt/Sample001/'
# temp_data, temp_labels = read_test_data(path, 0)
# sample_data.extend(temp_data)
# sample_labels.extend(temp_labels)

## Sample002 = Ones
print('---- loading Ones')
path = './datasets/Char74K/English/Fnt/Sample002/'
temp_data, temp_labels = read_test_data(path, 1)
sample_data.extend(temp_data)
sample_labels.extend(temp_labels)

## Sample002 = Twos
print('---- loading Twos')
path = './datasets/Char74K/English/Fnt/Sample003/'
temp_data, temp_labels = read_test_data(path, 2)
sample_data.extend(temp_data)
sample_labels.extend(temp_labels)

## Sample002 = Threes
print('---- loading Threes')
path = './datasets/Char74K/English/Fnt/Sample004/'
temp_data, temp_labels = read_test_data(path, 3)
sample_data.extend(temp_data)
sample_labels.extend(temp_labels)

## Sample002 = Fours
print('---- loading Fours')
path = './datasets/Char74K/English/Fnt/Sample005/'
temp_data, temp_labels = read_test_data(path, 4)
sample_data.extend(temp_data)
sample_labels.extend(temp_labels)

## Sample002 = Fives
print('---- loading Fives')
path = './datasets/Char74K/English/Fnt/Sample006/'
temp_data, temp_labels = read_test_data(path, 5)
sample_data.extend(temp_data)
sample_labels.extend(temp_labels)

## Sample002 = Sixes
print('---- loading Sixes')
path = './datasets/Char74K/English/Fnt/Sample007/'
temp_data, temp_labels = read_test_data(path, 6)
sample_data.extend(temp_data)
sample_labels.extend(temp_labels)

## Sample002 = Sevens
print('---- loading Sevens')
path = './datasets/Char74K/English/Fnt/Sample008/'
temp_data, temp_labels = read_test_data(path, 7)
sample_data.extend(temp_data)
sample_labels.extend(temp_labels)

## Sample002 = Eights
print('---- loading Eights')
path = './datasets/Char74K/English/Fnt/Sample009/'
temp_data, temp_labels = read_test_data(path, 8)
sample_data.extend(temp_data)
sample_labels.extend(temp_labels)

## Sample002 = Nines
print('---- loading Nines')
path = './datasets/Char74K/English/Fnt/Sample010/'
temp_data, temp_labels = read_test_data(path, 9)
sample_data.extend(temp_data)
sample_labels.extend(temp_labels)

print('---- calc model')

training_features = np.array(sample_data, dtype='float32')
sample_labels = np.array(sample_labels)
training_data, test_data, training_labels, test_labels = train_test_split(training_features, sample_labels)

training_data = training_data.reshape((training_data.shape[0], 128, 128, 1))
test_data = test_data.reshape((test_data.shape[0], 128, 128, 1))

# one hot encode target values
training_labels = to_categorical(training_labels)
test_labels = to_categorical(test_labels)

training_data = training_data / 255.0
test_data = test_data / 255.0

model = define_model()
# fit model
model.fit(training_data, training_labels, epochs=10, batch_size=32, verbose=0)
_, acc = model.evaluate(test_data, test_labels, verbose=0)
print('> %.3f' % (acc * 100.0))

model.save('./models/Char74K_CNN_model.h5')
print(datetime.datetime.now())
