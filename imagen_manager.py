import cv2
import imageio as im
import os
import numpy as np
import db_manager as dbm
from tensorflow.python import keras
import Rostros_utils as utils
import tensorflow as tf


model = tf.keras.models.load_model(r'C:\Users\monte\Desktop\Grupo_investigacion\Modelos\model_training_with_faces.h5')
path_base_images = r"C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Fotos Alumnos FRCU\Fotos Alumnos FRCU"
consulta_path_base = "Path base donde se encuentran las imagenes de la tabla consulta"

database = dbm.DatabaseConnection()

def insert_name_and_vector_from_directory(dir_path, model):
    for nombre in os.listdir(dir_path):
        path = os.path.join(dir_path, nombre)
        #TODO: ANTES DE OBTENER EL VECTOR SE DEBERIA OBTENER EL ROSTRO CON utils.get_only_face()
        try:
            embedding = utils.get_vector(path, model)
            "np.array(embedding).tolist()[0] permite guardarlo en la base de datos"
            image = nombre, np.array(embedding).tolist()[0]
            database.insert_new_image(image)
        except:
            continue

def save_similar_faces(folder_to_save):
    for id, name in database.get_queries():
        path = os.path.join(consulta_path_base, name)
        img = im.imread(path)
        cv2.imwrite(os.path.join(folder_to_save,name, name), img)
        for i , name in enumerate(database.get_ansquers(id)):
            path = os.path.join(path_base_images, name)
            img = im.imread(path)
            cv2.imwrite(os.path.join(folder_to_save,name, name+f'similar{i}'), img)

insert_name_and_vector_from_directory(path_base_images, model)