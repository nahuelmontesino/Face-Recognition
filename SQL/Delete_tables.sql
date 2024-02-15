DO $$
DECLARE
    table_name text;
BEGIN
    -- Tabla 2
    DELETE FROM respuesta; -- Cambia 'tabla2' al nombre de tu segunda tabla
	
	-- Tabla 1
    DELETE FROM consulta; -- Cambia 'tabla1' al nombre de tu primera tabla
	
	-- Tabla 2
    DELETE FROM imagen; -- Cambia 'tabla2' al nombre de tu segunda tabla

    -- Continúa con tantas tablas como necesites...
END $$;