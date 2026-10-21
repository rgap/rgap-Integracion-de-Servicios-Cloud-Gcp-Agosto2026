C4Deployment
    title Lab04 - Tarea 3 - Configura una puerta de enlace de Cloud NAT

    %% @pos estudiante x=0 y=276 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Actualiza los paquetes en Cloud Shell y en la VM, y crea Cloud NAT")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y Cloud Shell")
    }

    %% @pos consola x=580 y=-160 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Servicios de red > Cloud NAT")

    %% @pos cloudshell x=676 y=260 w=248 h=404 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian", "Tiene IP externa") {
        %% @pos terminal x=700 y=316 kind=terminal
        Container(terminal, "Terminal web", "Bash", "sudo apt-get update")
        %% @pos gcloud x=700 y=520 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Abre el túnel SSH por IAP")
    }

    %% @pos iap x=1100 y=760 kind=external
    System_Ext(iap, "IAP", "Lleva SSH a vm-internal desde 35.235.240.0/20")

    %% @pos debian x=836 y=-804 kind=external url=https://deb.debian.org/debian
    %% @part debian | Distribuciones | bookworm, bookworm-updates, bookworm-backports y bookworm-security
    System_Ext(debian, "deb.debian.org", "Repositorio de Debian, en Internet")

    %% @pos gpkgs x=2620 y=192 kind=external url=https://packages.cloud.google.com/apt
    %% @part gpkgs | Repositorios | google-compute-engine-bookworm-stable y cloud-sdk-bookworm
    System_Ext(gpkgs, "packages.cloud.google.com", "Repositorio de Google: llega con Acceso privado a Google")

    %% @pos proyecto x=1100 y=-272 w=1368 h=888 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1124 y=-160 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea el Cloud Router con su NAT")
        %% @pos privatenet x=1480 y=-216 w=964 h=808 kind=cloud
        Deployment_Node(privatenet, "privatenet", "Google Cloud VPC", "Red de modo personalizado") {
            %% @pos regla_ssh x=1504 y=-160 kind=firewall
            Container(regla_ssh, "privatenet-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 35.235.240.0/20 (IAP) a todas las instancias")
            %% @pos router x=2180 y=-160 w=240 h=200 kind=generic
            Deployment_Node(router, "nat-router", "Cloud Router · us-central1", "Creado junto con el NAT") {
                %% @pos nat x=2204 y=-104 kind=generic
                %% @part nat | Subredes | Todos los rangos de las subredes de us-central1
                %% @part nat | IP de NAT | Automáticas
                Container(nat, "nat-config", "Cloud NAT", "Deja salir a Internet a las VMs sin IP externa de privatenet")
            }
            %% @pos subred x=1504 y=80 w=608 h=488 kind=generic
            %% @part subred | Acceso privado a Google | Activo desde la tarea 2
            Deployment_Node(subred, "Subred privatenet-us", "VPC de Google Cloud · 10.130.0.0/20", "us-central1") {
                %% @pos vm x=1528 y=136 w=560 h=408 kind=appserver
                %% @part vm | IP externa | Ninguna
                Deployment_Node(vm, "vm-internal", "Compute Engine · Debian 12", "us-central1-c · e2-standard-2") {
                    %% @pos sshd x=1552 y=192 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos nic x=1552 y=400 kind=interface
                    Container(nic, "nic0", "10.130.0.2", "Solo IP interna")
                    %% @pos bash_vm x=1864 y=192 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "sudo apt-get update")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea nat-config", "HTTPS")
    Rel(consola, api_compute, "Crea el router y su NAT", "JSON/HTTPS")
    Rel(api_compute, nat, "Crea la puerta de enlace de NAT")
    Rel(navegador, terminal, "Abre la terminal", "WebSocket/HTTPS")
    Rel(terminal, gcloud, "Ejecuta")
    Rel(terminal, debian, "apt-get update", "HTTPS :443")
    Rel(gcloud, iap, "Abre el túnel SSH", "WebSocket/HTTPS")
    Rel(iap, sshd, "Reenvía la conexión", "TCP :22")
    Rel(sshd, bash_vm, "Abre la terminal")
    %% @door vm | nic0 · 10.130.0.2\n→ packages.cloud.google.com:443 (TCP)
    %% @door subred | Acceso privado a Google: activo\nllega sin IP externa\n→ packages.cloud.google.com:443 (TCP)
    %% @door privatenet | Ruta 0.0.0.0/0 hacia las IP de Google:\nno sale a Internet
    %% @door gpkgs | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de packages.cloud.google.com
    Rel(bash_vm, gpkgs, "apt-get update", "HTTPS :443")
    %% @door vm | nic0 · 10.130.0.2\n→ Internet:443 (TCP)
    %% @door subred | Sin IP externa: la ruta 0.0.0.0/0\nlo lleva a nat-config (Cloud NAT)
    %% @door nat | Traduce 10.130.0.2 y su puerto\na una IP de NAT y un puerto suyo;\nla respuesta vuelve por aquí
    Rel(bash_vm, nat, "Sale a Internet por NAT", "HTTPS")
    %% @door privatenet | Ruta 0.0.0.0/0\n→ puerta de enlace de Internet\ncon la IP de NAT de nat-config
    %% @door debian | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de deb.debian.org
    Rel(nat, debian, "Lo reenvía con su IP de NAT", "HTTPS :443")

    %% @step estudiante navegador | En Cloud Shell: sudo apt-get update
    %% @step navegador terminal | sudo apt-get update
    %% @step terminal debian | Responde | GET /debian/dists/bookworm/InRelease HTTP/1.1\nHost: deb.debian.org\n\nHit:1 https://deb.debian.org/debian bookworm InRelease
    %% @step terminal gcloud | Entra a vm-internal | gcloud compute ssh vm-internal --zone us-central1-c --tunnel-through-iap
    %% @step gcloud iap | Abre el túnel
    %% @step iap sshd | privatenet-allow-ssh deja pasar el puerto 22
    %% @step sshd bash_vm | estudiante@vm-internal
    %% @step bash_vm gpkgs | Responde: Acceso privado a Google | GET /apt/dists/cloud-sdk-bookworm/InRelease HTTP/1.1\nHost: packages.cloud.google.com\n\nHit:1 https://packages.cloud.google.com/apt cloud-sdk-bookworm InRelease
    %% @step bash_vm bash_vm | Debian no responde (Ctrl+C) | 0% [Connecting to deb.debian.org (151.101.2.132)]\n\nSin IP externa ni NAT, la VM no sale a Internet
    %% @step estudiante navegador | Servicios de red > Cloud NAT > Comenzar
    %% @step navegador consola | nat-config, privatenet, us-central1; router nuevo nat-router
    %% @step consola api_compute | Crea nat-router con nat-config | POST /compute/v1/projects/PROYECTO/regions/us-central1/routers HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "nat-router", "network": "…/global/networks/privatenet",\n "nats": [{"name": "nat-config", "natIpAllocateOption": "AUTO_ONLY",\n  "sourceSubnetworkIpRangesToNat": "ALL_SUBNETWORKS_ALL_IP_RANGES"}]}
    %% @step api_compute nat | Estado: En ejecución
    %% @step bash_vm nat | Vuelve a ejecutar sudo apt-get update
    %% @step nat debian | Lo reenvía con una IP de NAT | GET /debian/dists/bookworm/InRelease HTTP/1.1\nHost: deb.debian.org
    %% @step debian nat | Hit: bookworm InRelease
    %% @step nat bash_vm | Devuelve la respuesta a 10.130.0.2
    %% @step bash_vm bash_vm | Reading package lists... Done; exit
