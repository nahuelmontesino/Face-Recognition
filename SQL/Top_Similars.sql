CREATE OR REPLACE FUNCTION TopSimilars(vector_entrada float[]) 
RETURNS table (
	name varchar,
	distancia float) as
$$
Declare
rec record;
Begin 
	FOR REC in 
			(select * from Distancias(vector_entrada)
			order by distancia desc
			limit 10) LOOP
		name := rec.name;
		distancia:= rec.distancia;
		RETURN NEXT;
	END LOOP;
End
$$
language 'plpgsql';

select TopSimilars(array[1,2,3])