import psycopg2


class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
                "dbname='gad' user='postgres' host='localhost' password='admin' port='5433'")
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def insert_new_image(self,image, is_consulta):
        """Allow to insert image name and asociated vector"""
        if is_consulta:
            insert_command = "INSERT INTO consulta(nombre,vector) VALUES(%s,%s)"
        else:
            insert_command = "INSERT INTO imagen(nombre,vector) VALUES(%s,%s)"
        self.cursor.execute(insert_command, image)
    
    def insert_new_consulta(self,consulta):
        """Allow to insert image name and asociated vector"""
        insert_command = "INSERT INTO consulta(nombre, vector) VALUES(%s,%s)"
        self.cursor.execute(insert_command, consulta)

    def get_answers(self):
        """Obtiene las respuestas asociadas a cada consulta"""
        self.cursor.callproc("Obtener_Respuestas")
        answers = self.cursor.fetchall()

        return answers

    def insert_anwers_from_queries(self, limit):
        "Agregar las limit respuestas asociadas a cada consulta"
        self.cursor.callproc("Insert_top_similars", (limit,))

    def get_similars(self):
        self.cursor.execute("select")  

    def query_all_nombres(self):
        """Get all persons name from Image table"""
        self.cursor.execute("SELECT nombre FROM imagen;")
        nombres =[nombre[0] for nombre in  self.cursor.fetchall()] 
        return nombres

    def close_connection(self):
        self.cursor.close()
        self.connection.close()        

if __name__=='__main__':
    databaseConnection = DatabaseConnection()
    databaseConnection.query_all_nombres()
    databaseConnection.close_connection()
    

