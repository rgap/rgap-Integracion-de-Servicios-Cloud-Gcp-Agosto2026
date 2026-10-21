C4Deployment
    title Lab01 - Tarea 5 - Crea un estado persistente en Cloud Shell

    %% @pos estudiante x=20 y=205 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Configura variables que sobreviven al cambio de VM")

    %% @pos equipo x=456 y=-172 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=500 y=-116 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Abre, cierra y vuelve a abrir Cloud Shell")
    }

    %% @pos consola x=-4 y=-124 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Muestra el ID del proyecto")

    %% @pos vm1 x=804 y=-452 w=428 h=200 kind=appserver
    Deployment_Node(vm1, "VM temporal - sesión inicial", "Cloud Shell · Debian", "Las variables de proceso desaparecen al cerrar") {
        %% @pos terminal1 x=828 y=-396 kind=terminal
        Container(terminal1, "Terminal inicial", "Bash", "Crea variables y archivos de configuración")
        %% @pos gcloud x=1008 y=-396 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Lista regiones disponibles")
    }

    %% @pos home x=905 y=75 kind=storage
    ContainerDb(home, "Directorio personal persistente", "$HOME · 5 GB", "Conserva ~/infraclass/config y ~/.profile")

    %% @pos vm2 x=532 y=372 w=276 h=200 kind=appserver
    Deployment_Node(vm2, "VM temporal - sesión nueva", "Cloud Shell · Debian", "Nueva VM asignada al reabrir") {
        %% @pos terminal2 x=570 y=428 kind=terminal
        Container(terminal2, "Terminal nueva", "Bash", "Carga .profile y recupera las variables")
    }

    %% @pos api x=1232 y=68 kind=api
    Container(api, "API de Compute Engine", "Google Cloud API", "Devuelve la lista de regiones")

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Consulta el ID del proyecto", "HTTPS")
    Rel(navegador, terminal1, "Abre la sesión inicial", "WebSocket")
    Rel(terminal1, gcloud, "Ejecuta gcloud compute regions list")
    Rel(gcloud, api, "Consulta regiones", "HTTPS / REST")
    Rel(terminal1, home, "Crea ~/infraclass/config con región e ID")
    %% @rel label=-8,-48 points=1092,-152
    Rel(terminal1, home, "Edita ~/.profile para ejecutar source")
    Rel(navegador, terminal2, "Cierra y abre una sesión nueva", "WebSocket")
    Rel(home, terminal2, "Carga .profile e infraclass/config al iniciar")
    Rel(terminal2, estudiante, "Confirma INFRACLASS_PROJECT_ID con echo")
