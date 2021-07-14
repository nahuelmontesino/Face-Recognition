import os
import shutil
import aumentation
from itertools import combinations

path = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\Python-code'
img_original = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\original\\img.jpg'
path_img_copia = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\copia'
path_img_descargadas = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Imagenes\lfw_funneled'
path_original = 'D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\original'

path_imagene_aumentadas = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Imagenes\aumentadas/'
path_imagenes_facultad = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Imagenes\Fotos Alumnos FRCU/'


path_pares = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Imagenes\pares'

path_pares_facultad = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Imagenes\pares_facultad'
path_prueba = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Imagenes\pruebas'

path_aumentadas = r'D:\UTN\5 año\Gestion Avanzada de datos\Tp-Final\Imagenes\aumentadas'

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

def generar_pares(cantidad,path_origen,path_destino): #la cantidad como maximo 1 menos a la cantidad en cada directorio
    count = 4719
    lista_ficheros = os.listdir(path_origen)
    directorio_destino1 = os.path.join(path_destino,'imagenes1')
    directorio_destino2 = os.path.join(path_destino,'imagenes2')
    if not os.path.exists(directorio_destino1):
        os.makedirs(directorio_destino1)
        os.makedirs(directorio_destino2)
    for directorio in lista_ficheros: 
        try:        
            imagenes_subdirectorio = os.path.join(path_origen,directorio)
            imagenes_path = os.listdir(imagenes_subdirectorio)
            for index in range(0,cantidad):
                imagen1_path = os.path.join(path_origen,directorio,imagenes_path[0])
                imagen2_path = os.path.join(path_origen,directorio,imagenes_path[index + 1])
                #print(imagen1_path)
                #print(imagen2_path)
                shutil.copy(imagen1_path,directorio_destino1)
                imagen_destino1 = os.path.join(directorio_destino1,imagenes_path[0])
                #print(imagen_destino1)
                #print('este', directorio_destino1 + '\\' + str(count) +".jpg")
                os.rename(imagen_destino1,directorio_destino1 + '\\' + str(count) +".jpg")
                shutil.copy(imagen2_path,directorio_destino2)
                imagen_destino2 = os.path.join(directorio_destino2,imagenes_path[index + 1])
            # print(imagen_destino2)
                #print('este2', directorio_destino2 + '\\' + str(count) +".jpg")
                os.rename(imagen_destino2,directorio_destino2 + '\\' + str(count) +".jpg")
                count = count + 1
        except:
                continue



def generar_pares_all_combinaciones(path_origen,path_destino): #la cantidad como maximo 1 menos a la cantidad en cada directorio
    count = 0
    lista_ficheros = os.listdir(path_origen)
    directorio_destino1 = os.path.join(path_destino,'imagenes1')
    directorio_destino2 = os.path.join(path_destino,'imagenes2')
    if not os.path.exists(directorio_destino1):
        os.makedirs(directorio_destino1)
        os.makedirs(directorio_destino2)
    for directorio in lista_ficheros: 
        try:        
            imagenes_subdirectorio = os.path.join(path_origen,directorio)
            imagenes_path = os.listdir(imagenes_subdirectorio)
            #print(imagenes_path)
           # print(len(imagenes_path))
            if len(imagenes_path) > 1 and len(imagenes_path) <= 6:
                #print('hola')
                for par in combinations(imagenes_path,2): #par = tupla con la combinacion de imagnes
                   # print(par)
                    imagen1_path = os.path.join(path_origen,directorio,par[0])
                    imagen2_path = os.path.join(path_origen,directorio,par[1])
                    #print(imagen1_path)
                    #print(imagen2_path)
                    shutil.copy(imagen1_path,directorio_destino1)
                    imagen_destino1 = os.path.join(directorio_destino1,par[0])
                    #print(imagen_destino1)
                    # print('este', directorio_destino1 + '\\' + str(count) +".jpg")
                    os.rename(imagen_destino1,directorio_destino1 + '\\' + str(count) +".jpg")
                    shutil.copy(imagen2_path,directorio_destino2)
                    imagen_destino2 = os.path.join(directorio_destino2,par[1])
                    #print(imagen_destino2)
                    # print('este2', directorio_destino2 + '\\' + str(count) +".jpg")
                    os.rename(imagen_destino2,directorio_destino2 + '\\' + str(count) +".jpg")
                    count = count + 1
        except:
                continue            
             

#print(len([name for name in os.listdir('D:\\UTN\\5 año\\Gestion Avanzada de datos\\Tp-Final\\prueba\\original\\1')]))

# img_aumentation = aumentation.DataAumentation()
# img_aumentation.generete_aumented_images(path_imagenes_facultad,path_imagene_aumentadas,5)

#generar_pares(3,path_aumentadas,path_pares)

# print(os.listdir(path_imagene_aumentadas))

#print(len([name for name in os.listdir(path_img) if os.path.isdir(name)]))
#print(random.randint(0, 1))

# numeros = [1,2,3,4]
# palabras = ['10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg']

# # for num in combinations(numeros,2):
# #     print(num)

# for palabra in combinations(palabras,2):
#     print(palabra)    

#generar_pares_all_combinaciones(path_prueba,path_pares)

#generar_pares_all_combinaciones(path_img_descargadas,path_pares_facultad)

generar_pares(1,path_aumentadas,path_pares_facultad)

# array = [['jola','tor','sdas'],['este no'],['wqewqe','pole']]

# print(array)

# for elem in array:
#     if len(elem) > 1:
#         for par in combinations(elem,2):
#             print(par)