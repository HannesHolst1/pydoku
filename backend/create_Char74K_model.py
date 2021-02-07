import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import  train_test_split
import joblib
import cv2
from os import listdir
from os.path import isfile, join
import image_manipulation as im
from skimage.feature import hog


def read_test_data(path, label):
    data = []    
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    for file in onlyfiles:
        test_image = cv2.imread(path+file)
        test_image = im.prepare_image(test_image)
        hog_feature = hog(test_image, orientations=8, pixels_per_cell=(10,10), cells_per_block=(5, 5))      
        data.append(hog_feature)

    labels = [label for element in data]
    return data, labels

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

training_features = np.array(sample_data, dtype='float64')
training_data, test_data, training_labels, test_labels = train_test_split(training_features, sample_labels)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(training_data, training_labels)
model_score = knn.score(test_data, test_labels)

print('prediction score: {}'.format(model_score))

joblib.dump(knn, './models/Char74K_knn_model.pkl')