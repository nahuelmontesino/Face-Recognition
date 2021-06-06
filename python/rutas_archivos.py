import os
import shutil

path = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\Python-code'
img_original = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\original\\img.jpg'
path_img_copia = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\copia'
path_img = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\Imagenes\\lfw_funneled'
path_original = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\original'

# path_entrenamiento = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\copia\\entrenamiento'
# path_validacion = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\copia\\validacion'

path_entrenamiento = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\Imagenes\\1000 imagenes\\entrenamiento'
path_validacion = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\Imagenes\\1000 imagenes\\validacion'

# with os.scandir(path) as ficheros:
#     for fichero in ficheros:
#         print(fichero.name)

# shutil.copy(img_original,path_img_copia)

# for file in os.listdir(path_img_copia):
#     src = file 
#     dst = "rename.jpg"
#     os.rename(src,dst)

#os.rename('D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\copia\\img.jpg',"D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\copia\\rename.jpg")

#print(len([name for name in os.listdir(path_img_copia) if os.path.isfile(name)])) 

#print(os.listdir(path_img))

def copiarImagenes(cantidad,path_origen,path_destino_entrenamiento,path_destino_validacion):
    count = 0
    index = 0
    lista_ficheros = os.listdir(path_origen)
    print(path_origen +'\\'+ lista_ficheros[count])
    while count <= cantidad - 1:
        if(len([name for name in os.listdir(path_origen +'\\'+ lista_ficheros[index])]) >= 2):
            imagenes_subdirectorio = os.listdir(path_origen + '\\' +lista_ficheros[index])
            shutil.copy(path_origen + '\\' + lista_ficheros[index] + '\\' + imagenes_subdirectorio[0],path_destino_entrenamiento)
            os.rename(path_destino_entrenamiento + '\\' + imagenes_subdirectorio[0], path_destino_entrenamiento + '\\' + str(count) + ".jpg")
            shutil.copy(path_origen + '\\' + lista_ficheros[index] + '\\' + imagenes_subdirectorio[1],path_destino_validacion)
            os.rename(path_destino_validacion  + '\\' + imagenes_subdirectorio[1], path_destino_validacion + '\\' + str(count) + ".jpg")
            # print(imagenes_subdirectorio)
            # print(imagenes_subdirectorio[0])
            # print(imagenes_subdirectorio[1])
            count = count  + 1
        index += 1 #se elimina el primer fichero, ya que el while es la cantidad de fotos que queres

#copiarImagenes(1000,path_img,path_entrenamiento,path_validacion)
#copiarImagenes(3,path_original,path_entrenamiento,path_validacion)
#,path_destino_entrenamiento,path_destino_validacion

#print(len([name for name in os.listdir('D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\original\\1')]))

