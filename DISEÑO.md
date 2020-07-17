## Qué se necesita a nivel de diseño

La base del juego es que son cartas de paises, de un lado con la bandera, y del otro lado con mucha info sobre ese país (para más info, ver estas [instrucciones](INSTRUCCIONES.md)).

A nivel de diseño, es muy distinto lo que hay que hacer de cada lado de la carta.

La parte de adelante realmente es un 90% bandera, entonces quizás se podría decorar apenas ese borde blanco, quizás con un fondo suavecito. Son [estas](https://github.com/facundobatista/flagsy/blob/master/final-front.pdf).

La parte que tiene todo el contenido es realmente la parte de atrás. Acá hay donde hay que hacer mucho diseño. Las partes de atrás son [estas](https://github.com/facundobatista/flagsy/blob/master/final-back.pdf).

La complejidad de la parte de atrás es que no sólo quede lindo y elegante, sino también poder meter toda la info de los distintos paises. Algunos tienen nombres muy largo. Algunos tienen dos idiomas, otros tienen ocho. Algunos tienen una capital de nombre corto, otros tienes varias capitales.

Entonces hay que ver cómo acomodar toda esa diversidad de información. En [esta tabla](https://github.com/facundobatista/flagsy/blob/master/art/generated-es-countries_data.csv) está toda la info.

El diseño hay que plasmarlo en dos SVGs con variables para reemplazar toda la info. Estos son los que hice yo, para [atrás](https://github.com/facundobatista/flagsy/blob/master/art/card-back.svg) y para [adelante](https://github.com/facundobatista/flagsy/blob/master/art/card-front.svg). Son feos, pero son funcionales en el sentido en que toda la info entra acomodada.

A partir de esos SVGs se generan todos los PDFs finales. Así que sólo se necesitan esos dos SVGs.

Habiendo dicho eso, si a nivel diseño se necesitan más de un SVG para la parte de atrás, eso se puede hacer, lo tenemos que coordinar y listo (ejemplo, un SVG genérico que sirve para el 90% de los paises, pero otro distinto para aquellos con nombre muy largo, y otro más para los que tienen muchos gentilicios o idiomas).
