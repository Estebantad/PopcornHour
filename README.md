PopcornHour: Tu Portal de Cine y Series
Descripción del Proyecto
PopcornHour es un portal web interactivo diseñado para entusiastas del cine y las series. Permite a los usuarios descubrir nuevas producciones, compartir sus opiniones a través de calificaciones y comentarios, y participar en discusiones enriquecedoras. La plataforma distingue entre dos tipos de usuarios: Moderadores, quienes tienen la capacidad de subir y gestionar el catálogo de películas y series, y Estándares, quienes pueden interactuar con el contenido existente calificándolo, comentando y discutiendo.

Características Principales
Exploración de Contenido: Descubre una amplia variedad de películas y series.

Calificaciones Personalizadas: Califica tus títulos favoritos y mira las puntuaciones de otros.

Discusiones Activas: Comenta en películas/series y participa en conversaciones con la comunidad.

Roles de Usuario:

Estándar: Acceso a calificación, comentarios y visualización de contenido.

Moderador: Gestión completa del catálogo de películas y series.

Estructura del Proyecto
La aplicación está construida utilizando el microframework Flask de Python, persistiendo los datos en una base de datos PostgreSQL. La estructura de directorios está organizada para una clara separación de preocupaciones:

popcorn_hour_app/
├── app/
│   ├── static/         # Archivos estáticos (CSS, JS, imágenes de diseño)
│   │   ├── css/        # Hojas de estilo CSS
│   │   ├── images/     # Imágenes de la interfaz (ej. logos, iconos)
│   ├── templates/      # Plantillas HTML con Jinja2 para las vistas
│   ├── __init__.py     # Inicialización de la aplicación Flask y extensiones
│   ├── models.py       # Definición de los modelos de base de datos (SQLAlchemy)
│   ├── routes.py       # Lógica de las rutas (URLs) y controladores
│   ├── forms.py        # Clases de formularios web (Flask-WTF)
│   └── (otros módulos)
├── config.py           # Configuración de la aplicación (conexión a DB, claves)
├── run.py              # Script principal para iniciar la aplicación
├── venv/               # Entorno virtual de Python con las dependencias
├── requirements.txt    # Lista de todas las dependencias de Python
├── README.md           # Este archivo
└── documentation/      # Carpeta para entregables de documentación
    └── db/             # Esquema Entidad-Relación de la base de datos

Instalación y Ejecución del Proyecto
Sigue estos pasos para poner en marcha PopcornHour en tu entorno local:

Clona el Repositorio:

git clone https://github.com/Estebantad/PopcornHour.git
cd popcorn_hour_app

Crea y Activa un Entorno Virtual:
Es una buena práctica aislar las dependencias de tu proyecto.

python3 -m venv venv
# En macOS/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate.bat

Instala las Dependencias:

pip install -r requirements.txt

Configura tu Base de Datos PostgreSQL:

Asegúrate de tener PostgreSQL instalado y ejecutándose.

Crea una base de datos llamada popcorn_hour_db (por ejemplo, usando PgAdmin).

Muy importante: Abre config.py y actualiza SQLALCHEMY_DATABASE_URI con el nombre de usuario y contraseña correctos de tu PostgreSQL.

Ejecuta la Aplicación:
Al ejecutar run.py por primera vez, SQLAlchemy creará automáticamente todas las tablas de la base de datos definidas en app/models.py.

python run.py

Uso
Una vez que la aplicación esté en funcionamiento, ábrela en tu navegador web visitando:
http://127.0.0.1:5000/

Contribución
¡Las contribuciones son bienvenidas! Si deseas mejorar PopcornHour:

Haz un "fork" del repositorio.

Crea una nueva rama para tu característica (git checkout -b feature/nombre-de-tu-caracteristica).

Realiza tus cambios y haz "commit" (git commit -m "Descripción breve de los cambios").

Sube tu rama (git push origin feature/nombre-de-tu-caracteristica).

Abre un "Pull Request".

Contacto
Esteban Arias
tonatiuh112001@gmail.com