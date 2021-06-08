import psycopg2
import os
from pprint import pprint




class DatabaseConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                "dbname='gad' user='postgres' host='localhost' password='admin' port='5432'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except:
            pprint("No se pudo conectar con la base de datos")


    def insert_new_categoria(self,categoria_name):
        insert_command = f"INSERT INTO categoria(nombre) VALUES('{categoria_name}')" #f para insertar valores en string
        pprint(insert_command)
        self.cursor.execute(insert_command)

    def insert_new_imagenes(self,images):
        insert_command = "INSERT INTO imagen(nombre,vector) VALUES(%s,%s)"
        self.cursor.executemany(insert_command, images)  #execute many para insertar por lote, images es un arrary de imagenes
    

    def query_all_nombres(self):
        self.cursor.execute("SELECT nombre FROM imagen;")
        nombres =[nombre[0] for nombre in  self.cursor.fetchall()]  #fetchall convierte en una lista lo que viene 
        return nombres
        

    def insert_all_name(self):
        nombres = os.listdir(path_base)
        for nombre in nombres:
            try:
                insert_command = f"INSERT INTO imagen(nombre) VALUES('{nombre}')"
                self.cursor.execute(insert_command) 
            except:
                continue
         
         


    def close_connection(self):
        self.cursor.close()
        self.connection.close()        

if __name__=='__main__':
    databaseConnection = DatabaseConnection()

    databaseConnection.query_all_nombres()
    #databaseConnection.insert_new_categoria("perro")
    #databaseConnection.insert_new_imagenes([("nahuel",[1.1,1.3],"path/path"),("agustin",[1.4,1.5],"path1/path1")])
    #databaseConnection.insert_all_name()
    #cerrar conexion dsp de ejecutar los comandos
    databaseConnection.close_connection()
    

