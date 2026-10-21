C4Deployment
    title Lab06 - Tarea 2 - Prepara el disco de datos

    %% @pos estudiante x=224 y=424 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Da formato al disco de datos y lo monta en /home/minecraft")

    %% @pos equipo x=560 y=372 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=604 y=428 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y la ventana SSH")
    }

    %% @pos ssh_navegador x=1032 y=424 kind=terminal url=https://ssh.cloud.google.com/v2/ssh/projects/PROYECTO/zones/us-central1-c/instances/mc-server
    Container(ssh_navegador, "SSH en el navegador", "ssh.cloud.google.com", "La terminal de mc-server en otra pestaña")

    %% @pos proyecto x=1456 y=-200 w=1220 h=836 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos default x=1480 y=-144 w=1172 h=756 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos regla_ssh x=1504 y=-88 kind=firewall
            Container(regla_ssh, "default-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 0.0.0.0/0: la trae la red default")
            %% @pos subred x=1504 y=80 w=1124 h=508 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1528 y=136 w=1076 h=428 kind=appserver
                %% @part vm | Discos | sda: el de arranque; sdb: minecraft-disk
                Deployment_Node(vm, "mc-server", "Compute Engine · Debian 12", "us-central1-c · e2-medium") {
                    %% @pos ip_estatica x=1572 y=196 kind=interface
                    Container(ip_estatica, "IP externa estática", "203.0.113.30", "mc-server-ip")
                    %% @pos nic x=2000 y=192 kind=interface
                    Container(nic, "nic0", "10.128.0.2", "La IP interna")
                    %% @pos sshd x=1552 y=420 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos bash_vm x=1936 y=420 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "mkdir, mkfs.ext4 y mount, con sudo")
                    %% @pos disco_datos x=2380 y=416 kind=storage
                    %% @part disco_datos | Nombre de dispositivo | /dev/disk/by-id/google-minecraft-disk (sdb)
                    %% @part disco_datos | Sistema de archivos | ext4, creado con mkfs.ext4
                    %% @part disco_datos | Punto de montaje | /home/minecraft, con las opciones discard,defaults
                    %% @file disco_datos | lost+found/
                    ContainerDb(disco_datos, "minecraft-disk", "Persistent Disk SSD (pd-ssd)", "50 GB en ext4, montado en /home/minecraft")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, ssh_navegador, "Abre la ventana SSH", "WebSocket/HTTPS")
    Rel(ip_estatica, nic, "Traduce a la IP interna", "NAT 1:1")
    %% @door default | Entra a la VPC\ndefault-allow-ssh:\npermite 22/TCP desde 0.0.0.0/0 (Internet)
    %% @door subred | Ruta de la subred 10.128.0.0/20\n→ 203.0.113.30:22 (TCP)
    %% @door vm | IP externa estática · 203.0.113.30\ndefault-allow-ssh:\npermite 22/TCP desde 0.0.0.0/0 (Internet)
    %% @door sshd | Escucha en el puerto 22 (SSH)\nCon una llave temporal\nagregada a los metadatos
    Rel(ssh_navegador, sshd, "Abre una sesión", "SSH")
    Rel(sshd, bash_vm, "Abre la terminal")
    Rel(bash_vm, disco_datos, "Le da formato y lo monta", "ext4")

    %% @step estudiante navegador | SSH en la fila de mc-server
    %% @step navegador ssh_navegador | Abre la ventana en otra pestaña
    %% @step ssh_navegador sshd | Abre la sesión: default-allow-ssh deja pasar el 22
    %% @step sshd bash_vm | estudiante@mc-server
    %% @step bash_vm bash_vm | sudo mkdir -p /home/minecraft
    %% @step bash_vm disco_datos | sudo mkfs.ext4 -F … google-minecraft-disk | $ sudo mkfs.ext4 -F -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/disk/by-id/google-minecraft-disk\nmke2fs 1.47.0 (5-Feb-2023)\nDiscarding device blocks: done\nCreating filesystem with 13107200 4k blocks and 3276800 inodes\nFilesystem UUID: …\nSuperblock backups stored on blocks:\n    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,\n    4096000, 7962624, 11239424\n\nAllocating group tables: done\nWriting inode tables: done\nCreating journal (65536 blocks): done\nWriting superblocks and filesystem accounting information: done
    %% @step bash_vm disco_datos | sudo mount … /home/minecraft | $ sudo mount -o discard,defaults /dev/disk/by-id/google-minecraft-disk /home/minecraft
    %% @step bash_vm bash_vm | El disco de 50 GB queda en /home/minecraft
