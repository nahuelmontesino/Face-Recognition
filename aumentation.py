from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import rostros_utils as utils
import numpy as np
import os

datagen = ImageDataGenerator(
    rescale=1./255,     # Establece el valor de los pixeles en un rando de (0 a 1)
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.3,  # Inclina las imagenes
    zoom_range=0.2,  # Hace zoom a las imagenes
    brightness_range=[0.7, 1.3],
    horizontal_flip=True,  # Invierte las imagenes
    fill_mode='nearest')


class DataAumentation:
    def __init__(self):
        self.datagen = datagen

    def generete_aumented_images(self, input_directory, output_directory, total_images):
        my_images = os.listdir(input_directory)
        for i, image_name in enumerate(my_images):
            try:  
                path = os.path.join(input_directory, image_name)    
                preprocess_img = utils.preprocess_image(path)  
                image_array = image.img_to_array(preprocess_img)
                image_array = np.expand_dims(image_array, axis=0)
            except:
                continue
            image_name = image_name.replace('.jpg','').replace('.JGP','')
            aumented_path = os.path.join(output_directory, image_name)
            if not os.path.exists(aumented_path):
                os.makedirs(aumented_path)

            img_gen = self.datagen.flow(image_array, batch_size=1,
                                    save_to_dir= aumented_path,
                                    save_prefix='image',
                                    save_format='jpg')  
            for e in range(total_images):
                img_gen.next()
    
