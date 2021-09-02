import cv2
import imageio as im
import os
import numpy as np
import db_manager as dbm
import Rostros_utils as utils
import tensorflow as tf
from pathlib import Path


model = tf.keras.models.load_model(r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Modelos\model_vgg_face.h5')
path_base_images = r"D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\alumnos_faces"
consulta_path_base = r"D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\consultas"
#folder_to_save_ = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\resultados'
#image_directory = r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Fotos Alumnos FRCU\Fotos Alumnos FRCU/'
#aumented_images_dir = r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Imagenes_aumentadas/'
prueba_normalizar = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\pruebar_normalizar'
folder_to_save_ = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\resultados_normalizados'




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
    for nombre in os.listdir(dir_path):
        path = os.path.join(dir_path, nombre)
        #TODO: ANTES DE OBTENER EL VECTOR SE DEBERIA OBTENER EL ROSTRO CON utils.get_only_face()
        try:
            embedding = utils.get_vector(path, model)
            "np.array(embedding).tolist()[0] permite guardarlo en la base de datos"
            image = nombre, np.array(embedding).tolist()[0]
            print(image)
            #database.insert_new_image(image, is_consulta)
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
        #print('distancia',distancia)
        i += 1
        if consult_name_old != consult_name:
            if not os.path.exists(os.path.join(folder_to_save,consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""))):
                os.makedirs(os.path.join(folder_to_save,consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg","")))
            #open(os.path.join(folder_to_save,img_name,'distancias.txt'),'a+')
            myfile = Path(os.path.join(folder_to_save,consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""),'distancias.txt'))
            myfile.touch(exist_ok=True)
           
            consult_name_old = consult_name
            path = os.path.join(consulta_path_base, consult_name_old)
            #print('path',path)
            img = im.imread(path)
            #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            path_to_write = os.path.join(folder_to_save, consult_name_old.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""), 'imagen_base.jpg')
            #print("path_to_write",path_to_write)
            im.imwrite(path_to_write, img)
 
            
            
        path = os.path.join(path_base_images, img_name)
        img = im.imread(path)
        #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im.imwrite(os.path.join(folder_to_save, consult_name_old.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""), f'similar{i}.jpg'), img)

        path_file = os.path.join(folder_to_save, consult_name.replace(".JPG", "").replace(".jpg","").replace(".jpeg",""),'distancias.txt')
        myfile = open(path_file,'a')
        myfile.write('\n' + f'similar{i}.jpg' + ' ' + str(distancia))
        myfile.close()


#aumentation = aumentation.DataAumentation()
#aumentation.generete_aumented_images(image_directory, aumented_images_dir, 5)
"Paso 1: Cargar las imagenes en la tabla imagenes"
load_images_into_database(prueba_normalizar, model)
"Paso 2: cargar las consultas en la tabla consulta"
#load_images_into_database(consulta_path_base, model, True)
"Paso 3: Obtener las respuestas asociadas a cada consulta y guardarlas en la tabla respuesta"
#load_anwers_from_queries(10)
"Paso 4: Guardar en una carpeta las imagenes de las consultas y sus respuestas similares"
#save_similar_faces(folder_to_save_)





