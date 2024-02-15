import cv2
import os
import numpy as np
import db_manager as dbm
from rostros_utils import get_face_crop, get_vector
import tensorflow as tf
from pathlib import Path
from dotenv import load_dotenv

# Load env variables
dotenv_path = Path("enviroment.env")
load_dotenv(dotenv_path=dotenv_path)

model = tf.keras.models.load_model('model/model_vgg_face.h5')
PATH_BASE_IMAGES = os.getenv("PATH_BASE_IMAGES")
REQUEST_IMAGES_DIR = os.getenv("REQUEST_IMAGES_DIR")
MAIN_IMAGES_DIR = os.getenv("MAIN_IMAGES_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")

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
            face_crop = get_face_crop(dir_path, image_name)
            embedding = get_vector(face_crop, model)
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
            if not os.path.exists(os.path.join(folder_to_save, os.path.splitext(consult_name)[0])):
                os.makedirs(os.path.join(folder_to_save, os.path.splitext(consult_name)[0]))

            myfile = Path(os.path.join(folder_to_save, os.path.splitext(consult_name)[0]), 'distancias.txt')
            myfile.touch(exist_ok=True)

            consult_name_old = consult_name
            path = os.path.join(REQUEST_IMAGES_DIR, consult_name_old)
            img = cv2.imread(path)
            path_to_write = os.path.join(folder_to_save, os.path.splitext(consult_name)[0], 'imagen_base.jpg')

            cv2.imwrite(path_to_write, img)

        path = os.path.join(PATH_BASE_IMAGES, img_name)
        img = cv2.imread(path)
        cv2.imwrite(os.path.join(folder_to_save, os.path.splitext(consult_name)[0], f'similar{i}.jpg'), img)

        path_file = os.path.join(folder_to_save, os.path.splitext(consult_name)[0], 'distancias.txt')
        myfile = open(path_file, 'a')
        myfile.write('\n' + f'similar{i}.jpg' + ' ' + str(distancia))
        myfile.close()


"Paso 1: Cargar las imagenes en la tabla imagenes"
load_images_into_database(MAIN_IMAGES_DIR, model)
"Paso 2: cargar las consultas en la tabla consulta"
load_images_into_database(REQUEST_IMAGES_DIR, model, True)
"Paso 3: Obtener las respuestas asociadas a cada consulta y guardarlas en la tabla respuesta"
load_anwers_from_queries(20)
"Paso 4: Guardar en una carpeta las imagenes de las consultas y sus respuestas similares"
save_similar_faces(OUTPUT_DIR)
