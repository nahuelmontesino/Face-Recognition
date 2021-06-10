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


model = tf.keras.models.load_model(r'C:\Users\monte\Desktop\Grupo_investigacion\Codigo\my_model3.h5')
vectors = []
dir_path = r'C:\Users\monte\Desktop\Grupo_investigacion\Codigo\Images misma carpeta'
for image_name in os.listdir(dir_path):
  path = os.path.join(dir_path,image_name)
  embedding = utils.get_vector(path, model)
  vectors.append(embedding)