```
C4Deployment
    title Lab06 - Tarea 4 - Permite el tráfico de los clientes

    %% @pos estudiante x=-136 y=252 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Abre el puerto 25565 y comprueba que el servidor responde")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y el comprobador")
    }

    %% @pos consola x=700 y=40 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Crea minecraft-rule y muestra mc-server-ip")

    %% @pos comprobador x=700 y=480 kind=external url=https://mcsrvstat.us
    System_Ext(comprobador, "Comprobador de estado de Minecraft", "Prueba desde Internet la IP externa de mc-server en el puerto 25565")

    %% @pos proyecto x=1100 y=-196 w=1508 h=892 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1124 y=40 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea la regla de firewall")
        %% @pos default x=1480 y=-140 w=1104 h=812 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos regla_mc x=1544 y=-84 kind=firewall
            %% @part regla_mc | Destinos | Etiqueta minecraft-server: solo mc-server la tiene
            %% @part regla_mc | Origen | 0.0.0.0/0: desde cualquier dirección
            %% @part regla_mc | Protocolos y puertos | tcp:25565
            Container(regla_mc, "minecraft-rule", "Regla de Cloud Firewall · entrada", "Permite tcp:25565 desde 0.0.0.0/0 a la etiqueta minecraft-server")
            %% @pos subred x=1504 y=128 w=1056 h=520 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1528 y=184 w=1008 h=440 kind=appserver
                %% @part vm | Etiquetas de red | minecraft-server
                Deployment_Node(vm, "mc-server", "Compute Engine · Debian 12", "us-central1-c · e2-medium") {
                    %% @pos screen x=2300 y=240 kind=terminal
                    Container(screen, "Sesión de screen", "GNU screen", "mcs, de root: el servidor sigue tras cerrar SSH")
                    %% @pos ip_estatica x=1552 y=480 kind=interface
                    Container(ip_estatica, "IP externa estática", "203.0.113.30", "mc-server-ip, en Red de VPC > Direcciones IP")
                    %% @pos nic x=1944 y=480 kind=interface
                    Container(nic, "nic0", "10.128.0.2", "La IP interna")
                    %% @pos minecraft x=2312 y=480 kind=appserver
                    Container(minecraft, "Servidor de Minecraft", "Java · server.jar · TCP 25565", "Escucha en el puerto 25565")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea minecraft-rule", "HTTPS")
    Rel(consola, api_compute, "Crea la regla", "JSON/HTTPS")
    Rel(api_compute, regla_mc, "Crea la regla de firewall")
    Rel(navegador, comprobador, "Prueba la dirección", "HTTPS")
    %% @door default | Entra a la VPC\nminecraft-rule:\npermite 25565/TCP desde 0.0.0.0/0 (Internet)
    %% @door subred | Ruta de la subred 10.128.0.0/20\n→ 203.0.113.30:25565 (TCP)
    %% @door vm | IP externa estática · 203.0.113.30\nminecraft-rule:\npermite 25565/TCP desde 0.0.0.0/0 (Internet)
    Rel(comprobador, ip_estatica, "Consulta el estado del servidor", "Minecraft/TCP")
    Rel(ip_estatica, nic, "Traduce a la IP interna", "NAT 1:1")
    %% @door minecraft | Escucha en el puerto 25565 (Minecraft)
    Rel(nic, minecraft, "Entrega al puerto", "TCP :25565")
    Rel(screen, minecraft, "Ejecuta el servidor y le pasa sus comandos")

    %% @step estudiante navegador | Red de VPC > Firewall > Crear regla de firewall
    %% @step navegador consola | minecraft-rule: etiqueta minecraft-server, 0.0.0.0/0, tcp:25565
    %% @step consola api_compute | Crea minecraft-rule | POST /compute/v1/projects/PROYECTO/global/firewalls HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "minecraft-rule", "network": "global/networks/default",\n "direction": "INGRESS", "priority": 1000,\n "targetTags": ["minecraft-server"], "sourceRanges": ["0.0.0.0/0"],\n "allowed": [{"IPProtocol": "tcp", "ports": ["25565"]}]}
    %% @step api_compute regla_mc | Se aplica a las VMs con la etiqueta
    %% @step navegador consola | Red de VPC > Direcciones IP: copia mc-server-ip
    %% @step navegador comprobador | Prueba 203.0.113.30
    %% @step comprobador ip_estatica | Se conecta al 25565: minecraft-rule lo deja pasar
    %% @step ip_estatica nic | 203.0.113.30 → 10.128.0.2
    %% @step nic minecraft | Entrega al puerto 25565
    %% @step comprobador navegador | En línea | En línea\nJugadores: 0 / 20 · MOTD: A Minecraft Server
```