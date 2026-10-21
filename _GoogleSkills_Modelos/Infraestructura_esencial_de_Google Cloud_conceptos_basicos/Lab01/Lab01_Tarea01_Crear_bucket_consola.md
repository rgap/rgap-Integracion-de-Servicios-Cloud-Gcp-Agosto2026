C4Deployment
    title Lab01 - Tarea 1 - Crea un bucket desde la consola

    %% @pos estudiante x=144 y=-208 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Usa la cuenta temporal del laboratorio")

    %% @pos equipo x=428 y=-264 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=472 y=-208 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Abre la consola de Google Cloud")
    }

    %% @pos consola x=448 y=292 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Valida los datos y solicita la creación del bucket")

    %% @pos proyecto x=916 y=-276 w=640 h=407 kind=cloud size=manual
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api x=940 y=-220 kind=api
        Container(api, "API de Google Cloud", "REST · googleapis.com", "Recibe la operación de Cloud Storage")
        %% @pos bucket x=1332 y=-220 w=200 h=128 kind=storage
        ContainerDb(bucket, "Bucket de Cloud Storage", "Cloud Storage", "Guarda objetos con un nombre globalmente único")
        %% @pos notificaciones x=1144 y=-20 kind=webapp
        Container(notificaciones, "Notificaciones", "Google Cloud Console", "Muestra el resultado de la operación")
    }

    %% @pos iam x=864 y=296 kind=external
    System_Ext(iam, "IAM", "Autoriza a la cuenta temporal")

    %% @rel label=-16,0
    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Abre y completa el formulario", "HTTPS")
    Rel(consola, iam, "Comprueba permisos", "HTTPS")
    Rel(consola, api, "Solicita crear el bucket", "HTTPS / REST")
    Rel(api, bucket, "Crea y configura")
    Rel(api, notificaciones, "Publica el resultado")
    Rel(consola, notificaciones, "Consulta el historial", "HTTPS")
