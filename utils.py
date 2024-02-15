import os
import cv2
import rostros_utils as utils

#image_directory = r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Fotos Alumnos FRCU\Fotos Alumnos FRCU/'
#aumented_images_dir = r'C:\Users\monte\Desktop\Grupo_investigacion\Datasets\Imagenes_aumentadas/'

dir_origen = 'consultas'
dir_destino = 'consultas_rostros'

#dir_origen = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\Fotos Alumnos FRCU/'
# dir_origen = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\prueba'
# dir_destino = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\alumnos_faces'
#dir_destino = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Fotos Alumnos\consultas'


def generate_datasets(images_dir, aumented_images_dir):
    aumented_list_dir = os.listdir(aumented_images_dir)
    for image_name in os.listdir(images_dir)[:1]:
        image_name = image_name.replace('.jpg',"").replace('.JPG',"")
        filter_object = filter(lambda a: image_name in a, aumented_list_dir)
        print(list(filter_object))

#generate_datasets(image_directory, aumented_images_dir)

face_cascade = "haarcascade_frontalface_default.xml"
cascade = cv2.CascadeClassifier(face_cascade)
# Esta carpeta hay que crearla
# Iterate through files
# for f in [f for f in os.listdir(dir_origen) if os.path.isfile(os.path.join(dir_origen, f))]:
#     print(os.path.join(dir_origen, f))
#     # print(os.path.join(dir_destino, f))
#     utils.save_only_face(cascade, f, dir_origen, dir_destino)

for f in [f for f in os.listdir(dir_origen) if os.path.isfile(os.path.join(dir_origen, f))]:
    # print(os.path.join(dir_origen, f))
    # print(os.path.join(dir_destino, f))
    # print(f)
    try:
        utils.recortarRostro(dir_origen, dir_destino, f)
       
    except:
        continue 