import cv2
import imageio as im
import os
import numpy as np
import db_manager as dbm
from tensorflow.python import keras
import Rostros_utils as utils
import tensorflow as tf


model = tf.keras.models.load_model("""model path""")
path_base = """path base a donde se encuentran las imagenes"""

database = dbm.DatabaseConnection()

for nombre in database.query_all_nombres()[:1]:
    path = os.path.join(path_base, nombre)
    img = im.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    embedding = utils.get_vector(path, model)
    #db.insert_vector(nombre, embedding)
