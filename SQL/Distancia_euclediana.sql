
CREATE OR REPLACE FUNCTION DistanciaEuclidiana(x float[], y float[]) RETURNS float AS --ej e (ver como devolver en diferentes campos)
$$
Declare
sum float = 0;

Begin
for i in 1..array_length(x,1) LOOP

sum = sum + power((x[i] - y[i]),2);


END LOOP;



return sqrt(sum);

 
End
$$
language 'plpgsql'; 


select DistanciaEuclidiana(array[3,4],array[0,0])

select DistanciaEuclidiana('{1.25,2.45}'::float[],'{-3.56,1.67}'::float[])
