```
C4Deployment
    title Lab06 - Tarea 1 - Crea la VM

    %% @pos estudiante x=-156 y=256 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Crea mc-server con un disco de datos SSD y una IP estática")

    %% @pos equipo x=196 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=240 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola")
    }

    %% @pos consola x=676 y=252 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Crea mc-server, su disco de datos y su IP estática")

    %% @pos proyecto x=1104 y=-200 w=1120 h=952 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1128 y=260 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Reserva la IP y crea la VM con sus dos discos")
        %% @pos default x=1480 y=-144 w=720 h=872 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos subred x=1504 y=-88 w=672 h=792 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1528 y=-32 w=624 h=712 kind=appserver
                %% @part vm | Tipo de máquina | e2-medium: 2 vCPU y 4 GB
                %% @part vm | Imagen | Debian GNU/Linux 12 (bookworm)
                %% @part vm | Etiquetas de red | minecraft-server: a la que se aplicará la regla del puerto 25565
                %% @part vm | Permisos de acceso | Cuenta de servicio predeterminada; Storage: lectura y escritura
                Deployment_Node(vm, "mc-server", "Compute Engine · Debian 12", "us-central1-c · e2-medium") {
                    %% @pos disco_arranque x=1552 y=280 kind=storage
                    ContainerDb(disco_arranque, "Disco de arranque", "Persistent Disk (pd-balanced)", "10 GB con Debian 12")
                    %% @pos disco_datos x=1552 y=536 kind=storage
                    %% @part disco_datos | Nombre de dispositivo | minecraft-disk: /dev/disk/by-id/google-minecraft-disk
                    %% @part disco_datos | Origen | Disco en blanco: sin sistema de archivos todavía
                    %% @part disco_datos | Encriptación | Clave administrada por Google
                    ContainerDb(disco_datos, "minecraft-disk", "Persistent Disk SSD (pd-ssd)", "Disco de datos de 50 GB, en blanco")
                    %% @pos ip_estatica x=1552 y=24 kind=interface
                    %% @part ip_estatica | Nombre | mc-server-ip
                    %% @part ip_estatica | Región | us-central1, la de la VM
                    Container(ip_estatica, "IP externa estática", "203.0.113.30", "mc-server-ip: no cambia al detener la VM")
                    %% @pos nic x=1980 y=24 kind=interface
                    Container(nic, "nic0", "10.128.0.2", "La IP interna")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea mc-server", "HTTPS")
    Rel(consola, api_compute, "Reserva la IP y crea la VM", "JSON/HTTPS")
    Rel(api_compute, ip_estatica, "Reserva la IP estática")
    Rel(api_compute, disco_arranque, "Crea el disco")
    Rel(api_compute, disco_datos, "Crea el disco")
    Rel(ip_estatica, nic, "Traduce a la IP interna", "NAT 1:1")

    %% @step estudiante navegador | Crear instancia: mc-server, us-central1-c
    %% @step navegador consola | SO: Debian 12; disco nuevo minecraft-disk: SSD, 50 GB
    %% @step navegador consola | Redes: etiqueta minecraft-server; IP estática mc-server-ip
    %% @step consola api_compute | Reserva mc-server-ip | POST /compute/v1/projects/PROYECTO/regions/us-central1/addresses HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "mc-server-ip", "addressType": "EXTERNAL"}
    %% @step api_compute ip_estatica | Reservada: 203.0.113.30
    %% @step navegador consola | Seguridad: Storage, lectura y escritura; Crear
    %% @step consola api_compute | Crea mc-server | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "mc-server", "machineType": "zones/us-central1-c/machineTypes/e2-medium",\n "tags": {"items": ["minecraft-server"]},\n "disks": [{"boot": true, "initializeParams": {"sourceImage": "projects/debian-cloud/global/images/family/debian-12"}},\n           {"deviceName": "minecraft-disk", "initializeParams": {"diskName": "minecraft-disk",\n             "diskType": "zones/us-central1-c/diskTypes/pd-ssd", "diskSizeGb": "50"}}],\n "networkInterfaces": [{"network": "global/networks/default",\n   "accessConfigs": [{"type": "ONE_TO_ONE_NAT", "natIP": "203.0.113.30"}]}],\n "serviceAccounts": [{"email": "default", "scopes": ["https://www.googleapis.com/auth/devstorage.read_write", "…"]}]}
    %% @step api_compute disco_arranque | 10 GB con Debian 12
    %% @step api_compute disco_datos | minecraft-disk: SSD de 50 GB, en blanco
    %% @step ip_estatica nic | mc-server-ip apunta a nic0
    %% @step api_compute consola | En ejecución, con IP externa 203.0.113.30
```