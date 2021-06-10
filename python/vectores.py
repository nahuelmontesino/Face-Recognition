from tensorflow.python import keras
import Rostros_utils as utils
import tensorflow as tf
import os
import cv2

"""image_path = ["./Images misma carpeta/"]
face_cascade = "./haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(face_cascade)
#Esta carpeta hay que crearla
# Iterate through files
for path in image_path:
  for f in [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]:
    print(os.path.join(path, f))
    utils.save_faces(cascade, f,path)"""


embedding = tf.keras.models.load_model('my_model2.h5')
path = "./Imagene"
name, vector = utils.get_name_and_vector(path, embedding)
print(vector[0])