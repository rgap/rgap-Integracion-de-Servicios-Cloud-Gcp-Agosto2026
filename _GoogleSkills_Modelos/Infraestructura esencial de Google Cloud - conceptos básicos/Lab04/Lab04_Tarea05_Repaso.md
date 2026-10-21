C4Deployment
    title Lab04 - Tarea 5 - Repaso

    %% @pos estudiante x=-128 y=260 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Repasa cómo entra y sale una VM sin IP externa")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y Cloud Shell")
    }

    %% @pos consola x=700 y=-160 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Explorador de registros")

    %% @pos cloudshell x=676 y=260 w=248 h=404 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian") {
        %% @pos terminal x=700 y=316 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Escribe gcloud compute ssh")
        %% @pos gcloud x=700 y=520 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Abre el túnel SSH por IAP")
    }

    %% @pos iap x=872 y=772 kind=external
    System_Ext(iap, "IAP", "Entrada: SSH desde 35.235.240.0/20, sin IP externa")

    %% @pos debian x=1756 y=-592 kind=external url=https://deb.debian.org/debian
    System_Ext(debian, "deb.debian.org", "Internet: llega solo por Cloud NAT")

    %% @pos gpkgs x=2560 y=348 kind=external url=https://packages.cloud.google.com/apt
    System_Ext(gpkgs, "packages.cloud.google.com", "Servicio de Google: llega con Acceso privado a Google")

    %% @pos proyecto x=1136 y=-272 w=1332 h=1320 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos bucket x=2044 y=904 kind=storage url=https://storage.googleapis.com/qwiklabs-gcp-04-8f2c1d
        %% @file bucket | access.svg | | 9 kB
        ContainerDb(bucket, "qwiklabs-gcp-04-8f2c1d", "Cloud Storage · multirregión US", "Llega con Acceso privado a Google")
        %% @pos logging x=1160 y=164 kind=external url=https://logging.googleapis.com
        System_Ext(logging, "Cloud Logging", "Guarda cada traducción de Cloud NAT, que se ve en el Explorador de registros")
        %% @pos privatenet x=1480 y=-216 w=964 h=964 kind=cloud
        Deployment_Node(privatenet, "privatenet", "Google Cloud VPC", "Red de modo personalizado") {
            %% @pos regla_ssh x=1504 y=-160 kind=firewall
            Container(regla_ssh, "privatenet-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 35.235.240.0/20 (IAP) a todas las instancias")
            %% @pos router x=2180 y=-160 w=240 h=200 kind=generic
            Deployment_Node(router, "nat-router", "Cloud Router · us-central1") {
                %% @pos nat x=2204 y=-104 kind=generic
                %% @part nat | Registro | Traducción y errores
                %% @part nat | Solo salida | Nadie de Internet puede abrir una conexión hacia la VM
                Container(nat, "nat-config", "Cloud NAT", "Deja salir a Internet a las VMs sin IP externa de privatenet")
            }
            %% @pos subred x=1612 y=236 w=608 h=488 kind=generic
            %% @part subred | Acceso privado a Google | Activo
            Deployment_Node(subred, "Subred privatenet-us", "VPC de Google Cloud · 10.130.0.0/20", "us-central1") {
                %% @pos vm x=1636 y=292 w=560 h=408 kind=appserver
                %% @part vm | IP externa | Ninguna
                Deployment_Node(vm, "vm-internal", "Compute Engine · Debian 12", "us-central1-c · e2-standard-2") {
                    %% @pos sshd x=1660 y=348 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos bash_vm x=1972 y=348 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "apt-get update y gcloud storage cp")
                    %% @pos nic x=1660 y=556 kind=interface
                    Container(nic, "nic0", "10.130.0.2", "Solo IP interna")
                    %% @pos gcloud_vm x=1972 y=556 kind=terminal
                    Container(gcloud_vm, "gcloud de la VM", "Google Cloud CLI", "gcloud storage cp desde el bucket")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Mira los registros", "HTTPS")
    Rel(consola, logging, "Muestra los registros", "HTTPS")
    Rel(navegador, terminal, "Abre la terminal", "WebSocket/HTTPS")
    Rel(terminal, gcloud, "Ejecuta")
    Rel(gcloud, iap, "Abre el túnel SSH", "WebSocket/HTTPS")
    %% @door privatenet | Entra a la VPC\nprivatenet-allow-ssh:\npermite 22/TCP desde 35.235.240.0/20 (IAP)
    %% @door subred | Ruta de la subred 10.130.0.0/20\n→ 10.130.0.2:22 (TCP)
    %% @door vm | nic0 · 10.130.0.2\nprivatenet-allow-ssh:\npermite 22/TCP desde 35.235.240.0/20 (IAP)
    %% @door sshd | Escucha en el puerto 22 (SSH)
    Rel(iap, sshd, "Reenvía la conexión", "TCP :22")
    Rel(sshd, bash_vm, "Abre la terminal")
    Rel(bash_vm, gcloud_vm, "Ejecuta")
    %% @door vm | nic0 · 10.130.0.2\n→ storage.googleapis.com:443 (TCP)
    %% @door subred | Acceso privado a Google: activo\nllega sin IP externa\n→ storage.googleapis.com:443 (TCP)
    %% @door privatenet | Ruta 0.0.0.0/0 hacia las IP de Google:\nno sale a Internet
    %% @door bucket | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de storage.googleapis.com\nCon el token OAuth de la cuenta\n(Authorization: Bearer)
    Rel(gcloud_vm, bucket, "Copia access.svg", "JSON/HTTPS")
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
    Rel(nat, logging, "Registra cada traducción")

    %% @step estudiante navegador | vm-internal no tiene IP externa: tres caminos
    %% @step navegador terminal | Abre Cloud Shell
    %% @step terminal gcloud | gcloud compute ssh --tunnel-through-iap
    %% @step gcloud iap | 1. Entrada: SSH por IAP
    %% @step iap sshd | privatenet-allow-ssh admite solo 35.235.240.0/20
    %% @step sshd bash_vm | estudiante@vm-internal
    %% @step bash_vm gcloud_vm | gcloud storage cp gs://$MY_BUCKET/*.svg .
    %% @step gcloud_vm bucket | 2. APIs de Google: Acceso privado a Google
    %% @step bash_vm gpkgs | El repositorio de Google también, sin NAT
    %% @step bash_vm nat | 3. El resto de Internet: por Cloud NAT
    %% @step nat debian | Solo conexiones que abre la VM
    %% @step nat logging | Cada traducción queda registrada
    %% @step consola logging | Se ven en el Explorador de registros
