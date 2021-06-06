import psycopg2

# Global constant
PSQL_HOST = "localhost"
PSQL_PORT = "5432"
PSQL_USER = "postgres"
PSQL_PASS = "admin"
PSQL_DB = "gad"

# Connection
connection_address = """
host=%s port=%s user=%s password=%s dbname=%s
""" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
connection = psycopg2.connect(connection_address)

cursor = connection.cursor()

# Query
SQL = "SELECT * FROM categoria;"
cursor.execute(SQL)

# Get Values
all_values = cursor.fetchall()

cursor.close()
connection.close()

print('Get values: ', all_values)

##functions
def add_categoria(categoria_name):
    connection = psycopg2.connect(connection_address)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO categoria (nombre) VALUES(%s)", (categoria_name))
    connection.commit()
    cursor.close()
    connection.close()

#add_categoria(autos)