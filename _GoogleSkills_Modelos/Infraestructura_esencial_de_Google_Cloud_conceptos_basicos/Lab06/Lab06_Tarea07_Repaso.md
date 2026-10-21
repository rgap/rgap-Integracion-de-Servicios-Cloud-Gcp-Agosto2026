```
C4Deployment
    title Lab06 - Tarea 7 - Repaso

    %% @pos estudiante x=-156 y=248 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Repasa el servidor de Minecraft: disco, IP, puerto, copias y scripts")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Abre el comprobador de estado")
    }

    %% @pos comprobador x=700 y=232 kind=external url=https://mcsrvstat.us
    System_Ext(comprobador, "Comprobador de estado de Minecraft", "Prueba desde Internet la IP externa de mc-server en el puerto 25565")

    %% @pos proyecto x=1288 y=-200 w=2044 h=1308 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos default x=1312 y=-144 w=1732 h=1228 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos regla_mc x=1504 y=-88 kind=firewall
            Container(regla_mc, "minecraft-rule", "Regla de Cloud Firewall · entrada", "Permite tcp:25565 desde 0.0.0.0/0 a la etiqueta minecraft-server")
            %% @pos subred x=1336 y=120 w=1684 h=940 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1360 y=176 w=1636 h=860 kind=appserver
                %% @part vm | Tipo de máquina | e2-medium con Debian 12
                %% @part vm | Etiquetas de red | minecraft-server
                %% @part vm | Permisos de acceso | Storage: lectura y escritura
                %% @part vm | Metadatos | startup-script-url y shutdown-script-url
                Deployment_Node(vm, "mc-server", "Compute Engine · Debian 12", "us-central1-c · e2-medium") {
                    %% @pos ip_estatica x=1384 y=244 kind=interface
                    Container(ip_estatica, "IP externa estática", "203.0.113.30", "mc-server-ip: no cambia al detener la VM")
                    %% @pos nic x=1836 y=232 kind=interface
                    Container(nic, "nic0", "10.128.0.2", "La IP interna")
                    %% @pos minecraft x=2192 y=232 kind=appserver
                    Container(minecraft, "Servidor de Minecraft", "Java · server.jar · TCP 25565", "Escucha en el puerto 25565")
                    %% @pos disco_datos x=2672 y=236 kind=storage
                    ContainerDb(disco_datos, "minecraft-disk", "Persistent Disk SSD (pd-ssd)", "50 GB en ext4, montado en /home/minecraft")
                    %% @pos script_inicio x=1864 y=480 kind=generic
                    Container(script_inicio, "startup.sh", "startup-script-url", "Monta el disco y arranca el servidor en screen")
                    %% @pos screen x=2276 y=628 kind=terminal
                    Container(screen, "Sesión de screen", "GNU screen", "mcs: el servidor sigue sin SSH")
                    %% @pos script_apagado x=2772 y=516 kind=generic
                    Container(script_apagado, "shutdown.sh", "shutdown-script-url", "Envía /stop al servidor antes de apagar")
                    %% @pos cron x=1724 y=892 kind=generic
                    Container(cron, "Tarea programada", "cron", "0 */4 * * * /home/minecraft/backup.sh, de root")
                    %% @pos backup x=2352 y=892 kind=generic
                    Container(backup, "backup.sh", "Bash", "Copia de seguridad del mundo al bucket")
                }
            }
        }
        %% @pos bucket x=3108 y=892 kind=storage url=https://storage.googleapis.com/PROYECTO-minecraft-backup
        ContainerDb(bucket, "PROYECTO-minecraft-backup", "Cloud Storage", "Una copia del mundo por fecha y hora")
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, comprobador, "Prueba la dirección", "HTTPS")
    %% @door default | Entra a la VPC\nminecraft-rule:\npermite 25565/TCP desde 0.0.0.0/0 (Internet)
    %% @door subred | Ruta de la subred 10.128.0.0/20\n→ 203.0.113.30:25565 (TCP)
    %% @door vm | IP externa estática · 203.0.113.30\nminecraft-rule:\npermite 25565/TCP desde 0.0.0.0/0 (Internet)
    Rel(comprobador, ip_estatica, "Consulta el estado del servidor", "Minecraft/TCP")
    Rel(ip_estatica, nic, "Traduce a la IP interna", "NAT 1:1")
    %% @door minecraft | Escucha en el puerto 25565 (Minecraft)
    Rel(nic, minecraft, "Entrega al puerto", "TCP :25565")
    Rel(minecraft, disco_datos, "Lee y escribe sus archivos", "ext4")
    Rel(screen, minecraft, "Ejecuta el servidor y le pasa sus comandos")
    %% @rel label=60,-20
    Rel(script_inicio, disco_datos, "Monta el disco", "ext4")
    Rel(script_inicio, screen, "Arranca el servidor en screen", "screen -d -m")
    Rel(script_apagado, screen, "Envía /stop al servidor", "screen -X stuff")
    Rel(cron, backup, "Lo ejecuta según su horario")
    Rel(backup, screen, "Pausa el guardado mientras copia", "screen -X stuff")
    %% @door vm | IP externa estática · 203.0.113.30\n→ storage.googleapis.com:443 (TCP)
    %% @door default | Ruta 0.0.0.0/0\n→ puerta de enlace de Internet\ncon la IP externa de la VM
    %% @door bucket | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de storage.googleapis.com\nCon el token de la cuenta de servicio\nde la VM: su alcance de Storage\nlo permite
    Rel(backup, bucket, "Sube las copias", "HTTPS")

    %% @step estudiante navegador | mc-server: Debian 12, disco SSD de 50 GB e IP estática
    %% @step navegador comprobador | Prueba 203.0.113.30
    %% @step comprobador ip_estatica | minecraft-rule deja pasar el 25565
    %% @step ip_estatica nic | 203.0.113.30 → 10.128.0.2
    %% @step nic minecraft | El servidor responde: En línea
    %% @step screen minecraft | Corre en screen aunque se cierre SSH
    %% @step minecraft disco_datos | El mundo queda en el disco de datos
    %% @step cron backup | Cada 4 horas
    %% @step backup screen | /save-all y /save-off mientras copia
    %% @step backup bucket | Una copia del mundo por fecha y hora
    %% @step script_inicio screen | Al iniciar la VM: monta el disco y arranca el servidor
    %% @step script_apagado screen | Al detenerla: /stop, y el mundo se guarda
```