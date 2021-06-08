import cv2
import os
import db_manager as dbm

path_base = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\Imagenes\\Fotos Alumnos FRCU\\'

database = dbm.DatabaseConnection()


for nombre in database.query_all_nombres()[:1]:
    path = os.path.join(path_base, nombre)
    img = cv2.imread(path)
    if img == None: 
        print('error')
        print(img)
    print(path)
   # cv2.imshow('hola',img)