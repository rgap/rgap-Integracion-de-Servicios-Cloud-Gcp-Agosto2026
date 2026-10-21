```
C4Deployment
    title Lab06 - Tarea 6 - Mantenimiento del servidor

    %% @pos estudiante x=-164 y=472 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Detiene el servidor y agrega los scripts de inicio y apagado a mc-server")

    %% @pos equipo x=220 y=424 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=480 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la ventana SSH y la consola")
    }

    %% @pos consola x=584 y=56 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Detiene mc-server y edita sus metadatos")

    %% @pos ssh_navegador x=700 y=480 kind=terminal url=https://ssh.cloud.google.com/v2/ssh/projects/PROYECTO/zones/us-central1-c/instances/mc-server
    Container(ssh_navegador, "SSH en el navegador", "ssh.cloud.google.com", "La terminal de mc-server en otra pestaña")

    %% @pos training x=3172 y=640 kind=storage url=https://storage.googleapis.com/cloud-training
    %% @file training | archinfra/mcserver/startup.sh
    %% @file training | archinfra/mcserver/shutdown.sh
    ContainerDb(training, "cloud-training", "Cloud Storage", "Bucket público de Google: los scripts del lab")

    %% @pos proyecto x=1100 y=-200 w=1880 h=1448 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1124 y=60 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Detiene la VM y guarda sus metadatos")
        %% @pos metadatos x=2768 y=232 kind=external
        %% @part metadatos | startup-script-url | https://storage.googleapis.com/cloud-training/archinfra/mcserver/startup.sh
        %% @part metadatos | shutdown-script-url | https://storage.googleapis.com/cloud-training/archinfra/mcserver/shutdown.sh
        System_Ext(metadatos, "Servidor de metadatos", "Dice a la VM de dónde bajar sus scripts")
        %% @pos default x=1480 y=-144 w=1172 h=1368 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos regla_ssh x=1504 y=-88 kind=firewall
            Container(regla_ssh, "default-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 0.0.0.0/0: la trae la red default")
            %% @pos subred x=1504 y=36 w=1124 h=1164 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1528 y=92 w=1076 h=1084 kind=appserver
                %% @part vm | Metadatos | startup-script-url y shutdown-script-url
                Deployment_Node(vm, "mc-server", "Compute Engine · Debian 12", "us-central1-c · e2-medium") {
                    %% @pos ip_estatica x=1552 y=232 kind=interface
                    Container(ip_estatica, "IP externa estática", "203.0.113.30", "mc-server-ip: la misma tras detener e iniciar")
                    %% @pos disco_datos x=1804 y=236 kind=storage
                    ContainerDb(disco_datos, "minecraft-disk", "Persistent Disk SSD (pd-ssd)", "/home/minecraft: el servidor y su mundo")
                    %% @pos script_inicio x=2176 y=148 kind=generic
                    Container(script_inicio, "startup.sh", "startup-script-url", "Monta el disco y arranca el servidor en screen")
                    %% @pos sshd x=1552 y=480 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos screen x=2108 y=1032 kind=terminal
                    Container(screen, "Sesión de screen", "GNU screen", "mcs, de root")
                    %% @pos script_apagado x=2380 y=628 kind=generic
                    Container(script_apagado, "shutdown.sh", "shutdown-script-url", "Envía /stop al servidor antes de apagar")
                    %% @pos bash_vm x=1552 y=720 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "Detiene el servidor con /stop")
                    %% @pos minecraft x=1872 y=744 kind=appserver
                    Container(minecraft, "Servidor de Minecraft", "Java · server.jar · TCP 25565", "Guarda el mundo y se detiene con /stop")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, ssh_navegador, "Abre la ventana SSH", "WebSocket/HTTPS")
    %% @door default | Entra a la VPC\ndefault-allow-ssh:\npermite 22/TCP desde 0.0.0.0/0 (Internet)
    %% @door subred | Ruta de la subred 10.128.0.0/20\n→ 203.0.113.30:22 (TCP)
    %% @door vm | IP externa estática · 203.0.113.30\ndefault-allow-ssh:\npermite 22/TCP desde 0.0.0.0/0 (Internet)
    %% @door sshd | Escucha en el puerto 22 (SSH)\nCon una llave temporal\nagregada a los metadatos
    Rel(ssh_navegador, sshd, "Abre una sesión", "SSH")
    Rel(sshd, bash_vm, "Abre la terminal")
    Rel(bash_vm, screen, "Envía /stop al servidor", "screen -X stuff")
    Rel(screen, minecraft, "Ejecuta el servidor y le pasa sus comandos")
    %% @rel points=2108,780;2108,290
    Rel(minecraft, disco_datos, "Lee y escribe sus archivos", "ext4")
    Rel(navegador, consola, "Detiene la VM y edita sus metadatos", "HTTPS")
    Rel(consola, api_compute, "Detiene la VM y guarda los metadatos", "JSON/HTTPS")
    %% @rel points=1200,-280;2636,-280
    Rel(api_compute, metadatos, "Guarda las URL de los scripts")
    Rel(script_inicio, metadatos, "Lee la URL del script", "HTTP")
    Rel(script_apagado, metadatos, "Lee la URL del script", "HTTP")
    %% @door vm | IP externa estática · 203.0.113.30\n→ storage.googleapis.com:443 (TCP)
    %% @door default | Ruta 0.0.0.0/0\n→ puerta de enlace de Internet\ncon la IP externa de la VM
    %% @door training | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de storage.googleapis.com\nBucket público: lo lee cualquiera\n(allUsers)
    Rel(script_inicio, training, "Se descarga del bucket", "HTTPS")
    Rel(script_apagado, training, "Se descarga del bucket", "HTTPS")
    Rel(script_inicio, disco_datos, "Monta el disco", "ext4")
    Rel(script_inicio, screen, "Arranca el servidor en screen", "screen -d -m")
    Rel(script_apagado, screen, "Envía /stop al servidor", "screen -X stuff")

    %% @step bash_vm screen | sudo screen -r -X stuff '/stop\n'
    %% @step screen minecraft | /stop: guarda el mundo y se detiene | [19:02:11] [Server thread/INFO]: Stopping the server\n[19:02:11] [Server thread/INFO]: Stopping server\n[19:02:11] [Server thread/INFO]: Saving players\n[19:02:11] [Server thread/INFO]: Saving worlds\n[19:02:11] [Server thread/INFO]: Saving chunks for level 'ServerLevel[world]'/minecraft:overworld\n[19:02:11] [Server thread/INFO]: ThreadedAnvilChunkStorage (world): All chunks are saved
    %% @step estudiante navegador | Instancias de VM: mc-server > Detener
    %% @step consola api_compute | Detiene mc-server | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances/mc-server/stop HTTP/1.1\nHost: compute.googleapis.com
    %% @step api_compute consola | Detenida: la sesión SSH se cierra
    %% @step navegador consola | Editar > Metadatos: dos elementos; Guardar
    %% @step consola api_compute | Guarda los metadatos | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances/mc-server/setMetadata HTTP/1.1\nHost: compute.googleapis.com\n\n{"items": [\n  {"key": "startup-script-url", "value": "https://storage.googleapis.com/cloud-training/archinfra/mcserver/startup.sh"},\n  {"key": "shutdown-script-url", "value": "https://storage.googleapis.com/cloud-training/archinfra/mcserver/shutdown.sh"}]}
    %% @step api_compute metadatos | Guarda las dos URL
    %% @step script_inicio metadatos | Al iniciar la VM: startup-script-url
    %% @step script_inicio training | Descarga startup.sh | #!/bin/bash\nmount /dev/disk/by-id/google-minecraft-disk /home/minecraft\ncd /home/minecraft\nsudo screen -d -m -S mcs java -Xmx1024M -Xms1024M -jar server.jar nogui
    %% @step script_inicio disco_datos | Monta minecraft-disk en /home/minecraft
    %% @step script_inicio screen | screen -d -m -S mcs java … nogui
    %% @step screen minecraft | El servidor vuelve solo, en mcs
    %% @step script_apagado metadatos | Al detener la VM: shutdown-script-url
    %% @step script_apagado training | Descarga shutdown.sh | #!/bin/bash\nsudo screen -r -X stuff '/stop\n'
    %% @step script_apagado screen | /stop: el servidor guarda el mundo antes de apagarse
```