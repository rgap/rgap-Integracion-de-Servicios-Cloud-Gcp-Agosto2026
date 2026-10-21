```
C4Deployment
    title Lab01 - Tarea 4 - Sube un archivo y cópialo a un bucket

    %% @pos estudiante x=60 y=236 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Sube un archivo y confirma su copia")

    %% @pos equipo x=300 y=184 w=244 h=436 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=342 y=240 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra Cloud Shell y el selector de archivos")
        %% @pos archivo_local x=347 y=476 kind=database
        ContainerDb(archivo_local, "Archivo local", "Disco local", "Archivo seleccionado para subir")
    }

    %% @pos cloudshell x=708 y=472 w=624 h=484 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian", "Entorno temporal con almacenamiento persistente") {
        %% @pos terminal x=732 y=540 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Ejecuta ls y el comando de copia")
        %% @pos home x=1112 y=528 kind=storage
        ContainerDb(home, "Directorio personal", "$HOME · 5 GB", "Recibe el archivo subido")
        %% @pos gcloud x=888 y=812 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Copia el archivo desde Cloud Shell")
    }

    %% @pos proyecto x=1440 y=756 w=260 h=408 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api x=1470 y=812 kind=api
        Container(api, "API de Google Cloud", "REST · googleapis.com", "Procesa la carga del objeto")
        %% @pos bucket x=1486 y=1020 kind=storage
        ContainerDb(bucket, "Bucket de destino", "Cloud Storage", "Contiene la copia del archivo")
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(archivo_local, navegador, "Selecciona para subir")
    Rel(navegador, terminal, "Abre la sesión", "WebSocket")
    Rel(navegador, home, "Sube el archivo", "HTTPS")
    Rel(terminal, home, "Verifica con ls")
    Rel(terminal, gcloud, "Ejecuta gcloud storage cp")
    Rel(home, gcloud, "Entrega el archivo")
    Rel(gcloud, api, "Copia el objeto", "HTTPS / REST")
    Rel(api, bucket, "Almacena el objeto")

    %% @step estudiante navegador | Escribe la dirección y pulsa Enter
    %% @step navegador terminal | Abre la aplicación
    %% @step terminal home | Descarga los archivos | GET / HTTP/1.1\nHost: ejemplo.com\nAccept: text/html
    %% @step home terminal | Devuelve los archivos | HTTP/1.1 200 OK\nContent-Type: application/json\n\n{ … }
    %% @step terminal gcloud | Ejecuta el script
    %% @step gcloud api | Pide los datos que va a mostrar | GET /api/datos HTTP/1.1\nHost: ejemplo.com\nAccept: application/json
    %% @step api bucket | Lee el archivo | GET / HTTP/1.1\nHost: ejemplo.com\nAccept: text/html
    %% @step bucket api | Devuelve el archivo | HTTP/1.1 200 OK\nContent-Type: application/json\n\n{ … }
    %% @step api gcloud | Devuelve los datos en JSON | HTTP/1.1 200 OK\nContent-Type: application/json\n\n{ … }
    %% @step gcloud terminal | Termina y devuelve el resultado
    %% @step terminal navegador | Muestra el resultado
    %% @step navegador home | Descarga los archivos | GET / HTTP/1.1\nHost: ejemplo.com\nAccept: text/html
    %% @step home navegador | Devuelve los archivos | HTTP/1.1 200 OK\nContent-Type: application/json\n\n{ … }
    %% @step navegador estudiante | Ve la página
```