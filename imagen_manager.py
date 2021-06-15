import cv2
import imageio as im
import os
import numpy as np
import db_manager as dbm
from tensorflow.python import keras
import Rostros_utils as utils
import tensorflow as tf


model = tf.keras.models.load_model(r'C:\Users\monte\Desktop\Grupo_investigacion\Modelos\model_trainig_with_similars.h5')
path_base_images = r"C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Fotos Alumnos FRCU\Test"
consulta_path_base = r"C:\Users\monte\Desktop\Consultas"
folder_to_save_ = r'C:\Users\monte\Desktop\Prueva'



def load_images_into_database(dir_path, model, is_consulta=False):
    """
    Se guarda el nombre y el vector asociados a 
    una imagen en la base de datos, a partir de un direcorio dado.
    --dir_path: directorio desde donde se obtienen las imagenes
    --model: modelo para obtener los vectores a partir de la imagenes
    --is_consulta: especifica si las imagenes a cargar son para consulta, 
    caso contrario se agregan a la tabla imagen
    """
    database = dbm.DatabaseConnection()
    for nombre in os.listdir(dir_path):
        path = os.path.join(dir_path, nombre)
        #TODO: ANTES DE OBTENER EL VECTOR SE DEBERIA OBTENER EL ROSTRO CON utils.get_only_face()
        try:
            embedding = utils.get_vector(path, model)
            "np.array(embedding).tolist()[0] permite guardarlo en la base de datos"
            image = nombre, np.array(embedding).tolist()[0]
            database.insert_new_image(image, is_consulta)
        except:
            continue

def load_anwers_from_queries(limit):
    """
    Recorre las consultas y obtiene las respuestas asociadas a 
    cada una de ellas
    """
    database = dbm.DatabaseConnection()
    database.insert_anwers_from_queries(limit)

def save_similar_faces(folder_to_save):
    i = 0
    database = dbm.DatabaseConnection()
    consult_name_old = ""
    for img_name, consult_name in database.get_answers():
        i += 1
        if consult_name_old != consult_name:
            consult_name_old = consult_name
            path = os.path.join(consulta_path_base, consult_name_old)
            img = im.imread(path)
            path_to_write = os.path.join(folder_to_save, consult_name_old.replace(".JPG", "").replace(".jpg",""), 'imagen_base.jpg')
            cv2.imwrite(path_to_write, img)
            

        path = os.path.join(path_base_images, img_name)
        img = im.imread(path)
        cv2.imwrite(os.path.join(folder_to_save, consult_name_old.replace(".JPG", "").replace(".jpg",""), f'similar{i}.jpg'), img)

#database = dbm.DatabaseConnection()
#database.get_answers()


#load_images_into_database(path_base_images, model)
#load_images_into_database(consulta_path_base, model, True)
save_similar_faces(folder_to_save_)


#load_anwers_from_queries(10)

