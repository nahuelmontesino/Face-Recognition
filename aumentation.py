from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import Rostros_utils as utils

datagen = ImageDataGenerator(        
        rotation_range = 40,
        shear_range = 0.2,
        zoom_range = 0.2,
        horizontal_flip = True,
        brightness_range = (0.5, 1.5))
import numpy as np
import os

image_directory = r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Fotos Alumnos FRCU\Fotos Alumnos FRCU/'
SIZE = 180
dataset = []
my_images = os.listdir(image_directory)
for i, image_name in enumerate(my_images):  
    try:  
        path = os.path.join(image_directory, image_name)    
        imagen = utils.preprocess_image(path)       
        imagen = image.img_to_array(imagen)
        #imagen = np.expand_dims(imagen, axis=0)
        dataset.append(imagen)
    except:
        continue

x = np.array(dataset)
i = 0
for batch in datagen.flow(x, batch_size=16,
                          save_to_dir= r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Fotos Alumnos FRCU\Fotos_aumentadas',
                          save_prefix='dr',
                          save_format='jpg'):    
    i += 1    
    if i > 50:        
        break