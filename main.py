import cv2
import os
import pathlib
import numpy as np
from PIL import Image


cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8, 123)
root_path = 'pictures'


def get_images(image_paths):
    images = []
    labels = []

    for image_path in image_paths:
        faces, image = detect_faces(image_path)

        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            subject_number = int(str(image_path.parent)[-1:])
            labels.append(subject_number)
    return images, labels


def test_recognition(test_image_paths):
    for image_path in test_image_paths:
        faces, image = detect_faces(image_path)

        for (x, y, w, h) in faces:
            number_predicted, conf = recognizer.predict(image[y: y + h, x: x + w])
            number_actual = int(str(image_path.parent)[-1:])    

            if number_actual == number_predicted:
                print("{} корректно опознано со значением уверенности {}".format(number_actual, conf))
            else:
                print("{} неправильно опознано как {}".format(number_actual, number_predicted))


def detect_faces(image_path):
    gray = Image.open(str(image_path)).convert('L')
    image = np.array(gray, 'uint8')
    faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
    return faces, image


def show_images(image, x, y, w, h, time=100):
    cv2.imshow("", image[y: y + h, x: x + w])
    cv2.waitKey(time)


train_image_paths = [pathlib.PurePath(paths, name) for paths, subdirectory, files in os.walk(root_path)
                     for name in files
                     if len(name) > 8 and name[-6:-4] != '10']

test_image_paths = [pathlib.PurePath(paths, name) for paths, subdirectory, files in os.walk(root_path)
                    for name in files
                    if len(name) > 8 and name[-6:-4] == '10']

images, labels = get_images(train_image_paths)
cv2.destroyAllWindows()

recognizer.train(images, np.array(labels))
test_recognition(test_image_paths)
