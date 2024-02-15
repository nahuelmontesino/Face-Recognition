import cv2
import imageio as im
import os
import numpy as np
import db_manager as dbm
import rostros_utils as utils
import tensorflow as tf
from pathlib import Path


model = tf.keras.models.load_model('model/model_vgg_face.h5')
path_base_images = "imagenes/rostros_images"
consulta_path_base = "imagenes/consultas"
prueba_normalizar = 'imagenes/images'
folder_to_save_ = 'imagenes/results'

target_shape = (224, 224)


def load_images_into_database(dir_path, model, is_consulta=False):
    """
    Se guarda el nombre y el vector asociados a 
    una imagen en la base de datos, a partir de un direcorio dado.

    Parameters
    ----------
    dir_path : directorio desde donde se obtienen las imagenes.
    model: modelo para obtener los vectores a partir de la imagenes.
    is_consulta: bool, optional
        especifica si las imagenes a cargar son para consulta, 
        caso contrario se agregan a la tabla imagen
    --------
    """
    database = dbm.DatabaseConnection()

    for image_name in os.listdir(dir_path):
        try:
            face_crop = utils.get_face_crop(dir_path, image_name)
            embedding = utils.get_vector(face_crop, model)
            "np.array(embedding).tolist()[0] permite guardarlo en la base de datos"
            image = np.array(embedding).tolist()[0]
            database.insert_new_image((image_name, image), is_consulta)
        except Exception as e:
            print("Ocurrió una excepción:", e)


def load_anwers_from_queries(limit):
    """
    Recorre la tabla consultas y obtiene las respuestas asociadas a 
    cada una de ellas y las inserta en la tabla respuesta
    Parameters
    ----------
    limit: numero de respuestas por consulta.
    --------
    """
    database = dbm.DatabaseConnection()
    database.insert_anwers_from_queries(limit)


def save_similar_faces(folder_to_save):
    """
     Obtiene respuestas de la tabla respuesta de la base de datos
     y guarda una carpeta por consulta, en dicha carpeta estara la imagen
     base y sus N similares
    """
    i = 0
    database = dbm.DatabaseConnection()
    consult_name_old = ""
    for img_name, consult_name, distancia in database.get_answers():
        i += 1
        if consult_name_old != consult_name:
            if not os.path.exists(os.path.join(folder_to_save, consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""))):
                os.makedirs(os.path.join(folder_to_save, consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg","")))

            myfile = Path(os.path.join(folder_to_save, consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""),'distancias.txt'))
            myfile.touch(exist_ok=True)

            consult_name_old = consult_name
            path = os.path.join(consulta_path_base, consult_name_old)
            img = im.imread(path)
            path_to_write = os.path.join(folder_to_save, consult_name_old.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""), 'imagen_base.jpg')

            im.imwrite(path_to_write, img)

        path = os.path.join(path_base_images, img_name)
        img = im.imread(path)
        im.imwrite(os.path.join(folder_to_save, consult_name_old.replace(".JPG", "").replace(".jpg", "").replace(".jpeg", ""), f'similar{i}.jpg'), img)

        path_file = os.path.join(folder_to_save, consult_name.replace(".JPG", "").replace(".jpg", "").replace(".jpeg", ""), 'distancias.txt')
        myfile = open(path_file, 'a')
        myfile.write('\n' + f'similar{i}.jpg' + ' ' + str(distancia))
        myfile.close()


"Paso 1: Cargar las imagenes en la tabla imagenes"
load_images_into_database(prueba_normalizar, model)
"Paso 2: cargar las consultas en la tabla consulta"
load_images_into_database(consulta_path_base, model, True)
"Paso 3: Obtener las respuestas asociadas a cada consulta y guardarlas en la tabla respuesta"
load_anwers_from_queries(20)
"Paso 4: Guardar en una carpeta las imagenes de las consultas y sus respuestas similares"
save_similar_faces(folder_to_save_)
