   CREATE TABLE imagen(
   id SERIAL,
   nombre VARCHAR(100),
   vector float[],
	
   PRIMARY KEY(id));

CREATE TABLE consulta(
   id SERIAL,
   vector float[],
   path VARCHAR(100),
   respuesta_correcta int,
   
   PRIMARY KEY(id),
   FOREIGN KEY (respuesta_correcta) REFERENCES imagen(id));

CREATE TABLE respuesta(
id SERIAL,
distancia float,
acierto boolean,
consulta_id int,
imagen_id int,

PRIMARY KEY (id),
FOREIGN KEY (consulta_id) REFERENCES consulta(id),
FOREIGN KEY (imagen_id) REFERENCES imagen(id));

