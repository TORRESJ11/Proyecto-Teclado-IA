# Proyecto-Teclado-IA
Entregable para el proyecto del teclado de IA

Aquí dejo la carpeta con los elementos de mi teclado de selección por mano

Instrucciones para la instalación y ejecución del proyecto

Para facilitar la distribución e instalación del proyecto, se sugiere alojarlo en un repositorio de GitHub. Desde allí, cualquier usuario con conocimientos básicos puede descargarlo y ponerlo en funcionamiento. A continuación se detallan los pasos para clonar el repositorio, configurar el entorno y ejecutar el sistema completo.

Primero, es necesario contar con algunas herramientas instaladas en el sistema, como Python 3.10 o superior, Git, y pip (el gestor de paquetes de Python). También se recomienda tener instalado un entorno virtual para gestionar las dependencias de manera aislada.

Una vez cubiertos los requisitos previos, se debe abrir una terminal y clonar el repositorio usando el comando git clone, seguido de la URL del repositorio. Luego, se ingresa al directorio del proyecto con el comando cd.

El siguiente paso es la creación de un entorno virtual. Esto se hace mediante el comando python -m venv env, lo que genera una carpeta env que contendrá las versiones locales de Python y los paquetes necesarios. Para activarlo, se debe ejecutar .\env\Scripts\activate en Windows o source env/bin/activate en Mac y Linux.

Una vez activado el entorno, se procede a instalar las dependencias del proyecto mediante el comando pip install -r requirements.txt, el cual lee las bibliotecas listadas en el archivo correspondiente (como OpenCV, MediaPipe y Pygame).

Con las bibliotecas instaladas, el siguiente paso es entrenar el modelo de predicción de texto. Para ello, se debe contar con un archivo corpus.txt, el cual contiene una serie de frases y prefijos que alimentarán al modelo de trigramas. El entrenamiento se realiza ejecutando el archivo entrenar_trigramas.py, el cual genera un archivo modelo_trigramas.pkl que será usado por el teclado para sugerir autocompletados.

También se debe incluir un archivo de sonido en formato .wav llamado click.wav, que representa el efecto sonoro al seleccionar una tecla. Este archivo debe colocarse en el mismo directorio que el script principal.

Una vez entrenado el modelo y con los archivos preparados, se ejecuta el teclado con el comando python teclado_mano_avanzado.py. El sistema accede a la cámara y muestra el teclado virtual en pantalla. El usuario puede interactuar con el teclado mediante el movimiento de su mano, utilizando el índice como puntero. Para seleccionar una tecla, basta con mantener la punta del dedo índice sobre la misma por un segundo. Si se abre la palma completamente, el texto escrito se borra.

El sistema también muestra sugerencias de palabras debajo del texto actual, basadas en las primeras letras escritas. Estas sugerencias se despliegan en una pequeña ventana justo debajo de la palabra incompleta, y pueden ser seleccionadas usando el mismo gesto sobre la zona de la sugerencia.

Gracias a esta arquitectura modular, el sistema puede ser fácilmente extendido, mejorado y personalizado, permitiendo así su integración en proyectos educativos, de accesibilidad, o interfaces sin contacto físico.

Windows: python -m venv env .\env\Scripts\activate

macOS/Linux: python3 -m venv env source env/bin/activate

pip install -r requirements.txt

Asegúrate de tener un archivo corpus.txt con frases y prefijos.

Ejecuta el script de entrenamiento: python entrenar_trigramas.py

Asegúrate de tener el archivo de sonido click.wav en el mismo directorio que el script teclado_mano_avanzado.py. Puedes usar cualquier efecto corto de clic en formato .wav.

Una vez entrenado el modelo y configurado el entorno, ejecuta el teclado: python teclado_mano_avanzado.py

Funcionalidades Clave Control por gestos (índice como puntero).

Borrado por gesto de palma abierta.

Selección de teclas tras 1 segundo de enfoque.

Reproducción de sonido al seleccionar una tecla.

Predicción de palabras por trigramas o prefijos.

Sugerencias visibles justo debajo de la palabra en edición.

Casos de Prueba Escribir palabras completas letra por letra.

Mantener el dedo índice sobre una letra durante un segundo.

Probar el gesto de la palma abierta para borrar todo.

Escribir las primeras letras de una palabra y seleccionar una sugerencia emergente

Posibles Mejoras Futuras Uso de modelos de lenguaje más potentes (como BERT o Transformers livianos).

Reconocimiento multi-mano o para personas zurdas.

Interfaz gráfica con botones clicables con mouse.

Personalización del teclado (idioma, disposición, colores).

Inclusión de puntuación y teclas especiales.
