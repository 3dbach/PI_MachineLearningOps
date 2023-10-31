# PIMlops
Proyecto Individual Machine Learnig Ops


[![1143164-3840x2160-desktop-4k-robot-background-image.jpg](https://i.postimg.cc/P5JHbCCq/1143164-3840x2160-desktop-4k-robot-background-image.jpg)](https://postimg.cc/w7CngTcK)


API de Juegos de Steam
Este proyecto proporciona una API construida con FastAPI para analizar y obtener información sobre juegos de Steam y sus reseñas. La API es capaz de desglosar información basada en diferentes parámetros, permitiendo a los usuarios obtener insights valiosos sobre la dinámica del mercado de juegos y las percepciones de los usuarios.

Tabla de Contenidos
Características
Instalación
Uso
Documentación de la API
Conjuntos de Datos
Contribución
Licencia
Contacto
Características
La API ofrece las siguientes rutas y funcionalidades:

Ruta Raíz (/): Devuelve un mensaje de bienvenida, indicando que la API está activa y funcionando correctamente.

Ruta Developer (/developer/{desarrollador}): Dado un nombre de desarrollador, esta ruta devuelve información detallada sobre los juegos lanzados por ese desarrollador, incluyendo la cantidad de juegos lanzados por año y el porcentaje de esos juegos que son gratuitos.

Ruta Best Developer Year (/best_developer_year/{año}): Al proporcionar un año específico, esta ruta devuelve los tres principales desarrolladores que tienen la mayoría de las reseñas recomendadas para ese año.

Ruta Developer Reviews Analysis (/developer_reviews_analysis/{desarrolladora}): Dada una desarrolladora, esta ruta devuelve un análisis detallado de las reseñas de los juegos desarrollados por esa empresa, clasificadas en positivas y negativas.

Instalación
Para instalar y ejecutar esta API en tu máquina local, sigue los siguientes pasos:

Clonar el Repositorio:
git clone [URL-del-repositorio]
cd [nombre-del-repositorio]

Instalar Dependencias:
Asegúrate de tener pip instalado y ejecuta:
pip install -r requirements.txt

Ejecutar la API:

uvicorn main:app --reload

Con estos pasos, la API debería estar ejecutándose en http:

Uso
Después de instalar y ejecutar la API, puedes interactuar con ella directamente a través de la URL mencionada anteriormente o utilizando herramientas como curl o Postman.

Documentación de la API
FastAPI proporciona una interfaz de usuario interactiva para la documentación de la API. Una vez que la API esté en ejecución, puedes acceder a esta documentación visitando http://127.0.0.1:8000/docs en tu navegador. Aquí, podrás ver todos los endpoints disponibles, los parámetros que aceptan y probarlos en tiempo real.

Conjuntos de Datos
Este proyecto utiliza varios archivos CSV que contienen información sobre juegos de Steam y sus reseñas. Los datos han sido recopilados y limpiados para adaptarse a las necesidades de esta API. Si deseas conocer más sobre la fuente original de los datos o cómo se recolectaron, por favor contáctame.

Contribución
Las contribuciones al proyecto son bienvenidas. Si encuentras un error o ves una mejora potencial, no dudes en abrir un issue para discutirlo. Si decides aportar con código, por favor abre un pull request. Asegúrate de describir en detalle los cambios propuestos y su motivo.

Licencia
Este proyecto está bajo la licencia MIT.

Contacto
Para cualquier comentario, pregunta o sugerencia, puedes contactarme a través de:

GitHub: @[ ]
Email: [ag_omarb@hotmail.com]
