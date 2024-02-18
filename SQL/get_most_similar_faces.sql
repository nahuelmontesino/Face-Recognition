CREATE OR REPLACE FUNCTION Obtener_Respuestas() 
RETURNS table(img_name varchar, cons_name varchar, distancia float) as
$$
Begin
	RETURN QUERY
	select img.nombre as img_name, con.nombre as cons_name, res.distancia as distancia
	from respuesta as res
	inner join imagen as img on (img.id = res.imagen_id)
	inner join consulta as con on (con.id = res.consulta_id);
end
$$ 
LANGUAGE 'plpgsql';


select Obtener_Respuestas()