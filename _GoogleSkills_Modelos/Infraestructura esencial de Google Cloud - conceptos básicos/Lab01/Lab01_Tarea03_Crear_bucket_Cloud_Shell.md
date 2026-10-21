C4Deployment
    title Lab01 - Tarea 3 - Crea un bucket con Cloud Shell

    %% @pos estudiante x=-92 y=116 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Crea y verifica un bucket desde la terminal")

    %% @pos equipo x=206 y=74 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=250 y=130 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Abre la consola y Cloud Shell")
    }

    %% @pos consola x=664 y=-136 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Permite comprobar la lista de buckets")

    %% @pos proyecto x=1092 y=-52 w=592 h=204 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api x=1116 y=4 kind=api
        Container(api, "API de Google Cloud", "REST · googleapis.com", "Procesa solicitudes de Cloud Storage")
        %% @pos bucket2 x=1460 y=8 kind=storage
        ContainerDb(bucket2, "Segundo bucket", "Cloud Storage", "Bucket creado con un nombre globalmente único")
    }

    %% @pos iam x=1404 y=372 kind=external
    System_Ext(iam, "IAM", "Autoriza a la cuenta temporal")

    %% @pos cloudshell x=528 y=320 w=668 h=200 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian", "Entorno temporal administrado") {
        %% @pos terminal x=552 y=376 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Recibe los comandos del estudiante")
        %% @pos gcloud x=972 y=376 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Ejecuta operaciones de Cloud Storage")
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, terminal, "Abre Cloud Shell", "WebSocket")
    Rel(terminal, gcloud, "Ejecuta gcloud storage buckets create")
    Rel(gcloud, iam, "Solicita autorización", "HTTPS")
    Rel(gcloud, api, "Crea el segundo bucket", "HTTPS / REST")
    Rel(api, bucket2, "Aprovisiona")
    Rel(navegador, consola, "Actualiza Cloud Storage > Buckets", "HTTPS")
    Rel(consola, api, "Lista los buckets", "HTTPS / REST")
