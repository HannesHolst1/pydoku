from mnist import MNIST
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import joblib
# import cv2
# import random

mndata = MNIST('./MNIST')

training_images, training_labels = mndata.load_training()
test_images, test_labels = mndata.load_testing()

np.set_printoptions(linewidth=200)

# training_features = np.zeros(shape=(len(training_images), 28, 28), dtype='float64')
# for index, image in enumerate(training_images):
#     array = np.asarray(image)
#     training_features[index] = array.reshape(28,28)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(training_images, training_labels)
model_score = knn.score(test_images, list(test_labels))

print('prediction score: {}'.format(model_score))

joblib.dump(knn, './models/mnist_knn_model.pkl')