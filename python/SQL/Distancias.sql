CREATE OR REPLACE FUNCTION Distancias(vector_entrada float[]) 
RETURNS table (
	name varchar,
	distancia float) as
$$
Declare

rec record;

Begin 
	FOR REC in (select nombre, vector from imagen) LOOP
		distancia := DistanciaEuclidiana(vector_entrada, rec.vector);
		name := rec.nombre;
		RETURN NEXT;
	END LOOP;
	
	--return;
--nombres;
	
End;
$$
language 'plpgsql';

select name from Distancias(array[1,1])