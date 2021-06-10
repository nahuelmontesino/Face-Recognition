import cv2
import imageio as im
import os
import numpy as np
import db_manager as dbm

path_base = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\Imagenes\\Fotos Alumnos FRCU\\'

database = dbm.DatabaseConnection()


for nombre in database.query_all_nombres()[:1]:
    path = os.path.join(path_base, nombre)
    img = im.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # # if img == None: 
    # #     print('error')
    # #     print(img)
    # # else:
    # #     print('error')
    # #     print(img)
    # print(img)
    # print(path)
    #img = cv2.imread("0.jpg")
    #print(img)
    cv2.imshow('hola',img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   # print(type(path))