CREATE OR REPLACE FUNCTION Distancias(vector_entrada float[]) 
--Obtiene la distancia de un vector de entrada a cada una de las imagenes en la tabla imagen
RETURNS table (
	id int, 
	name varchar,
	distancia float) as
$$
Declare

rec record;

Begin 
	FOR REC in (select * from imagen) LOOP
		distancia := DistanciaEuclidiana(vector_entrada, rec.vector);
		name := rec.nombre;
		id := rec.id;
		RETURN NEXT;
	END LOOP;
	
End;
$$
language 'plpgsql';


select name from Distancias(array[1,1])