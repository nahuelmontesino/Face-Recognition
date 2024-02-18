import cv2
import os
import db_manager as dbm
from face_utils import get_face_crop, get_vector
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


def load_images_into_database(dir_path, model, is_query=False):
    """
    Loads images from a given directory into a database. The image name
    and the feature vector are stored

    Args:
        dir_path (str): Path to the directory containing the images to load.
        model: Model used to extract features from the images.
        is_query (bool, optional): Indicates if the images are for querying. Default is False.
    """
    # connect with database
    database = dbm.DatabaseConnection()

    for image_name in os.listdir(dir_path):
        try:
            face_crop = get_face_crop(dir_path, image_name)
            # get image features array
            embedding = get_vector(face_crop, model)
            # .tolist() allow to save into the database
            image = embedding.tolist()
            # insert the image features into the database
            database.insert_new_image((image_name, image), is_query)
        except Exception as e:
            print("Ocurrió una excepción:", e)


def load_anwers_from_queries(limit):
    """
    Iterate over the queries table and get the most similar faces asociated
    to every query and insert it into a response table. The number of similar
    faces that are stored is based on the "limit" number

    Args:
        limit: answer number for every query
    """
    database = dbm.DatabaseConnection()
    database.insert_anwers_from_queries(limit)


def save_similar_faces(folder_to_save):
    """
    Get responses from the database response table and saves a 
    folder per query, in this folder will be the base image and its similar N
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


"Step 1: load the images into the images table"
load_images_into_database(MAIN_IMAGES_DIR, model)
"Step 2: cload the queries into the query table"
load_images_into_database(REQUEST_IMAGES_DIR, model, True)
"Step 3: get the answers related to every query and save it in the response table"
load_anwers_from_queries(20)
"Step 4: save in the output folder the images from the queries and their answers"
save_similar_faces(OUTPUT_DIR)
