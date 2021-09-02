CREATE OR REPLACE FUNCTION Obtener_Respuestas() 
RETURNS table(img_name varchar,
			 cons_name varchar) as
$$
Begin
	RETURN QUERY
	select img.nombre as img_name, con.nombre as cons_name 
	from respuesta as res
	inner join imagen as img on (img.id = res.imagen_id)
	inner join consulta as con on (con.id = res.consulta_id);
end
$$ 
language 'plpgsql';


select Obtener_Respuestas()