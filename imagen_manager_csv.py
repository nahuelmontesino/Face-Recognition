import cv2
import imageio as im
import os
import numpy as np
import db_manager as dbm
import rostros_utils as utils
import tensorflow as tf
from pathlib import Path
import pandas as pd 
from ast import literal_eval

model = tf.keras.models.load_model(r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Modelos\model_vgg_face.h5')
path_base_images = r"D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\alumnos_faces"
consulta_path_base = r"D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\consultas"
#folder_to_save_ = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\resultados'
#image_directory = r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Fotos Alumnos FRCU\Fotos Alumnos FRCU/'
#aumented_images_dir = r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Imagenes_aumentadas/'
prueba_normalizar = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\pruebar_normalizar'
folder_to_save_ = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\resultados_normalizados'

alumnos_face_csv = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\imagenes.csv'
prueba = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\prueba.csv'
consultas_csv = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\consultas.csv'
#encoding="latin9", sep=";"


def save_imagenes_from_csv(csv, is_consulta=False):
    database = dbm.DatabaseConnection()
    df = pd.read_csv(csv)
    nombres = df['Name'].tolist()
    vectores = df['Vectores']
    lengh = len(nombres)

    for x in range(lengh):
        try:
            tupla_image = nombres[x], literal_eval(vectores[x])
            database.insert_new_image(tupla_image, is_consulta)
        except:
            continue


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
        try:
            i += 1
            if consult_name_old != consult_name:
                if not os.path.exists(os.path.join(folder_to_save,consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""))):
                    os.makedirs(os.path.join(folder_to_save,consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg","")))
                myfile = Path(os.path.join(folder_to_save,consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""),'distancias.txt'))
                myfile.touch(exist_ok=True)

                consult_name_old = consult_name
                path = os.path.join(consulta_path_base, consult_name_old)
                img = im.imread(path)
                path_to_write = os.path.join(folder_to_save, consult_name_old.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""), 'imagen_base.jpg')
                im.imwrite(path_to_write, img)

            path = os.path.join(path_base_images, img_name)
            img = im.imread(path)
            # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im.imwrite(os.path.join(folder_to_save, consult_name_old.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""), f'similar{i}.jpg'), img)

            path_file = os.path.join(folder_to_save, consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""),'distancias.txt')
            myfile = open(path_file, 'a')
            myfile.write('\n' + f'similar{i}.jpg' + ' ' + str(distancia))
            myfile.close()
        except:
            continue


"Paso 1: Cargar las imagenes en la tabla imagenes"
# save_imagenes_from_csv(alumnos_face_csv)
"Paso 2: cargar las consultas en la tabla consulta"
# save_imagenes_from_csv(consultas_csv,True)
"Paso 3: Obtener las respuestas asociadas a cada consulta y guardarlas en la tabla respuesta"
# load_anwers_from_queries(10)
"Paso 4: Guardar en una carpeta las imagenes de las consultas y sus respuestas similares"
save_similar_faces(folder_to_save_)
