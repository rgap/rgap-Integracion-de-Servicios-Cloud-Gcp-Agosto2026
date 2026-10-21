C4Deployment
    title Lab06 - Tarea 5 - Programa copias de seguridad periódicas

    %% @pos estudiante x=76 y=316 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Crea el bucket de respaldo, escribe backup.sh y lo programa cada 4 horas")

    %% @pos equipo x=452 y=264 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=496 y=320 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la ventana SSH y la consola")
    }

    %% @pos consola x=952 y=84 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Muestra las copias en Cloud Storage > Buckets")

    %% @pos ssh_navegador x=908 y=440 kind=terminal url=https://ssh.cloud.google.com/v2/ssh/projects/PROYECTO/zones/us-central1-c/instances/mc-server
    Container(ssh_navegador, "SSH en el navegador", "ssh.cloud.google.com", "La terminal de mc-server en otra pestaña")

    %% @pos proyecto x=1456 y=-148 w=1416 h=1324 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos metadatos x=2640 y=376 kind=external
        %% @part metadatos | Token de la cuenta de servicio | …/service-accounts/default/token, con el alcance devstorage.read_write
        System_Ext(metadatos, "Servidor de metadatos", "Da a gcloud el token de la cuenta de servicio de la VM")
        %% @pos bucket x=2648 y=700 kind=storage url=https://storage.googleapis.com/PROYECTO-minecraft-backup
        %% @file bucket | 20261020-141530-world/
        ContainerDb(bucket, "PROYECTO-minecraft-backup", "Cloud Storage", "Las copias del mundo, una carpeta por fecha y hora")
        %% @pos default x=1480 y=-92 w=1088 h=1244 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos regla_ssh x=1540 y=-36 kind=firewall
            Container(regla_ssh, "default-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 0.0.0.0/0: la trae la red default")
            %% @pos subred x=1504 y=136 w=1040 h=992 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1528 y=192 w=992 h=912 kind=appserver
                %% @part vm | Permisos de acceso | Storage: lectura y escritura; por eso gcloud puede crear el bucket y subir
                Deployment_Node(vm, "mc-server", "Compute Engine · Debian 12", "us-central1-c · e2-medium") {
                    %% @pos ip_estatica x=1572 y=248 kind=interface
                    Container(ip_estatica, "IP externa estática", "203.0.113.30", "mc-server-ip")
                    %% @pos sshd x=1552 y=440 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos bash_vm x=1864 y=440 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "export, gcloud, nano, chmod y crontab")
                    %% @pos gcloud x=2176 y=440 kind=terminal
                    Container(gcloud, "gcloud", "Google Cloud CLI", "Crea el bucket y copia el mundo con gcloud storage")
                    %% @pos cron x=1552 y=700 kind=generic
                    %% @part cron | Crontab de root | sudo crontab -e
                    %% @part cron | Línea | 0 */4 * * * /home/minecraft/backup.sh
                    Container(cron, "Tarea programada", "cron", "Ejecuta backup.sh cada 4 horas, como root")
                    %% @pos backup x=1864 y=700 kind=generic
                    %% @part backup | Ruta | /home/minecraft/backup.sh, con permisos 755
                    %% @part backup | Pasos | /save-all y /save-off; gcloud storage cp -R world; /save-on
                    Container(backup, "backup.sh", "Bash", "Copia de seguridad del mundo al bucket")
                    %% @pos disco_datos x=1552 y=960 kind=storage
                    ContainerDb(disco_datos, "minecraft-disk", "Persistent Disk SSD (pd-ssd)", "/home/minecraft: world/ y backup.sh")
                    %% @pos screen x=1852 y=960 kind=terminal
                    Container(screen, "Sesión de screen", "GNU screen", "mcs, de root")
                    %% @pos minecraft x=2296 y=956 kind=appserver
                    Container(minecraft, "Servidor de Minecraft", "Java · server.jar · TCP 25565", "Guarda el mundo cuando se lo piden")
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
    Rel(bash_vm, gcloud, "Ejecuta")
    Rel(gcloud, metadatos, "Pide el token de la cuenta de servicio", "HTTP")
    %% @door vm | IP externa estática · 203.0.113.30\n→ storage.googleapis.com:443 (TCP)
    %% @door default | Ruta 0.0.0.0/0\n→ puerta de enlace de Internet\ncon la IP externa de la VM
    %% @door bucket | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de storage.googleapis.com\nCon el token de la cuenta de servicio\nde la VM: su alcance de Storage\nlo permite
    Rel(gcloud, bucket, "Crea el bucket y copia archivos", "JSON/HTTPS")
    Rel(bash_vm, backup, "Ejecuta")
    Rel(bash_vm, cron, "Programa la tarea", "crontab -e")
    Rel(cron, backup, "Lo ejecuta según su horario")
    Rel(backup, screen, "Pausa el guardado mientras copia", "screen -X stuff")
    Rel(backup, disco_datos, "Lee world/", "ext4")
    %% @door vm | IP externa estática · 203.0.113.30\n→ storage.googleapis.com:443 (TCP)
    %% @door default | Ruta 0.0.0.0/0\n→ puerta de enlace de Internet\ncon la IP externa de la VM
    %% @door bucket | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de storage.googleapis.com\nCon el token de la cuenta de servicio\nde la VM: su alcance de Storage\nlo permite
    Rel(backup, bucket, "Sube las copias", "HTTPS")
    Rel(screen, minecraft, "Ejecuta el servidor y le pasa sus comandos")
    %% @rel points=2260,1110;1630,1110
    Rel(minecraft, disco_datos, "Lee y escribe sus archivos", "ext4")
    %% @rel points=1056,-232;2932,-212;2880,760
    Rel(consola, bucket, "Muestra los objetos", "HTTPS")
    Rel(navegador, consola, "Abre Cloud Storage", "HTTPS")

    %% @step estudiante navegador | SSH en la fila de mc-server
    %% @step navegador ssh_navegador | Abre la ventana
    %% @step ssh_navegador sshd | Abre la sesión
    %% @step sshd bash_vm | estudiante@mc-server
    %% @step bash_vm bash_vm | export YOUR_BUCKET_NAME=PROYECTO
    %% @step bash_vm gcloud | gcloud storage buckets create gs://$YOUR_BUCKET_NAME-minecraft-backup
    %% @step gcloud metadatos | Token de la cuenta de servicio | GET /computeMetadata/v1/instance/service-accounts/default/token HTTP/1.1\nHost: metadata.google.internal\nMetadata-Flavor: Google
    %% @step gcloud bucket | Crea el bucket | Creating gs://PROYECTO-minecraft-backup/...
    %% @step bash_vm backup | sudo nano backup.sh; sudo chmod 755; . backup.sh | #!/bin/bash\nscreen -r mcs -X stuff '/save-all\\n/save-off\\n'\n/usr/bin/gcloud storage cp -R ${BASH_SOURCE%/*}/world gs://${YOUR_BUCKET_NAME}-minecraft-backup/$(date "+%Y%m%d-%H%M%S")-world\nscreen -r mcs -X stuff '/save-on\\n'
    %% @step backup screen | /save-all, /save-off: sin sesión | No screen session found.\n\n(La sesión mcs es de root y el script corre como estudiante)
    %% @step backup disco_datos | Lee /home/minecraft/world
    %% @step backup bucket | Sube world/ | Copying file:///home/minecraft/world/level.dat to gs://PROYECTO-minecraft-backup/20261020-141530-world/level.dat\nCopying file:///home/minecraft/world/region/r.0.0.mca to gs://PROYECTO-minecraft-backup/20261020-141530-world/region/r.0.0.mca\n…\n  Completed files 12/12 | …
    %% @step backup screen | /save-on: tampoco encuentra la sesión
    %% @step navegador consola | Cloud Storage > Buckets
    %% @step consola bucket | 20261020-141530-world/
    %% @step bash_vm cron | sudo crontab -e: 0 */4 * * * … | $ sudo crontab -e\nno crontab for root - using an empty one\n…\ncrontab: installing new crontab
    %% @step cron backup | Cada 4 horas, como root: ahí sí encuentra mcs
    %% @step screen minecraft | Saved the game | [18:00:00] [Server thread/INFO]: Saving the game (this may take a moment!)\n[18:00:00] [Server thread/INFO]: Saved the game\n[18:00:00] [Server thread/INFO]: Automatic saving is now disabled
