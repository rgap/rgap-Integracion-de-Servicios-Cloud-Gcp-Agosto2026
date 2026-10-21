C4Deployment
    title Lab05 - Tarea 4 - Repaso

    %% @pos estudiante x=-136 y=252 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Repasa las tres VMs: cada una con otra configuración")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y la ventana SSH")
    }

    %% @pos consola x=700 y=-40 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Crea las tres VMs y muestra sus registros")

    %% @pos ssh_navegador x=716 y=616 kind=terminal url=https://ssh.cloud.google.com/v2/ssh/projects/PROYECTO/zones/us-central1-c/instances/utility-cm
    Container(ssh_navegador, "SSH en el navegador", "ssh.cloud.google.com", "La terminal de utility-cm en otra pestaña")

    %% @pos proyecto x=1100 y=-200 w=1452 h=1064 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1124 y=-40 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea las tres VMs")
        %% @pos logging x=1124 y=220 kind=external url=https://logging.googleapis.com
        System_Ext(logging, "Cloud Logging", "Guarda el registro de auditoría de cada VM que se crea o cambia")
        %% @pos default x=1480 y=-144 w=1048 h=984 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos regla_ssh x=1504 y=-88 kind=firewall
            Container(regla_ssh, "default-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 0.0.0.0/0")
            %% @pos regla_rdp x=1856 y=-88 kind=firewall
            Container(regla_rdp, "default-allow-rdp", "Regla de Cloud Firewall · entrada", "Permite tcp:3389 desde 0.0.0.0/0")
            %% @pos regla_http x=2208 y=-88 kind=firewall
            %% @part regla_http | default-allow-https | tcp:443 a la etiqueta https-server
            Container(regla_http, "default-allow-http", "Regla de Cloud Firewall · entrada", "Permite tcp:80 a la etiqueta http-server; y -https, tcp:443")
            %% @pos subred x=1504 y=120 w=1000 h=696 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm_utility x=1528 y=176 w=248 h=408 kind=appserver
                %% @part vm_utility | Tipo de máquina | e2-medium: 2 vCPU compartidas y 4 GB
                %% @part vm_utility | IP externa | Ninguna
                Deployment_Node(vm_utility, "utility-vm", "Compute Engine · Debian 12", "e2-medium, sin IP externa") {
                    %% @pos nic_vm x=1552 y=232 kind=interface
                    Container(nic_vm, "nic0", "10.128.0.2", "Solo IP interna")
                    %% @pos disco_vm x=1552 y=440 kind=storage
                    ContainerDb(disco_vm, "Disco de arranque", "Persistent Disk (pd-balanced)", "10 GB con Debian 12")
                }
                %% @pos vm_windows x=1856 y=176 w=280 h=616 kind=appserver
                %% @part vm_windows | Tipo de máquina | e2-standard-2: 2 vCPU y 8 GB
                %% @part vm_windows | Etiquetas de red | http-server y https-server
                Deployment_Node(vm_windows, "utility-wm", "Compute Engine · Windows Server 2025 Datacenter Core", "e2-standard-2, SSD de 64 GB") {
                    %% @pos ip_wm x=1904 y=232 kind=interface
                    Container(ip_wm, "IP externa", "203.0.113.21", "Efímera")
                    %% @pos nic_wm x=1904 y=440 kind=interface
                    Container(nic_wm, "nic0", "10.128.0.3", "La IP interna")
                    %% @pos rdp x=1904 y=648 kind=generic
                    Container(rdp, "Escritorio remoto", "RDP · TCP 3389", "Con la contraseña de Windows")
                }
                %% @pos vm_custom x=2232 y=176 w=248 h=616 kind=appserver
                %% @part vm_custom | Tipo de máquina | Personalizado: e2-custom-2-4096, 2 vCPU y 4 GB
                Deployment_Node(vm_custom, "utility-cm", "Compute Engine · Debian 12", "e2-custom-2-4096") {
                    %% @pos ip_cm x=2256 y=232 kind=interface
                    Container(ip_cm, "IP externa", "203.0.113.22", "Efímera")
                    %% @pos sshd x=2256 y=648 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos bash_vm x=2256 y=440 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "free, nproc y lscpu: 2 vCPU y 4 GB")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea las tres VMs", "HTTPS")
    Rel(consola, api_compute, "Crea las VMs", "JSON/HTTPS")
    Rel(api_compute, logging, "Registra cada operación")
    Rel(consola, logging, "Muestra los registros", "HTTPS")
    Rel(ip_wm, nic_wm, "Traduce a la IP interna", "NAT 1:1")
    %% @door rdp | Escucha en el puerto 3389 (RDP)\nCon usuario y contraseña de Windows
    Rel(nic_wm, rdp, "Entrega al puerto", "RDP :3389")
    Rel(navegador, ssh_navegador, "Abre la ventana SSH", "WebSocket/HTTPS")
    %% @rel points=900,840;2330,840
    %% @door default | Entra a la VPC\ndefault-allow-ssh:\npermite 22/TCP desde 0.0.0.0/0 (Internet)
    %% @door subred | Ruta de la subred 10.128.0.0/20\n→ 203.0.113.22:22 (TCP)
    %% @door vm_custom | IP externa · 203.0.113.22\ndefault-allow-ssh:\npermite 22/TCP desde 0.0.0.0/0 (Internet)
    %% @door sshd | Escucha en el puerto 22 (SSH)\nCon una llave temporal\nagregada a los metadatos
    Rel(ssh_navegador, sshd, "Abre una sesión", "SSH")
    Rel(sshd, bash_vm, "Abre la terminal")

    %% @step estudiante navegador | Tres VMs en la misma subred, cada una distinta
    %% @step consola api_compute | utility-vm: e2-medium, sin IP externa
    %% @step consola api_compute | utility-wm: Windows Server 2025, SSD de 64 GB, HTTP y HTTPS
    %% @step consola api_compute | utility-cm: personalizado, 2 vCPU y 4 GB
    %% @step api_compute logging | Cada creación queda en el registro de auditoría
    %% @step ip_wm nic_wm | utility-wm se usaría por RDP, con su contraseña de Windows
    %% @step nic_wm rdp | default-allow-rdp deja pasar el 3389
    %% @step navegador ssh_navegador | utility-cm, por SSH en el navegador
    %% @step ssh_navegador sshd | default-allow-ssh deja pasar el 22
    %% @step sshd bash_vm | free, nproc y lscpu confirman lo configurado
