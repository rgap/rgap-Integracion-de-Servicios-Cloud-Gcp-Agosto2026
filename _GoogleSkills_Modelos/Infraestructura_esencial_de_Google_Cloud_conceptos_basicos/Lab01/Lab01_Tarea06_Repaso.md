```
C4Deployment
    title Lab01 - Tarea 6 - Repaso

    %% @pos estudiante x=-120 y=136 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Gestiona los mismos recursos con dos interfaces")

    %% @pos equipo x=197 y=84 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=235 y=140 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Accede a la consola, Cloud Shell y el laboratorio")
    }

    %% @pos consola x=656 y=-124 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Interfaz gráfica", "Presenta opciones válidas y valida cambios")

    %% @pos cloudshell x=552 y=400 w=580 h=200 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian", "Ofrece control detallado y automatización") {
        %% @pos terminal x=576 y=456 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Permite usar todas las opciones y scripts")
        %% @pos gcloud x=908 y=456 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Traduce comandos a solicitudes de API")
    }

    %% @pos proyecto x=1120 y=72 w=636 h=200 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api x=1144 y=128 kind=api
        Container(api, "API de Google Cloud", "REST · googleapis.com", "Punto común para ambas interfaces")
        %% @pos storage x=1532 y=128 kind=storage
        ContainerDb(storage, "Buckets y objetos", "Cloud Storage", "Recursos creados durante el Lab01")
    }

    %% @pos laboratorio x=692 y=144 kind=external
    System_Ext(laboratorio, "Control del laboratorio", "Finaliza el lab y limpia el proyecto temporal")

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Trabaja con formularios y validaciones", "HTTPS")
    Rel(navegador, terminal, "Trabaja con comandos y scripts", "WebSocket")
    Rel(terminal, gcloud, "Ejecuta")
    Rel(consola, api, "Opera los mismos recursos", "HTTPS / REST")
    Rel(gcloud, api, "Opera los mismos recursos", "HTTPS / REST")
    Rel(api, storage, "Crea, lista y carga")
    Rel(navegador, laboratorio, "Hace clic en Finalizar lab", "HTTPS")
    Rel(laboratorio, api, "Elimina los recursos del proyecto")
```