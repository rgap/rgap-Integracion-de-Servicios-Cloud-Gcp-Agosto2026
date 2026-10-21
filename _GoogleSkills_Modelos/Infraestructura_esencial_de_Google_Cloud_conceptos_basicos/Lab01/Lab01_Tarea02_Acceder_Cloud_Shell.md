```
C4Deployment
    title Lab01 - Tarea 2 - Accede a Cloud Shell

    %% @pos estudiante x=208 y=276 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Activa, explora y cierra Cloud Shell")

    %% @pos equipo x=232 y=-16 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=276 y=40 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y la terminal web")
    }

    %% @pos consola x=636 y=-176 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Activa Cloud Shell y controla su panel")

    %% @pos cloudshell x=1004 y=60 w=580 h=420 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian", "VM temporal asignada a la sesión") {
        %% @pos terminal x=1028 y=116 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Ofrece línea de comandos desde el navegador")
        %% @pos gcloud x=1360 y=116 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Herramientas preinstaladas")
        %% @pos home x=1196 y=336 kind=storage
        ContainerDb(home, "Directorio personal", "$HOME · 5 GB", "Almacenamiento que persiste entre sesiones")
    }

    %% @pos control x=544 y=356 kind=external
    System_Ext(control, "Controles del panel", "Minimizar, maximizar, nueva ventana y cerrar")

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Abre la consola", "HTTPS")
    Rel(consola, terminal, "Activa y asigna la sesión", "HTTPS")
    Rel(navegador, terminal, "Abre la terminal interactiva", "WebSocket")
    Rel(terminal, gcloud, "Ejecuta")
    Rel(terminal, home, "Lee y escribe archivos")
    Rel(estudiante, control, "Prueba los controles")
    Rel(control, terminal, "Cierra la terminal y termina la sesión")

    %% @step estudiante navegador | Escribe la dirección y pulsa Enter
    %% @step navegador terminal | Abre la aplicación
    %% @step terminal home | Descarga los archivos | GET / HTTP/1.1\nHost: ejemplo.com\nAccept: text/html
    %% @step home terminal | Devuelve los archivos | HTTP/1.1 200 OK\nContent-Type: application/json\n\n{ … }
    %% @step terminal gcloud | Ejecuta el script
    %% @step gcloud terminal | Termina y devuelve el resultado
    %% @step terminal navegador | Muestra el resultado
    %% @step navegador consola | Pide la página | GET / HTTP/1.1\nHost: console.cloud.google.com\nAccept: text/html
    %% @step consola navegador | Devuelve la página generada con los datos | HTTP/1.1 200 OK\nContent-Type: text/html\n\n<!doctype html>…
    %% @step navegador estudiante | Ve la página
```