# http_bach_sender

HTTP Bach Sender es una aplicación web para construir, gestionar y ejecutar peticiones HTTP a nivel de socket. Permite crear peticiones HTTP crudas, editarlas con caracteres de control, enviarlas mediante conexiones TCP directas (con soporte TLS), y examinar las respuestas en su formato original.

A diferencia de un navegador o un cliente HTTP convencional, este proyecto envía el texto exacto de la peticion sobre el socket sin intermediarios. Esto lo hace util para auditoria de seguridad, depuracion de protocolos, pruebas de APIs, o cualquier escenario donde se necesite control total sobre la peticion HTTP.

---

## Funcionalidades

- **Cola de peticiones** -- Lista todas las peticiones creadas con su metodo, dominio y ruta. Permite seleccionar, editar o eliminar peticiones individuales, asi como borrar la cola completa.

- **Editor de peticiones crudas** -- Un area de texto donde se escribe la peticion HTTP manualmente con soporte para secuencias de escape:
  - `\r` -- retorno de carro (CR, 0x0D)
  - `\n` -- nueva linea (LF, 0x0A)
  - `\t` -- tabulador horizontal (HT, 0x09)
  - `\0` -- caracter nulo (NUL, 0x00)
  - `\x1B` -- escape (ESC, 0x1B)
  - `\x7F` -- delete (DEL, 0x7F)
  - `\xHH` -- cualquier byte en hexadecimal (00-FF)
  - Insercion de caracteres personalizados mediante codigo hexadecimal
  - Copia del texto raw al portapapeles

- **Ejecucion por sockets** -- Envia cada peticion mediante una conexion TCP raw. Para dominios HTTPS establece una capa TLS. Las conexiones se reutilizan por dominio para evitar handshakes innecesarios.

- **Soporte de codificacion de contenido** -- Descomprime automaticamente respuestas comprimidas con gzip, deflate, brotli, zstd, bzip2, lzma y xz.

- **Visualizacion de respuestas** -- Muestra todas las respuestas recibidas con su codigo de estado HTTP. Permite inspeccionar el texto completo de cada respuesta.

---

## Arquitectura

```
Navegador (Interfaz)
       |
       v
Django (Backend)
       |
       +-- SQLite (Base de datos)
       |
       v
socket_sender.py (Motor de sockets)
       |
       +-- TCP Socket (HTTP)
       +-- TLS Socket (HTTPS)
       |
       v
Servidor destino
```

El flujo de trabajo es:

1. El usuario crea peticiones HTTP en el editor, escribiendo el texto exacto que desea enviar (primera linea, encabezados, cuerpo).
2. Las peticiones se guardan en la base de datos SQLite.
3. Al ejecutar, el backend lee todas las peticiones pendientes y las envia mediante sockets TCP/TLS al servidor correspondiente.
4. Las respuestas recibidas se almacenan junto con el codigo de estado.
5. El usuario puede inspeccionar cada respuesta en la pagina de resultados.

---

## Instalacion

### Requisitos

- Python 3.10 o superior
- Node.js (para Tailwind CSS, opcional si se usa el CSS precompilado)

### Pasos

1. Clonar el repositorio:

   ``git clone <repositorio>``
   ``cd http_bach_sender``

2. Ejecutar el script de inicio:

   **Windows:**

   ``iniciar.cmd``

   **Linux / macOS:**

   ``chmod +x iniciar.sh``
   ``./iniciar.sh``

   El script crea un entorno virtual, instala las dependencias, ejecuta las migraciones, y levanta el servidor en ``http://localhost:8000``.

### Instalacion manual

   ``python -m venv venv``
   ``venv\Scripts\activate`` (Windows) o ``source venv/bin/activate`` (Unix)
   ``pip install -r requeriments.txt``
   ``python manage.py migrate``
   ``python manage.py runserver``


## Uso

### 1. Crear una peticion

Desde la pagina principal (Cola de Peticiones), hacer clic en "ANADIR". Se abre el editor donde se debe:

1. Escribir el dominio completo (ej. ``https://ejemplo.com``).
2. En el area de texto, escribir la peticion HTTP comenzando con el metodo y la ruta:
   ``GET /api/recurso HTTP/1.1``
   ``Host: ejemplo.com``
   ``\r\n``

   Los caracteres de control como ``\r`` y ``\n`` se escriben como secuencias de escape y el editor los interpreta como los bytes reales CR (0x0D) y LF (0x0A).

3. Hacer clic en "GUARDAR".

### 2. Editar peticiones existentes

En la cola de peticiones, seleccionar una fila y hacer clic en "EDITAR PETICION". El editor carga la peticion guardada con todas sus secuencias de escape.

### 3. Ejecutar peticiones

En la cola de peticiones, hacer clic en "EJECUTAR". El sistema envia todas las peticiones pendientes mediante sockets y redirige a la pagina de respuestas.

### 4. Ver respuestas

En la pagina de respuestas, la tabla muestra cada peticion con su codigo de estado HTTP. Al hacer clic en una fila se muestra el texto completo de la respuesta recibida.

---

## Estructura del proyecto

```
http_bach_sender/
|
+-- core/                    Aplicacion principal
|   +-- models.py            Modelo Peticiones
|   +-- views.py             Vistas (cola, editor, resultados, ejecucion)
|   +-- urls.py              Rutas de la aplicacion
|   +-- templates/           Plantillas HTML
|   |   +-- editor.html      Editor de peticiones
|   |   +-- solicitudes.html Cola de peticiones
|   |   +-- respuestas.html  Visualizacion de respuestas
|   +-- utils/
|       +-- socket_sender.py Motor de envio por sockets TCP/TLS
|
+-- http_bach_sender/        Configuracion del proyecto Django
|   +-- settings.py          Configuracion general
|   +-- urls.py              Rutas raiz
|
+-- tema/                    Tema Tailwind CSS + daisyUI
|
+-- iniciar.cmd              Inicio rapido (Windows)
+-- iniciar.sh               Inicio rapido (Unix)
+-- requeriments.txt         Dependencias Python
```

---

## Componentes clave

### socket_sender.py

El nucleo del proyecto. Abre conexiones TCP raw a los servidores destino y envia el texto exacto de la peticion. Para HTTPS establece una capa TLS con verificacion de certificados. Gestiona la reutilizacion de conexiones por dominio para optimizar el envio multiple.

Soporta descompresion de los siguientes formatos: gzip, deflate, brotli, zstd, bzip2, lzma, xz.

### Editor de peticiones

El editor permite trabajar con bytes arbitrarios mediante un sistema de escape/unescape. El usuario escribe secuencias como ``\r`` o ``\x1B`` en el area de texto, y el sistema las convierte a los bytes reales antes de enviarlas al backend. A la inversa, al cargar una peticion guardada, los bytes de control se muestran como secuencias de escape legibles.

---

## Tecnologias

- **Django 6.0** -- Framework web
- **SQLite** -- Base de datos
- **Tailwind CSS v4 + daisyUI v5** -- Interfaz de usuario
- **Python sockets + ssl** -- Conexiones de red
- **brotli, zstandard, lzma, bz2** -- Descompresion de respuestas

---

## Notas

- La aplicacion no incluye autenticacion ni autorizacion. Esta disenada para entornos locales o de pruebas.
- No se utiliza CSRF middleware. Las peticiones POST se realizan mediante fetch sin token CSRF.
- El reemplazo de ``\n`` por ``\r\n`` se aplica automaticamente debido a que los navegadores normalizan los saltos de linea en los campos de texto.
- El proyecto no esta afiliado con PortSwigger ni con ninguna plataforma de seguridad. Los datos de ejemplo con dominios de academias de seguridad son solo ilustrativos.
