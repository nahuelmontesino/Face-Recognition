import cv2
import imageio as im
import os
import numpy as np
import db_manager as dbm
from tensorflow.python import keras
import Rostros_utils as utils
import tensorflow as tf
from psycopg2.extensions import register_adapter, AsIs


model = tf.keras.models.load_model(r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Modelos\my_model3.h5')
path_base = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Imagenes\Fotos Alumnos FRCU'

database = dbm.DatabaseConnection()

for nombre in os.listdir(path_base)[:1]:
    path = os.path.join(path_base, nombre)
    embedding = utils.get_vector(path, model)
    image = nombre,np.array(embedding).tolist()[0]
    #print(np.array(embedding).tolist()[0])
    database.insert_new_image(image)

# def addapt_numpy_array(numpy_array):
#     return AsIs(tuple(numpy_array))



# img = im.imread(path)
#  img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)