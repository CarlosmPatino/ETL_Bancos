🏦 Pipeline ETL: Bancos Más Grandes del Mundo por Capitalización de Mercado

Este proyecto implementa un sistema automatizado de ETL (Extract, Transform, Load) que compila una lista actualizada de los 10 bancos más grandes del mundo clasificados por capitalización de mercado (en miles de millones de dólares).

Extrayendo datos con Webscraping



🚀 Flujo del Pipeline

1️⃣ Extracción (Extract)

Se obtiene la lista de los bancos más grandes por capitalización de mercado mediante web scraping desde una fuente confiable.

Se carga el archivo CSV con los tipos de cambio proporcionados.

2️⃣ Transformación (Transform)

Se limpian y estructuran los datos en un DataFrame de Pandas.

Se convierte la capitalización de mercado de USD a GBP, EUR e INR, utilizando los tipos de cambio del archivo CSV.

Se ordenan los bancos de mayor a menor capitalización de mercado.

3️⃣ Carga (Load)

Se guarda la tabla procesada en un archivo CSV localmente.

Se almacena la tabla en una base de datos SQL para futuras consultas y análisis.

🛠 Tecnologías Utilizadas

Python 3.11.9

Pandas – Manipulación y transformación de datos.

BeautifulSoup & Requests – Web scraping de la fuente de datos.

NumPy – Conversión de divisas y cálculos.

SQLite / PostgreSQL – Almacenamiento en base de datos.
