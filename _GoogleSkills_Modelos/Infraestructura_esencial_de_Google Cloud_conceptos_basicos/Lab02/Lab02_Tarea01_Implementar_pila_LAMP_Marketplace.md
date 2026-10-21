C4Deployment
    title Lab02 - Tarea 1 - Implementa una pila LAMP con Cloud Marketplace

    %% @pos estudiante x=-32 y=152 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Busca la pila LAMP y la implementa en la zona del lab")

    %% @pos equipo x=234 y=100 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=156 kind=browser url=console.cloud.google.com/marketplace
        Container(navegador, "Navegador", "Chrome", "Muestra Marketplace y el formulario de implementación")
    }

    %% @pos consola x=700 y=156 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Abre Marketplace y muestra el avance de lamp-1")

    %% @pos marketplace x=1140 y=-220 kind=external
    %% @part marketplace | Pila de LAMP | De Google Click to Deploy: Linux, Apache, MariaDB y PHP en una VM
    %% @part marketplace | Términos y acuerdos | Se aceptan antes de implementar
    %% @part marketplace | Formulario | Zona del lab, serie E2 y tipo e2-medium; lo demás como viene
    System_Ext(marketplace, "Cloud Marketplace", "Catálogo de soluciones: se acepta el acuerdo y se manda a implementar")

    %% @pos infra_manager x=1140 y=156 kind=external
    %% @part infra_manager | Implementación lamp-1 | «Se está implementando lamp-1» y luego «Se implementó lamp-1»
    %% @part infra_manager | Resumen | URL del sitio, usuario y contraseña de MySQL
    System_Ext(infra_manager, "Infrastructure Manager", "Aplica la plantilla de la solución y sigue su estado")

    %% @pos cloud_build x=1576 y=132 kind=external
    System_Ext(cloud_build, "Cloud Build", "Corre terraform apply para Infrastructure Manager")

    %% @pos estado x=1572 y=412 kind=storage
    %% @file estado | deployments/lamp-1/default.tfstate | | 12 kB
    ContainerDb(estado, "Estado de Terraform", "Cloud Storage", "Qué recursos creó la implementación")

    %% @pos proyecto x=2020 y=44 w=1000 h=504 kind=cloud
    %% @part proyecto | APIs habilitadas | Compute Engine (compute.googleapis.com) e Infrastructure Manager (config.googleapis.com)
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=2044 y=116 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea la VM, su disco y las reglas de firewall")
        %% @pos firewall x=2044 y=380 kind=firewall
        %% @part firewall | lamp-1-tcp-80 | TCP 80 desde 0.0.0.0/0 a la etiqueta lamp-1-deployment
        %% @part firewall | lamp-1-tcp-443 | TCP 443 desde 0.0.0.0/0 a la misma etiqueta
        Container(firewall, "Reglas de firewall", "Cloud Firewall", "Abren los puertos 80 y 443 de la VM")
        %% @pos vm x=2440 y=100 w=556 h=424 kind=appserver
        %% @part vm | Tipo de máquina | e2-medium: 2 vCPU y 4 GB de memoria
        %% @part vm | Etiqueta de red | lamp-1-deployment
        Deployment_Node(vm, "lamp-1-vm", "Compute Engine · Debian 12") {
            %% @pos disco x=2484 y=156 kind=storage
            ContainerDb(disco, "Disco de arranque", "Persistent Disk (pd-balanced)", "Debian 12 con la imagen de la solución")
            %% @pos agente x=2772 y=156 kind=generic
            Container(agente, "Agente invitado", "google-guest-agent", "Configura la VM al arrancar")
            %% @pos apache x=2744 y=376 kind=webserver
            Container(apache, "Servidor web", "Apache HTTP Server", "Sirve /var/www/html en el puerto 80")
            %% @pos mariadb x=2464 y=380 kind=database
            ContainerDb(mariadb, "Base de datos", "MariaDB", "Con el usuario root y la contraseña del resumen")
        }
    }

    %% @pos metadatos x=3168 y=152 kind=external
    System_Ext(metadatos, "Servidor de metadatos", "Da a la VM su configuración y su script de inicio")

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Busca LAMP en Marketplace", "HTTPS")
    Rel(consola, marketplace, "Acepta los términos e implementa", "HTTPS")
    Rel(marketplace, infra_manager, "Crea la implementación lamp-1", "JSON/HTTPS")
    Rel(consola, infra_manager, "Consulta el estado de lamp-1", "JSON/HTTPS")
    Rel(infra_manager, cloud_build, "Ejecuta Terraform", "JSON/HTTPS")
    Rel(cloud_build, estado, "Guarda el estado de Terraform", "JSON/HTTPS")
    Rel(cloud_build, api_compute, "Crea los recursos de la plantilla", "JSON/HTTPS")
    Rel(api_compute, disco, "Crea el disco")
    Rel(api_compute, firewall, "Crea las reglas de firewall")
    Rel(agente, metadatos, "Lee su configuración", "HTTP")
    Rel(agente, apache, "Arranca Apache")
    Rel(agente, mariadb, "Arranca MariaDB")

    %% @step estudiante navegador | En el menú de navegación, abre Marketplace y busca «LAMP»
    %% @step navegador consola | Pide los resultados de la búsqueda | GET /marketplace/browse?q=lamp HTTP/1.1\nHost: console.cloud.google.com
    %% @step consola navegador | Muestra los resultados: elige «Pila de LAMP» de Google Click to Deploy
    %% @step navegador consola | Pulsa Comenzar, acepta los términos y pulsa Implementar
    %% @step consola marketplace | Registra el acuerdo y abre el formulario
    %% @step marketplace infra_manager | Con la zona del lab y e2-medium, crea lamp-1 | POST /v1/projects/PROYECTO/locations/REGION/deployments?deploymentId=lamp-1 HTTP/1.1\nHost: config.googleapis.com\nAuthorization: Bearer ya29.…
    %% @step infra_manager cloud_build | Corre terraform apply con la plantilla de la solución
    %% @step cloud_build api_compute | Crea la VM lamp-1-vm | POST /compute/v1/projects/PROYECTO/zones/ZONA/instances HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "lamp-1-vm", "machineType": "zones/ZONA/machineTypes/e2-medium",\n "tags": {"items": ["lamp-1-deployment"]}}
    %% @step api_compute disco | Crea el disco de arranque desde la imagen
    %% @step api_compute firewall | Crea lamp-1-tcp-80 y lamp-1-tcp-443
    %% @step cloud_build estado | Guarda qué recursos creó
    %% @step consola infra_manager | Pregunta cómo va lamp-1
    %% @step infra_manager consola | «Se implementó lamp-1»: la infraestructura ya está
    %% @step agente metadatos | La VM arranca y lee su configuración | GET /computeMetadata/v1/instance/?recursive=true HTTP/1.1\nHost: metadata.google.internal\nMetadata-Flavor: Google
    %% @step agente mariadb | Arranca MariaDB
    %% @step agente apache | Arranca Apache en el puerto 80
    %% @step consola infra_manager | Vuelve a preguntar
    %% @step infra_manager consola | Software instalado: devuelve el resumen con la URL del sitio
    %% @step consola navegador | Muestra el resumen de lamp-1
    %% @step navegador estudiante | Ve la URL del sitio y la contraseña de MySQL
