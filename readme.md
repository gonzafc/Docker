Bienvenido a mi repositorio dedicado al seguimiento y desarrollo de los ejercicios prácticos de la materia Docker.

Aquí encontrarás todos los archivos, configuraciones (Dockerfile) y scripts necesarios para el despliegue de las soluciones abordadas durante el curso.

🛠️ Contenido del Repositorio
Ejercicios Prácticos: Implementación de contenedores basados en imágenes de Nginx y otras tecnologías.

Configuraciones: Archivos Dockerfile utilizados para la creación de imágenes personalizadas.

Documentación: Registro del proceso de aprendizaje sobre el ciclo de vida de los contenedores (run, stop, rename, rm).

🚀 Cómo utilizar este repositorio
Clonar el repositorio:

Bash
git clone https://github.com/gonzafc/Docker.git
Construir las imágenes:
Dentro de la carpeta de cada ejercicio, ejecuta:

Bash
docker build -t nombre_de_imagen:etiqueta .
Ejecutar los contenedores:

Bash
docker run -d -p 8081:80 --name nombre_contenedor nombre_de_imagen:etiqueta
👨‍💻 Autor
Gonzalo Romero
Estudiante de la carrera de Ingeniería en Sistemas - Universidad Autónoma de Entre Ríos (UADER).

Este proyecto forma parte de mi formación académica y profesional.
