Script Python, para realizar scraping a las publicaciones más recientes de la pagina oficial del BOE.
El scraping se realiza mediante la API "Scrapy".
Para lanzar el script hay que ejecutar el comando en el "cmd" y ubicándolo en la carpeta donde se encuentra el script "scrapy.BOE.py": "scrapy runspider scrapyBOE.py -o nombre.json"

Si observamos el contenido de la carpeta encontramos tres archivos:
1--Leéme.txt
2-nombres-2015.csv
3-scrapyBOE.py

El primero archivo es Leéme que se encuentra leyendo ahora mismo.

El segundo es un dataset de libre acceso, que contiene todos los nombres de personas físicas censados en españa en 2015, proporcionado por el gobierno de españa.
Dicho dataset se utiliza para comprobar que efectivamente los nombres recogidos mediante scraping despues de la palabra clave "FIRMADO" son nombres autenticos.
Y evitar que se scrapee por ejemplo: "La Ministra de Cultura" y se guarde como si fuera un nombre real de una persona física.

Y el tercer archivo es el script que realiza scraping mediante la API "Scrapy"

Resumen de como funciona el script:
Gracias a la API "Scrapy" se scrapea facilmente el Id y la descripcion mediante "XPATH".
Para obtener las localizaciones, el sript tiene una matriz con todas las provincias de españa, dichas provincias estan ordenadas por orden alfabético y clasificadas por filas.
Por lo que en la primera fila estan todas las provincias que empiezan por la letra "a" en la segunda fila las provincias que empiezan por la letra "b" y asi sucesivamente.
El script obtiene todo el texto que se encuentra en "Url" y comprueba palabra por palabra por que letra empieza, si empieza por una de las letras en las que empizan las provincias españolas.
Se busca directamente fila que pertenece a dicha letra en la matriz de provincias españolas.
Yendo directamente a buscar a la fila por donde empieza la palabra, y evitando asi una busqueda por toda la matriz de provincias.

Para obtener los nombres, gracias a la API "Scrapy" se puede buscar si existe un "XPATH" que empiece por "firma_" y obtener asi todo el texto que se encuentra en dicho "XPATH",
despues para asegurarse que que dicho texto es perteneciente a un nombre real de una persona fisica, se comprueba con la el dataset y si existe en el dataset quiere decir que el nombre es real y debe ser scrapeado.
