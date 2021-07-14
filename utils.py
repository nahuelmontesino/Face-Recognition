import os
import cv2
import Rostros_utils as utils

image_directory = r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Fotos Alumnos FRCU\Fotos Alumnos FRCU/'
aumented_images_dir = r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Imagenes_aumentadas/'

dir_origen = r'C:\Users\monte\Desktop\Consul_/'
dir_destino = r'C:\Users\monte\Desktop\Consultas/'

def generate_datasets(images_dir, aumented_images_dir):
    aumented_list_dir = os.listdir(aumented_images_dir)
    for image_name in os.listdir(images_dir)[:1]:
        image_name = image_name.replace('.jpg',"").replace('.JPG',"")
        filter_object = filter(lambda a: image_name in a, aumented_list_dir)
        print(list(filter_object))

#generate_datasets(image_directory, aumented_images_dir)

face_cascade = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(face_cascade)
#Esta carpeta hay que crearla
# Iterate through files
for f in [f for f in os.listdir(dir_origen) if os.path.isfile(os.path.join(dir_origen, f))]:
    print(os.path.join(dir_origen, f))
    utils.save_only_face(cascade, f, dir_origen, dir_destino)