```
C4Deployment
    title Lab05 - Tarea 2 - Crea una máquina virtual de Windows

    %% @pos estudiante x=-192 y=252 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Crea utility-wm con Windows Server y le pone una contraseña")

    %% @pos equipo x=176 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=220 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola")
    }

    %% @pos consola x=700 y=256 kind=webapp url=console.cloud.google.com
    %% @part consola | Configurar contraseña de Windows | Crea un par de llaves en el navegador y descifra la contraseña con la privada
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Crea utility-wm y su contraseña de Windows")

    %% @pos proyecto x=1100 y=-200 w=1364 h=944 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1124 y=256 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea la VM, sus reglas y guarda la petición de contraseña")
        %% @pos metadatos x=1124 y=600 kind=external
        %% @part metadatos | windows-keys | La petición de contraseña: usuario, llave pública y vencimiento
        System_Ext(metadatos, "Servidor de metadatos", "Da a la VM su configuración y la petición de contraseña")
        %% @pos default x=1480 y=-144 w=960 h=816 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos regla_http x=1504 y=-88 kind=firewall
            Container(regla_http, "default-allow-http", "Regla de Cloud Firewall · entrada", "Permite tcp:80 desde 0.0.0.0/0 a la etiqueta http-server")
            %% @pos regla_https x=1780 y=-88 kind=firewall
            Container(regla_https, "default-allow-https", "Regla de Cloud Firewall · entrada", "Permite tcp:443 desde 0.0.0.0/0 a la etiqueta https-server")
            %% @pos regla_rdp x=2056 y=-88 kind=firewall
            Container(regla_rdp, "default-allow-rdp", "Regla de Cloud Firewall · entrada", "Permite tcp:3389 desde 0.0.0.0/0: la trae la red default")
            %% @pos subred x=1504 y=120 w=912 h=528 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1528 y=176 w=864 h=448 kind=appserver
                %% @part vm | Tipo de máquina | e2-standard-2: 2 vCPU y 8 GB
                %% @part vm | Etiquetas de red | http-server y https-server: las marcan las casillas de Firewall
                %% @part vm | Usuario de Windows | estudiante, creado por el agente
                %% @part vm | Puerto serie 4 | Donde el agente deja la contraseña cifrada
                Deployment_Node(vm, "utility-wm", "Compute Engine · Windows Server 2025 Datacenter Core", "us-central1-c · e2-standard-2") {
                    %% @pos ip_externa x=1864 y=232 kind=interface
                    Container(ip_externa, "IP externa", "203.0.113.21", "Efímera")
                    %% @pos agente x=1552 y=480 kind=generic
                    Container(agente, "Agente invitado", "google-guest-agent", "Crea el usuario y su contraseña cuando lo piden los metadatos")
                    %% @pos disco x=1552 y=232 kind=storage
                    ContainerDb(disco, "Disco de arranque", "Persistent Disk (pd-ssd)", "SSD de 64 GB con Windows Server 2025 Datacenter Core")
                    %% @pos nic x=2176 y=232 kind=interface
                    Container(nic, "nic0", "10.128.0.3", "La IP interna")
                    %% @pos rdp x=2176 y=480 kind=generic
                    Container(rdp, "Escritorio remoto", "RDP · TCP 3389", "Abre una sesión de Windows; conectarse queda fuera del lab")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea utility-wm y su contraseña", "HTTPS")
    Rel(consola, api_compute, "Crea la VM y pide la contraseña", "JSON/HTTPS")
    Rel(api_compute, disco, "Crea el disco")
    Rel(api_compute, regla_http, "Crea las reglas de firewall")
    Rel(api_compute, metadatos, "Guarda la petición de contraseña")
    Rel(agente, metadatos, "Espera cambios en los metadatos", "HTTP")
    Rel(ip_externa, nic, "Traduce a la IP interna", "NAT 1:1")
    %% @door rdp | Escucha en el puerto 3389 (RDP)\nCon usuario y contraseña de Windows
    Rel(nic, rdp, "Entrega al puerto", "RDP :3389")

    %% @step estudiante navegador | Crear instancia: utility-wm, us-central1-c, e2-standard-2
    %% @step navegador consola | SO: Windows Server 2025 Datacenter Core, SSD de 64 GB
    %% @step navegador consola | Firewall: Permitir tráfico HTTP y HTTPS; Crear
    %% @step consola api_compute | Crea utility-wm | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "utility-wm", "machineType": "zones/us-central1-c/machineTypes/e2-standard-2",\n "tags": {"items": ["http-server", "https-server"]},\n "disks": [{"boot": true, "initializeParams": {\n   "sourceImage": "projects/windows-cloud/global/images/family/windows-2025-core",\n   "diskType": "zones/us-central1-c/diskTypes/pd-ssd", "diskSizeGb": "64"}}],\n "networkInterfaces": [{"network": "global/networks/default",\n   "accessConfigs": [{"type": "ONE_TO_ONE_NAT"}]}]}
    %% @step api_compute disco | SSD de 64 GB con Windows Server
    %% @step api_compute regla_http | default-allow-http y -https, para las etiquetas
    %% @step api_compute consola | En ejecución: el listado ofrece RDP, no SSH
    %% @step estudiante navegador | utility-wm > Configurar contraseña de Windows
    %% @step consola api_compute | Pide la contraseña | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances/utility-wm/setMetadata HTTP/1.1\nHost: compute.googleapis.com\n\n{"items": [{"key": "windows-keys", "value":\n  "{\\"userName\\": \\"estudiante\\", \\"modulus\\": \\"…\\", \\"exponent\\": \\"AQAB\\", \\"expireOn\\": \\"…\\"}"}]}\n\nLa llave pública es de un par que la consola crea en el navegador
    %% @step api_compute metadatos | Guarda windows-keys en los metadatos de la VM
    %% @step agente metadatos | Ve el cambio | GET /computeMetadata/v1/instance/attributes/?recursive=true&wait_for_change=true HTTP/1.1\nHost: metadata.google.internal\nMetadata-Flavor: Google
    %% @step agente agente | Crea el usuario y su contraseña | Crea estudiante, le da una contraseña al azar\ny la cifra con la llave pública: la escribe en el puerto serie 4
    %% @step consola api_compute | Lee el puerto serie 4 | GET /compute/v1/projects/PROYECTO/zones/us-central1-c/instances/utility-wm/serialPort?port=4 HTTP/1.1\nHost: compute.googleapis.com
    %% @step api_compute consola | La contraseña cifrada: la consola la descifra
    %% @step navegador consola | Copia la contraseña y Cerrar
    %% @step ip_externa nic | Un cliente RDP entraría por la IP externa (fuera del lab)
    %% @step nic rdp | default-allow-rdp deja pasar el 3389
```