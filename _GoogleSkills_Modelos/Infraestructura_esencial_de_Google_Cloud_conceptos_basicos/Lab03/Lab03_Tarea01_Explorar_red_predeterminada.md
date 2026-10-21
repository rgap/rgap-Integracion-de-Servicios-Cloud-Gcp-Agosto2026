```
C4Deployment
    title Lab03 - Tarea 1 - Explora la red predeterminada

    %% @pos estudiante x=-40 y=152 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Revisa la red default, la borra e intenta crear una VM")

    %% @pos equipo x=222 y=100 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=156 kind=browser url=console.cloud.google.com/networking/networks
        Container(navegador, "Navegador", "Chrome", "Crear instancia: «No hay más redes disponibles»")
    }

    %% @pos consola x=688 y=144 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Red de VPC: redes, rutas y firewall; Compute Engine: crear instancia")

    %% @pos proyecto x=1236 y=40 w=1088 h=668 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1260 y=148 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Lista, borra y crea redes, reglas y VMs")
        %% @pos default x=1640 y=96 w=660 h=588 kind=cloud
        %% @part default | Modo de subredes | Automático: una subred por región en 10.128.0.0/9
        %% @part default | Reglas implícitas | deny-all-ingress y allow-all-egress, prioridad 65535: quedan aunque se borren las demás
        Deployment_Node(default, "default", "Google Cloud VPC", "Se borra en esta tarea, con sus subredes y sus rutas") {
            %% @pos subred_us x=2076 y=160 kind=generic
            Container(subred_us, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Una de las subredes: una por región")
            %% @pos subred_eu x=2072 y=336 kind=generic
            Container(subred_eu, "Subred europe-west1", "VPC de Google Cloud · 10.132.0.0/20", "Otra región, otro rango")
            %% @pos rutas x=1664 y=152 kind=generic
            %% @part rutas | Rutas de subred | Una por subred: 10.128.0.0/20, 10.132.0.0/20…
            %% @part rutas | Ruta predeterminada | 0.0.0.0/0 → default-internet-gateway
            Container(rutas, "Rutas", "Rutas de la VPC de Google Cloud", "Una ruta local por subred y 0.0.0.0/0 hacia internet")
            %% @pos igw x=2076 y=540 kind=generic
            Container(igw, "Puerta de enlace de Internet", "default-internet-gateway", "El siguiente salto de la ruta 0.0.0.0/0")
            %% @pos reglas x=1664 y=440 kind=firewall
            %% @part reglas | default-allow-icmp | icmp desde 0.0.0.0/0
            %% @part reglas | default-allow-internal | Todo tcp, udp e icmp desde 10.128.0.0/9
            %% @part reglas | default-allow-rdp | tcp:3389 desde 0.0.0.0/0
            %% @part reglas | default-allow-ssh | tcp:22 desde 0.0.0.0/0
            Container(reglas, "Reglas de firewall", "Cloud Firewall", "Las 4 reglas de entrada de default; se borran primero")
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Abre Red de VPC", "HTTPS")
    Rel(consola, api_compute, "Lista y borra la red y sus reglas", "JSON/HTTPS")
    Rel(api_compute, rutas, "Lista las rutas")
    Rel(api_compute, reglas, "Borra las reglas")
    Rel(rutas, igw, "Manda 0.0.0.0/0")
    Rel(rutas, subred_us, "Ruta local 10.128.0.0/20")
    Rel(rutas, subred_eu, "Ruta local 10.132.0.0/20")

    %% @step estudiante navegador | Abre Red de VPC > Redes de VPC
    %% @step navegador consola | Pide la lista de redes | GET /networking/networks/list HTTP/1.1\nHost: console.cloud.google.com
    %% @step consola api_compute | Lista las redes y sus subredes | GET /compute/v1/projects/PROYECTO/global/networks HTTP/1.1\nHost: compute.googleapis.com
    %% @step api_compute consola | default: modo automático, una subred por región
    %% @step consola api_compute | Rutas: red default, región us-central1, Ver
    %% @step api_compute rutas | Lee las rutas de default
    %% @step rutas subred_us | Una ruta por subred: 10.128.0.0/20, 10.132.0.0/20…
    %% @step rutas igw | La ruta 0.0.0.0/0 sale por la puerta de enlace de Internet
    %% @step rutas api_compute | Devuelve las rutas: las de subred y la de 0.0.0.0/0
    %% @step api_compute reglas | Lee el firewall: allow-icmp, -internal, -rdp y -ssh
    %% @step consola api_compute | Borra las 4 reglas | DELETE /compute/v1/projects/PROYECTO/global/firewalls/default-allow-icmp HTTP/1.1\nHost: compute.googleapis.com
    %% @step api_compute reglas | Borra default-allow-icmp, -internal, -rdp y -ssh
    %% @step consola api_compute | Borra la red default | DELETE /compute/v1/projects/PROYECTO/global/networks/default HTTP/1.1\nHost: compute.googleapis.com
    %% @step api_compute api_compute | Borra sus subredes y sus rutas: Rutas y Firewall quedan vacíos
    %% @step consola api_compute | Crear instancia con los valores predeterminados
    %% @step api_compute consola | No hay ninguna red: la VM no tiene dónde ir | HTTP/1.1 400 Bad Request\n\n{"error": {"message": "Invalid value for field 'resource.networkInterfaces[0].network'"}}
    %% @step consola navegador | Ver los problemas: en Redes, «No hay más redes disponibles»
    %% @step navegador estudiante | Sin una red de VPC no se puede crear una VM
```