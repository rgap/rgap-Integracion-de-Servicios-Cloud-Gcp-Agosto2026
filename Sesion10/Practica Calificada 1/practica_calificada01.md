# Práctica Calificada 1 — Despliegue de una landing ecommerce

Actua como un sysadmin responsable de preparar el servidor de una tienda ecommerce. En este simulador asumirás el turno de implementación: recibirás una aplicación desarrollada por otro equipo, configurarás su entorno, comprobarás las comunicaciones y entregarás el servicio funcionando con evidencias verificables.

## 1. Caso de estudio: el lanzamiento de ESTAMPA

Estampa es un emprendimiento de polos temáticos que prepara su tienda en línea. Mientras el equipo de desarrollo termina el catálogo, el negocio necesita una landing page que anuncie que el sitio está en construcción y permita solicitar cotizaciones por WhatsApp.

Los desarrolladores ya codificaron y entregaron [ecommerce_webapp](ecommerce_webapp/). Tu objetivo como administrador de sistemas (SysAdmin) es **desplegar esa aplicación en una VM Ubuntu y publicarla para los clientes de la red local mediante Nginx**, con Python funcionando detrás del servidor web. Debes demostrar cómo viajan las solicitudes y cómo se administran los procesos, permisos y reglas de acceso.

El enunciado se organiza en partes, pero las implementaciones y pruebas deben ejecutarse realmente. Una explicación hipotética, una captura de los diagramas proporcionados o una respuesta generada por IA no reemplazan un servicio funcionando.

### Condiciones de la práctica

- Utiliza `server.py`, `static/index.html` y `static/style.css` del proyecto entregado. Conserva su funcionalidad y diseño; configura el despliegue mediante variables de entorno y archivos de administración.
- Esta entrega no incluye catálogo, carrito, pagos, panel de administración ni base de datos. No debes instalar MySQL para esta landing.
- El entorno de evaluación será una VM Ubuntu con adaptador puente y un cliente en el equipo físico, denominado `PC_HOST`.
- La publicación final será `http://VM_IP/`, en la red local. No se exige dominio, HTTPS del sitio, despliegue en GCP ni apertura de puertos en el router hacia Internet.
- Implementa todas las operaciones de los cinco diagramas de esta carpeta mediante las etapas indicadas. Los escenarios son sucesivos: no deben competir por el puerto `8000`.
- Puedes adaptar los ejemplos de clase y utilizar herramientas de asistencia. Debes comprender, explicar y comprobar lo que ejecutes.

## 2. Material previo que debes aplicar

Consulta las sesiones 00 a 10, sus ejemplos y respuestas disponibles, además de la `tarea` de análisis de flujo de red. La siguiente relación establece cómo se aplican al caso:

| Material | Aplicación en esta práctica |
| --- | --- |
| [Sesion00](../../Sesion00/slides/build/slides.pdf) | Contexto del curso, soluciones cloud y relación entre sistemas, GCP y automatización. Vincula este panorama con los fundamentos aplicados en el laboratorio. |
| [Sesion01](../../Sesion01/slides/build/slides.pdf) | Roles, cliente y servidor, servicios, puertos y asignación de recursos de una VM. |
| [Sesion02](../../Sesion02/slides/build/slides.pdf) | Tipo de hipervisor, virtualización, diseño y justificación de arquitectura. |
| [Sesion03_Sesion04](../../Sesion03_Sesion04/slides/build/slides.pdf) | Las sesiones 03 y 04 se dictaron con un solo archivo de diapositivas. Ubuntu, terminal, shell, sistema de archivos, identificación del sistema y paquetes con `apt`. |
| [Sesion05](../../Sesion05/slides/build/slides.pdf) | Interfaces, IP, rutas, DNS, direcciones de escucha, `systemctl`, alias y funciones persistentes. |
| [Sesion06](../../Sesion06/slides/build/slides.pdf) | Herramientas de edición y asistencia, obtención de datos reales, observación del tráfico y representación del recorrido de red. |
| [Sesion07](../../Sesion07/slides/build/slides.pdf) | Cliente y servidor TCP en Python, petición HTTP y lectura de una respuesta. |
| [Sesion08](../../Sesion08/slides/build/slides.pdf) | Ciclo de vida de servicios, Nginx, UFW y prueba de bloqueo por IP. |
| [Sesion09](../../Sesion09/slides/build/slides.pdf) | Proxy inverso, cuentas, permisos y configuración. |
| [Sesion10](../../Sesion10/slides/build/slides.pdf) | Diferencia entre servidor web y servidor de aplicaciones; elección del entorno de trabajo desde el que administras la VM. |
| [Tarea de análisis de flujo de red](../../tarea/Tarea%20-%20Analisis%20de%20Flujo%20de%20Red.md) | Modo puente, datos reales de red, DNS, salida a Internet, NAT del router y diagramas de secuencia y bloques. |

Utiliza la terminal de tu sistema como cliente y documenta el entorno que empleas. La VM Ubuntu en modo puente sigue siendo el servidor del caso. Explica esta elección con lo visto en la sesión 10.

## 3. Diagramas que debes llevar a la práctica

> **Sobre `0.0.0.0` y `127.0.0.1`:** en las tablas y partes siguientes, `0.0.0.0` no es la dirección de ningún equipo, sino una dirección de escucha que significa «aceptar conexiones por todas las interfaces de red de la VM»; por eso los clientes se conectan usando la IP real de la VM (`VM_IP`), no `0.0.0.0`. `127.0.0.1` es la dirección de loopback: un servicio que escucha ahí solo es accesible desde la propia VM.

| Referencia                                         | Implementación y comprobación obligatoria                                                                                                                                                                         |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [2026-09-10_15-10-25.jpg](2026-09-10_15-10-25.jpg) | Servidor TCP Python en `0.0.0.0:8000`; cliente en `PC_HOST`; envío de `Hola` y respuesta `Hola PC`.                                                                                                               |
| [2026-09-10_15-11-09.jpg](2026-09-10_15-11-09.jpg) | En la misma demostración, identificar la dirección y el puerto de escucha del servidor, la conexión aceptada, el puerto efímero del cliente y la conexión TCP que transporta ambos mensajes.                      |
| [2026-09-10_15-11-38.jpg](2026-09-10_15-11-38.jpg) | Verificar el orden: solicitud de conexión del cliente → establecimiento de la conexión TCP → aceptación en el servidor → intercambio de los dos mensajes, incluyendo la respuesta recibida en el cliente. Puede sustentarse con la misma ejecución de los dos diagramas anteriores. |
| [2026-09-10_15-13-23.jpg](2026-09-10_15-13-23.jpg) | Sustituir el servidor de saludo por `ecommerce_webapp`, accesible directamente en `VM_IP:8000`; realizar una petición HTTP y recibir el HTML de la landing.                                                       |
| [2026-09-10_15-16-01.jpg](2026-09-10_15-16-01.jpg) | Publicar Nginx en `VM_IP:80` y reenviar hacia Python en `127.0.0.1:8000`; demostrar los dos tramos TCP y el retorno de la respuesta.                                                                              |

**Adaptación al código recibido:** los diagramas HTTP usan `GET /productos` y HTML de productos como ejemplo. La aplicación entregada sirve la landing en `/` y `/index.html`, y su CSS en `/style.css`. Implementa el flujo con `GET /`; comprueba que `/productos` devuelve `404` y explica por qué. No inventes un catálogo ni cambies la aplicación para ocultar esa diferencia.

Utiliza el servidor HTTP incluido en la webapp, sin reescribirlo. Se evaluarán las pruebas de comunicación y sus resultados.

## 4. Actividades y capturas obligatorias

Ejecuta las partes en orden. Registra los comandos utilizados y sus resultados en un único informe, con capturas numeradas.

> **Qué son `E01`, `E02`, …:** son las **evidencias obligatorias** de la práctica. Cada `Exx` es un elemento concreto —normalmente una o varias capturas de pantalla con su pie explicativo— que demuestra que un requisito específico se ejecutó realmente y funcionó. Están numeradas de `E01` a `E20`, se citan al final de cada parte, se incorporan en el informe en el orden indicado en la sección 5 y se califican según la tabla de criterios de la sección 6. Una evidencia solo cuenta si es legible, indica si corresponde al host o a la VM y muestra el comando y su resultado (o la URL en el navegador).

### Parte 1 — Recibir el servidor e inventariar el entorno — 1 punto

1. Describe brevemente qué entrega desarrollo y qué debes resolver como sysadmin. Diferencia visitante, desarrollador y administrador.
2. Configura o reutiliza una VM Ubuntu. Registra hipervisor, tipo, versión de Ubuntu, CPU, RAM y disco asignados; justifica que los recursos caben en el equipo físico.
3. Configura el adaptador en modo puente sobre la interfaz física activa.
4. Identifica usuario, hostname, sistema operativo, shell y directorio de trabajo. Utiliza los comandos de las sesiones previas.
5. Crea un directorio de trabajo y copia la aplicación completa. Revisa su README, estructura y variables `HOST`, `PORT`, `WHATSAPP_NUMBER` y `WHATSAPP_MESSAGE`.
6. Actualiza el índice de paquetes e instala las herramientas necesarias: Python 3, Nginx, UFW, cliente HTTP y herramientas de observación de conexiones. El servidor recibido usa la biblioteca estándar de Python.

**E01:** configuración de la VM con recursos y modo puente visibles.

**E02:** identificación de Ubuntu y usuario, estructura de `ecommerce_webapp` y versiones de Python y Nginx.

### Parte 2 — Reconocer la red y comprobar la salida a Internet — 2 puntos

1. Obtén `VM_IP`, prefijo de red, interfaz activa y `ROUTER_IP` desde Ubuntu, mediante `ip addr` e `ip route` o comandos equivalentes.
2. Obtén `HOST_IP` desde el equipo físico. Comprueba con el prefijo que cliente y VM pertenecen a la misma subred.
3. Registra los siguientes datos con el comando o pantalla que sustenta cada uno:

   ```text
   HOST_IP =
   VM_IP =
   PREFIJO_RED =
   INTERFAZ_VM =
   ROUTER_IP =
   MODE = Bridged
   DEST_NAME = www.google.com
   DEST_IP =
   PROTOCOL =
   PORT =
   ```

4. Reproduce el análisis de `tarea`: resuelve el nombre de destino y realiza desde la VM una conexión HTTPS sobre TCP, por ejemplo con `curl -I https://www.google.com`. Observa el destino efectivo de esa conexión y su puerto; no copies la IP del ejemplo de clase.
5. Explica dónde intervienen DNS y el NAT de salida del router. No confundas el puente del hipervisor con el NAT del router. Puedes representar la dirección WAN como `IP pública`, sin registrar su valor.
6. Diferencia esa salida a Internet del acceso local `PC_HOST → VM`: en la misma subred no se necesita NAT ni una ruta por Internet para consultar la landing. Un `ping` no demuestra por sí solo que HTTP funcione.

**E03:** direcciones, prefijo, interfaz y ruta de la VM, junto con la IP del host.

**E04:** resolución de nombre y evidencia de la conexión HTTPS al destino real por TCP/443, mediante captura de tráfico o herramienta equivalente.

### Parte 3 — Reproducir los tres diagramas de comunicación TCP — 3 puntos

1. En archivos de laboratorio separados de la webapp, adapta los ejemplos de la sesión 07 para crear un servidor TCP de saludo y un cliente TCP.
2. En la VM, el servidor debe quedar a la escucha en `0.0.0.0:8000` y aceptar la conexión entrante del cliente.
3. En `PC_HOST`, el cliente debe conectarse a `VM_IP:8000`. Configura temporalmente el acceso necesario en UFW para ese origen y puerto.
4. Envía `Hola` desde el cliente; el servidor debe recibirlo y responder `Hola PC`; el cliente debe mostrar esa respuesta. Ambos mensajes deben viajar sobre la misma conexión aceptada.
5. Muestra las direcciones y puertos reales de ambos extremos mediante el programa o herramientas del sistema. Registra el puerto del cliente y el puerto de escucha del servidor.
6. Captura el tráfico de la prueba y guarda evidencia de la comunicación entre el cliente y el servidor.
7. Detén este servidor y comprueba que liberó el puerto `8000` antes de iniciar la webapp.

**E05:** terminal del servidor y terminal del cliente con los dos mensajes, las IP y los puertos reales.

**E06:** evidencia del servicio en escucha y de la comunicación entre el cliente y el servidor. Puedes mantener brevemente la conexión abierta para observarla con `ss`.

### Parte 4 — Desplegar la landing directamente en Python — 3 puntos

1. Inicia el proyecto entregado con Python 3 y las variables `HOST=0.0.0.0` y `PORT=8000`. Usa las variables de WhatsApp con valores de prueba identificados como tales. Coloca la configuración en un archivo `.env` junto a `server.py`: el servidor lo carga automáticamente al arrancar (las variables ya definidas en el entorno tienen prioridad).
2. Comprueba desde la VM qué proceso escucha en `8000` y en qué dirección.
3. Desde el navegador de `PC_HOST`, abre `http://VM_IP:8000/`. Debe verse Estampa, el anuncio de construcción, los estilos y los enlaces de cotización.
4. Desde el cliente, solicita `/`, `/index.html`, `/style.css` y `/productos`. Registra los códigos HTTP y el tipo de contenido. Para `/productos` el resultado esperado es `404`.
5. Adapta el cliente HTTP de la sesión 07 para solicitar `/` a `VM_IP:8000` sobre una conexión TCP. Envía una petición HTTP completa, con versión, cabecera `Host` y terminación de cabeceras; lee la respuesta completa y muestra estado, cabeceras y una porción del HTML.
6. Inspecciona el enlace generado de WhatsApp: verifica número y mensaje codificado. Basta inspeccionar el destino; no envíes mensajes.
7. Explica por qué `0.0.0.0` es una dirección de escucha y el navegador debe usar la IP real de la VM.

**E07:** landing desde el host, con la URL `http://VM_IP:8000/` visible, y proceso de escucha en la VM.

**E08:** respuestas HTTP de las cuatro rutas y respuesta recibida por el cliente HTTP de la sesión 07, incluyendo un fragmento reconocible de la landing.

**E09:** enlace de cotización generado con la configuración de prueba, sin marcadores `{{WHATSAPP_LINK}}` pendientes de sustituir.

### Parte 5 — Administrar usuarios, permisos y servicio — 2 puntos

1. Define una cuenta sin privilegios administrativos para ejecutar la aplicación. Documenta propietario, grupo y permisos de los archivos y directorios necesarios.
2. Mantén el archivo `.env` con las variables `HOST`, `PORT`, `WHATSAPP_NUMBER` y `WHATSAPP_MESSAGE` en el directorio de la aplicación, junto a `server.py` (el mismo que usaste en la parte 4). Es la única fuente de configuración del servicio: `server.py` lo carga al arrancar.
3. Aplica permisos mínimos al código y al archivo `.env`. No uses `chmod 777`.
4. Restringe el `.env` a las cuentas que necesiten leerlo (por ejemplo propietario administrativo y grupo del servicio, sin acceso para el resto). La cuenta del servicio debe poder leer el código, el `.env` y los recursos estáticos, y recorrer sus directorios. No necesita permisos administrativos para escuchar en `8000`.
5. Detén la ejecución manual y configura una unidad systemd para la aplicación, con usuario, directorio de trabajo y comando de inicio que invoque directamente Python 3 con la ruta de `server.py`. `server.py` carga el `.env` que está junto a él, así que no necesitas declarar variables en la unidad. El nombre del servicio debe quedar registrado en el informe.
6. Cambia en el `.env` el backend a `HOST=127.0.0.1` y `PORT=8000`, como requiere la arquitectura final, y reinicia el servicio.
7. Demuestra inicio, consulta de estado, parada, reinicio y habilitación al arranque. Diferencia `start` de `enable`, y `restart` de `reload`; no presupongas que tu unidad Python soporta recarga.
8. Crea un alias o función persistente para consultar el estado del servicio y demuéstralo desde una nueva sesión de shell.

**E10:** propietario y permisos del código y del archivo `.env`, y usuario efectivo del proceso Python.

**E11:** unidad y configuración de arranque, estados del servicio y alias o función funcionando. No muestres contraseñas ni claves privadas.

**E12:** `.env` con el backend cambiado a `HOST=127.0.0.1` y `PORT=8000`, servicio reiniciado, y demostración del ciclo `start` / `status` / `stop` / `restart` / `enable` con la explicación de la diferencia entre `start` y `enable`, y entre `restart` y `reload`.

### Parte 6 — Publicar mediante Nginx — 3 puntos

1. Adapta la configuración de proxy inverso de la sesión 09. Nginx debe escuchar en el puerto `80` y reenviar las rutas del sitio hacia `http://127.0.0.1:8000`.
2. Comprueba la configuración con `nginx -t` antes de aplicarla y recarga Nginx. Verifica que el bloque activo atienda el acceso por IP y no muestre la página predeterminada de Nginx.
3. Desde la VM, verifica que el backend responde en `http://127.0.0.1:8000/`.
4. Desde `PC_HOST`, visita `http://VM_IP/` y repite las pruebas de rutas de la parte 4 a través de Nginx. Comprueba HTML, CSS y enlaces de WhatsApp.
5. Muestra los listeners: Nginx en `0.0.0.0:80` y Python en `127.0.0.1:8000`. Python ya no debe escuchar en `0.0.0.0:8000` ni en una dirección externa equivalente.
6. Observa una solicitud en la interfaz de red de la VM y en loopback. Identifica los dos tramos TCP: `HOST_IP:puerto_efimero → VM_IP:80` y `127.0.0.1:otro_puerto_efimero → 127.0.0.1:8000`.
7. Relaciona la petición y respuesta con los registros de Nginx y del backend. Explica que Nginx establece una conexión al backend: no es una sola conexión TCP que atraviesa ambos procesos.

**E13:** configuración activa del proxy, validación satisfactoria de Nginx y listeners finales.

**E14:** landing final en `http://VM_IP/`, respuestas de las cuatro rutas y registros de ambos servicios correspondientes a las pruebas.

**E15:** tráfico de los dos tramos, con extremos, petición y respuesta identificados. Presenta varios recortes legibles si una sola imagen no permite verlos.

### Parte 7 — Controlar el acceso y recuperar una falla — 2 puntos

1. Deja UFW activo: permite el acceso HTTP de la red de evaluación; retira el permiso temporal de `8000` y registra las reglas finales.
2. Desde el host, comprueba que `http://VM_IP/` funciona y que `http://VM_IP:8000/` no es accesible. Desde la VM, confirma que `http://127.0.0.1:8000/` sí responde. Usa tiempos de espera limitados para las pruebas negativas.
3. Explica por separado la restricción por dirección de escucha y la política del firewall: una prueba fallida por sí sola no identifica cuál de las dos impide la conexión.
4. Reproduce el bloqueo por IP de la sesión 08, limitado al tráfico HTTP del host. Coloca la regla antes de la autorización correspondiente, abre una conexión nueva y demuestra el fallo. Elimina esa regla temporal y demuestra la recuperación. Mantén disponible la consola de la VM.
5. Simula una incidencia deteniendo únicamente el servicio Python. Solicita de nuevo la landing a través de Nginx, registra el error observado —normalmente `502 Bad Gateway`— y diagnostica usando estado del servicio, puertos en escucha y logs.
6. Recupera el servicio y comprueba una nueva respuesta `200`. Explica por qué Nginx activo no garantiza que el backend funcione.
7. Reinicia la VM y verifica que Nginx y la aplicación arrancan automáticamente y la landing vuelve a responder. Si cambia la IP por DHCP, actualiza la ficha y los diagramas finales.

**E16:** UFW activo, reglas finales y pruebas comparadas de acceso al puerto `80`, rechazo o falta de acceso externo a `8000`, y respuesta local del backend.

**E17:** bloqueo HTTP temporal por origen, fallo desde el cliente, eliminación de la regla y recuperación.

**E18:** incidencia del backend, diagnóstico, recuperación y verificación de ambos servicios después del reinicio de la VM.

### Parte 8 — Documentar la arquitectura implementada — 2 puntos

Elabora **un diagrama de bloques propio de la arquitectura de red final**, con los valores reales de tu entorno. Debe incluir:

- Equipo físico, sistema anfitrión, `HOST_IP` y cliente navegador o terminal.
- Hipervisor y su tipo, VM Ubuntu, recursos asignados, interfaz virtual, `VM_IP` y prefijo de subred.
- Adaptador puente, interfaz física, LAN y router con `ROUTER_IP`.
- UFW como control de acceso de la VM y las reglas relevantes.
- Nginx en `VM_IP:80`, Python en `127.0.0.1:8000` y archivos de `ecommerce_webapp` dentro de la VM.
- Flujo HTTP del cliente a Nginx y del proxy al backend, con flechas de respuesta, protocolos y puertos.
- Salida de la VM hacia Internet usada en la parte 2: resolución DNS, destino observado y NAT del router, diferenciada del acceso local a la landing.

Representa correctamente la pertenencia de componentes: Nginx y Python son procesos dentro de la misma VM; `127.0.0.1` pertenece a esa VM. El host aporta la interfaz física al puente, pero su IP no reemplaza la IP de origen de la VM. No dibujes el router como salto obligatorio de la petición local si ambos equipos comparten subred.

Además, entrega cuatro diagramas de secuencia propios:

1. Intercambio TCP `Hola` / `Hola PC`, cubriendo los tres diagramas de saludo proporcionados.
2. Acceso HTTP directo a Python durante la etapa temporal, usando `GET /`.
3. Acceso HTTP final mediante Nginx, con los dos tramos TCP y el retorno del HTML.
4. Salida HTTPS desde la VM hacia Internet, retomando `tarea`, con DNS, puente y NAT del router.

Puedes utilizar Mermaid, draw.io u otra herramienta. Entrega el archivo editable y su representación legible en el informe. Rotula el acceso directo a `8000` como **etapa temporal** para no confundirlo con la arquitectura final.

**E19:** diagrama de bloques y cuatro diagramas de secuencia con IP reales, puertos, protocolos y leyenda.

### Actividad adicional obligatoria — Mapa conceptual en `.canvas` — 2 puntos

Elabora un mapa conceptual que relacione **todos los conceptos que consideres relevantes desde la sesión 00 hasta la sesión 10**. Selecciona los conceptos con criterio y explica sus conexiones con el despliegue realizado. Esta actividad forma parte de la calificación sobre **20 puntos**; no otorga puntos por encima de ese total.

1. Revisa las sesiones 00 a 10 y selecciona los conceptos relevantes de cada material disponible. Las sesiones 03 y 04 comparten un solo archivo de diapositivas.
2. Organiza el mapa alrededor del despliegue y la administración de la landing ecommerce. Puedes agrupar los conceptos por temas, conservando una referencia a la sesión de origen de cada nodo o grupo.
3. Conecta los conceptos con flechas etiquetadas que expresen una relación concreta, por ejemplo: «ejecuta», «escucha en», «reenvía a», «controla el acceso a» o «resuelve». Incluye conexiones entre sesiones, no solo listas independientes de términos.
4. Considera, según su relevancia, sistemas operativos, nube, virtualización, hipervisores, recursos, Linux, terminal y shell, archivos, usuarios, permisos, servicios, systemd, interfaces, IP, subredes, puente, rutas, DNS, NAT, TCP, HTTP, puertos, Nginx, Python, proxy inverso, UFW y herramientas de asistencia. Esta lista orienta la selección; puedes incorporar otros conceptos fundamentados en las sesiones.
5. Vincula los conceptos con ejemplos de tu implementación: qué proceso escucha en cada puerto, qué administra systemd, qué controla UFW y cómo llega una petición al backend. Distingue los conceptos introductorios del curso de las tecnologías que efectivamente implementaste.
6. Guarda el mapa como `PC1_Apellido_Nombre_mapa_conceptual.canvas`, en formato editable compatible con Obsidian Canvas (JSON Canvas). Debe abrirse y mostrar sus nodos y conexiones; cambiar la extensión de una imagen o un PDF no cumple el requisito.
7. Incluye en el informe una vista general legible y los acercamientos necesarios, junto con un párrafo que justifique tu selección y explique al menos tres relaciones entre contenidos de distintas sesiones.

El mapa conceptual complementa el diagrama de bloques y los diagramas de secuencia: explica relaciones entre conocimientos, mientras los otros representan la arquitectura y sus comunicaciones. Debes entregar los tres tipos de representación.

**E20:** mapa conceptual abierto en una herramienta compatible, con conceptos, conexiones etiquetadas y referencias a las sesiones visibles; adjunta también el archivo `.canvas` original.

## 5. Documento y archivos que debes entregar

Presenta un único informe llamado `PC1_Apellido_Nombre.pdf`, con esta estructura:

1. Identificación del estudiante y descripción de la práctica.
2. Inventario, ficha de red y relación de materiales previos utilizados. Declara los materiales no disponibles.
3. Desarrollo de las ocho partes: acción, comando o configuración, resultado esperado, resultado observado y capturas `E01` a `E19`.
4. Diagrama de bloques y diagramas de secuencia.
5. Incidencia provocada, diagnóstico, corrección y pruebas posteriores al reinicio.
6. Tabla final de aceptación y explicación de las decisiones técnicas.
7. Actividad adicional: mapa conceptual de las sesiones 00 a 10, evidencia `E20`, justificación de la selección y explicación de las relaciones.

Entrega junto al informe el archivo `PC1_Apellido_Nombre_mapa_conceptual.canvas`. Dentro del informe incluye los programas Python de la prueba TCP y del cliente HTTP, la unidad systemd, el bloque de Nginx y el `.env` de ejemplo (con valores de prueba, sin secretos ni contraseñas). Identifica la ubicación donde desplegaste la aplicación y cualquier cambio realizado; el código funcional de la landing debe seguir siendo el entregado por desarrollo.

Cada captura debe ser legible, mostrar si corresponde al host o a la VM y tener un pie que explique qué requisito demuestra. En el navegador muestra la URL; en terminal muestra comando y resultado. Las capturas de código sin ejecución no acreditan funcionamiento. No reutilices imágenes de clase como evidencia propia.

### Tabla de aceptación que debes completar

| Comprobación             | Resultado esperado                                                                                                  | Evidencia y resultado observado |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| Saludo TCP desde el host | `Hola` recibido y `Hola PC` devuelto por la misma conexión.                                                         | Completar.                      |
| Etapa directa            | Landing en `VM_IP:8000`, con HTML y CSS correctos.                                                                  | Completar.                      |
| Publicación final        | Landing en `http://VM_IP/` mediante Nginx.                                                                          | Completar.                      |
| Rutas válidas            | `/`, `/index.html` y `/style.css` devuelven `200`.                                                                  | Completar.                      |
| Ruta no implementada     | `/productos` devuelve `404`, explicado según el código.                                                             | Completar.                      |
| Cotización               | Número y mensaje de prueba correctamente incorporados al enlace.                                                    | Completar.                      |
| Backend aislado          | Responde en loopback y no es accesible desde el host en `8000`.                                                     | Completar.                      |
| Administración           | Usuario sin privilegios para Python y permisos justificados.                                                        | Completar.                      |
| Firewall                 | Activo; prueba de bloqueo y recuperación demostrada.                                                                | Completar.                      |
| Recuperación             | Falla del backend diagnosticada y corregida.                                                                        | Completar.                      |
| Reinicio de la VM        | Servicios arrancan automáticamente y la landing responde.                                                           | Completar.                      |
| Arquitectura             | Diagrama de bloques y secuencias coinciden con la implementación.                                                   | Completar.                      |
| Mapa conceptual          | Archivo `.canvas` editable con conceptos relevantes de las sesiones 00 a 10 y relaciones explicadas entre sesiones. | Completar.                      |

## 6. Criterios de evaluación — 20 puntos

| Sección evaluada | Evidencias | Puntaje |
| --- | --- | ---: |
| Parte 1 — Entorno Ubuntu, recursos y modo puente. | E01–E02 | 1 |
| Parte 2 — Datos reales de red y salida a Internet. | E03–E04 | 2 |
| Parte 3 — Implementación TCP e intercambio de mensajes. | E05–E06 | 3 |
| Parte 4 — Landing en Python, rutas, cliente HTTP y cotización. | E07–E09 | 3 |
| Parte 5 — Usuarios, permisos y systemd. | E10–E12 | 2 |
| Parte 6 — Nginx, backend en loopback y ambos tramos de comunicación. | E13–E15 | 3 |
| Parte 7 — UFW, control de acceso, recuperación y reinicio. | E16–E18 | 2 |
| Parte 8 — Diagrama de bloques y diagramas de secuencia. | E19 | 2 |
| Actividad adicional — Mapa conceptual editable en `.canvas`. | E20 | 2 |
| **Total** | | **20** |

Se evalúa la implementación demostrada y la capacidad de explicarla. Una landing accesible no acredita por sí sola las etapas TCP, la configuración de seguridad, la persistencia del servicio ni el análisis de red. Al cerrar el simulador, deja la arquitectura final operativa, sin el servidor de saludo ni las reglas temporales de prueba.
