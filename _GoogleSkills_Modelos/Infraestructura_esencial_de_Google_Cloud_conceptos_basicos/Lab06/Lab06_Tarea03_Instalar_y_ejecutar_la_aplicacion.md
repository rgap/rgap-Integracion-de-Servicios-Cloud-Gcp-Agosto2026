```
C4Deployment
    title Lab06 - Tarea 3 - Instala y ejecuta la aplicación

    %% @pos estudiante x=204 y=396 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Instala Java, descarga el servidor de Minecraft y lo deja corriendo en screen")

    %% @pos equipo x=548 y=352 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=592 y=408 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la ventana SSH")
    }

    %% @pos ssh_navegador x=1012 y=408 kind=terminal url=https://ssh.cloud.google.com/v2/ssh/projects/PROYECTO/zones/us-central1-c/instances/mc-server
    Container(ssh_navegador, "SSH en el navegador", "ssh.cloud.google.com", "La terminal de mc-server en otra pestaña")

    %% @pos debian x=2544 y=156 kind=external url=https://deb.debian.org/debian
    System_Ext(debian, "Repositorio de Debian", "De aquí bajan Java (default-jre-headless) y screen")

    %% @pos mojang x=2576 y=420 kind=external url=https://launcher.mojang.com
    System_Ext(mojang, "Descargas de Mojang", "De aquí baja server.jar, el servidor de Minecraft")

    %% @pos proyecto x=1456 y=-184 w=1016 h=1080 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos default x=1480 y=-128 w=968 h=1000 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos regla_ssh x=1512 y=-72 kind=firewall
            Container(regla_ssh, "default-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 0.0.0.0/0: la trae la red default")
            %% @pos subred x=1504 y=80 w=920 h=768 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1528 y=136 w=872 h=688 kind=appserver
                %% @part vm | Paquetes instalados | default-jre-headless (OpenJDK 17), wget y screen
                Deployment_Node(vm, "mc-server", "Compute Engine · Debian 12", "us-central1-c · e2-medium") {
                    %% @pos ip_estatica x=1552 y=192 kind=interface
                    Container(ip_estatica, "IP externa estática", "203.0.113.30", "mc-server-ip")
                    %% @pos nic x=1864 y=192 kind=interface
                    Container(nic, "nic0", "10.128.0.2", "La IP interna")
                    %% @pos sshd x=1552 y=420 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos bash_vm x=1864 y=420 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "apt-get, wget, java, nano y screen")
                    %% @pos screen x=1864 y=680 kind=terminal
                    %% @part screen | Sesión mcs | sudo screen -S mcs: es de root
                    %% @part screen | Desconectarse | Ctrl+A y luego Ctrl+D
                    %% @part screen | Volver | sudo screen -r mcs
                    Container(screen, "Sesión de screen", "GNU screen", "mcs: mantiene el servidor al cerrar SSH")
                    %% @pos minecraft x=2176 y=680 kind=appserver
                    %% @part minecraft | Memoria | -Xmx1024M -Xms1024M: 1 GB para Java
                    %% @part minecraft | eula.txt | eula=true, editado con nano
                    %% @part minecraft | server.properties | server-port=25565, max-players=20
                    Container(minecraft, "Servidor de Minecraft", "Java · server.jar · TCP 25565", "Escucha en el puerto 25565 dentro de screen")
                    %% @pos disco_datos x=1552 y=680 kind=storage
                    %% @file disco_datos | server.jar | | 47 MB
                    %% @file disco_datos | eula.txt
                    %% @file disco_datos | server.properties
                    %% @file disco_datos | logs/
                    %% @file disco_datos | world/
                    ContainerDb(disco_datos, "minecraft-disk", "Persistent Disk SSD (pd-ssd)", "Montado en /home/minecraft: el servidor y su mundo")
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
    %% @door vm | IP externa estática · 203.0.113.30\n→ deb.debian.org:443 (TCP)
    %% @door default | Ruta 0.0.0.0/0\n→ puerta de enlace de Internet\ncon la IP externa de la VM
    %% @door debian | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de deb.debian.org
    Rel(bash_vm, debian, "apt-get update e install", "HTTPS :443")
    %% @door vm | IP externa estática · 203.0.113.30\n→ launcher.mojang.com:443 (TCP)
    %% @door default | Ruta 0.0.0.0/0\n→ puerta de enlace de Internet\ncon la IP externa de la VM
    %% @door mojang | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de launcher.mojang.com
    Rel(bash_vm, mojang, "Descarga server.jar", "HTTPS :443")
    Rel(bash_vm, disco_datos, "Guarda server.jar y edita eula.txt", "ext4")
    Rel(bash_vm, screen, "Abre una sesión de screen")
    Rel(screen, minecraft, "Ejecuta el servidor y le pasa sus comandos")
    %% @rel points=2220,928;1764,928
    Rel(minecraft, disco_datos, "Lee y escribe sus archivos", "ext4")

    %% @step estudiante navegador | SSH en la fila de mc-server
    %% @step navegador ssh_navegador | Abre la ventana
    %% @step ssh_navegador sshd | Abre la sesión
    %% @step sshd bash_vm | estudiante@mc-server
    %% @step bash_vm debian | sudo apt-get update
    %% @step bash_vm debian | sudo apt-get install -y default-jre-headless | Instala default-jre-headless y openjdk-17-jre-headless:\nJava 17, sin interfaz gráfica
    %% @step bash_vm mojang | cd /home/minecraft; sudo wget …/server.jar | $ sudo wget https://launcher.mojang.com/v1/objects/d0d0fe2b1dc6ab4c65554cb734270872b72dadd6/server.jar\nResolving launcher.mojang.com (launcher.mojang.com)... …\nConnecting to launcher.mojang.com (launcher.mojang.com)|…|:443... connected.\nHTTP request sent, awaiting response... 200 OK\nLength: 49150256 (47M) [application/java-archive]\nSaving to: ‘server.jar’
    %% @step bash_vm disco_datos | server.jar queda en el disco de datos
    %% @step bash_vm bash_vm | sudo java … -jar server.jar nogui: pide el EULA | $ sudo java -Xmx1024M -Xms1024M -jar server.jar nogui\nStarting net.minecraft.server.Main\n[14:10:02] [ServerMain/WARN]: Failed to load properties from file: server.properties\n[14:10:02] [ServerMain/WARN]: Failed to load eula.txt\n[14:10:02] [ServerMain/INFO]: You need to agree to the EULA in order to run the server. Go to eula.txt for more info.
    %% @step bash_vm disco_datos | sudo nano eula.txt: eula=true | #By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n#…\neula=true
    %% @step bash_vm debian | sudo apt-get install -y screen
    %% @step bash_vm screen | sudo screen -S mcs java … nogui
    %% @step screen minecraft | Arranca: Done | [14:12:40] [Server thread/INFO]: Starting minecraft server version (simulada)\n[14:12:40] [Server thread/INFO]: Starting Minecraft server on *:25565\n[14:12:40] [Server thread/INFO]: Preparing level "world"\n[14:12:42] [Worker-Main-2/INFO]: Preparing spawn area: 83%\n[14:12:42] [Server thread/INFO]: Time elapsed: 6123 ms\n[14:12:42] [Server thread/INFO]: Done (8.412s)! For help, type "help"
    %% @step minecraft disco_datos | Crea world/ y logs/ en /home/minecraft
    %% @step bash_vm screen | Ctrl+A, Ctrl+D: el servidor sigue en mcs
    %% @step bash_vm bash_vm | exit: cierra SSH; screen sigue
```