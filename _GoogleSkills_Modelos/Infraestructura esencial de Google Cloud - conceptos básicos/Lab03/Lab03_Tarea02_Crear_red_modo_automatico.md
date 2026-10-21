C4Deployment
    title Lab03 - Tarea 2 - Crea una red de modo automático

    %% @pos estudiante x=-116 y=252 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Crea mynetwork y dos VMs, entra por SSH y hace ping")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y Cloud Shell")
    }

    %% @pos consola x=700 y=-160 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Crea mynetwork, sus reglas y las VMs")

    %% @pos cloudshell x=676 y=260 w=248 h=404 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian") {
        %% @pos terminal x=700 y=316 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Escribe los comandos de gcloud")
        %% @pos gcloud x=700 y=520 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Habilita las APIs y abre el túnel SSH")
    }

    %% @pos iap x=1100 y=760 kind=external
    System_Ext(iap, "IAP", "Lleva SSH a la VM desde 35.235.240.0/20")

    %% @pos proyecto x=1100 y=-272 w=1480 h=928 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_servicios x=1152 y=360 kind=api
        Container(api_servicios, "API de Service Usage", "REST · googleapis.com", "Habilita iap.googleapis.com y networkmanagement.googleapis.com")
        %% @pos api_compute x=1124 y=160 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea la red, las reglas y las VMs")
        %% @pos mynetwork x=1480 y=-216 w=1076 h=848 kind=cloud
        %% @part mynetwork | Modo de subredes | Automático al crearla; al final de la tarea se pasa a personalizado
        Deployment_Node(mynetwork, "mynetwork", "Google Cloud VPC", "Una subred por región, creada sola") {
            %% @pos regla_custom x=1504 y=-160 kind=firewall
            Container(regla_custom, "mynetwork-allow-custom", "Regla de Cloud Firewall · entrada", "Permite todo desde 10.128.0.0/9 (las subredes de la red)")
            %% @pos regla_icmp x=1780 y=-160 kind=firewall
            Container(regla_icmp, "mynetwork-allow-icmp", "Regla de Cloud Firewall · entrada", "Permite icmp desde 0.0.0.0/0")
            %% @pos regla_iap x=2056 y=-160 kind=firewall
            Container(regla_iap, "allow-iap-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 35.235.240.0/20 a la etiqueta iap-gce")
            %% @pos reglas x=2332 y=-160 kind=firewall
            %% @part reglas | mynetwork-allow-rdp | tcp:3389 desde 0.0.0.0/0
            %% @part reglas | mynetwork-allow-ssh | tcp:22 desde 0.0.0.0/0
            Container(reglas, "Otras reglas", "Reglas de Cloud Firewall", "allow-rdp y allow-ssh, marcadas al crear la red")
            %% @pos subred_us x=1504 y=120 w=296 h=488 kind=generic
            Deployment_Node(subred_us, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20") {
                %% @pos vm_us x=1528 y=176 w=248 h=408 kind=appserver
                %% @part vm_us | Etiqueta de red | iap-gce: la elige allow-iap-ssh
                Deployment_Node(vm_us, "mynet-us-vm", "Compute Engine · Debian 12", "us-central1-c · e2-medium") {
                    %% @pos sshd x=1552 y=232 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos bash_us x=1552 y=440 kind=terminal
                    Container(bash_us, "Terminal de la VM", "Bash", "ping a la IP interna y a la externa de mynet-notus-vm")
                }
            }
            %% @pos subred_eu x=2122 y=120 w=292 h=488 kind=generic
            Deployment_Node(subred_eu, "Subred europe-west1", "VPC de Google Cloud · 10.132.0.0/20") {
                %% @pos vm_eu x=2146 y=176 w=244 h=408 kind=appserver
                Deployment_Node(vm_eu, "mynet-notus-vm", "Compute Engine · Debian 12", "europe-west1-b · e2-medium") {
                    %% @pos ip_eu x=2188 y=232 kind=interface
                    Container(ip_eu, "IP externa", "203.0.113.12", "Efímera")
                    %% @pos nic_eu x=2188 y=440 kind=interface
                    Container(nic_eu, "nic0", "10.132.0.2", "La IP interna, en europe-west1")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea mynetwork, la regla y las VMs", "HTTPS")
    Rel(navegador, terminal, "Abre la terminal", "WebSocket/HTTPS")
    Rel(terminal, gcloud, "Ejecuta")
    Rel(gcloud, api_servicios, "gcloud services enable", "JSON/HTTPS")
    Rel(consola, api_compute, "Crea la red, las reglas y las VMs", "JSON/HTTPS")
    Rel(api_compute, regla_iap, "Crea las reglas de firewall")
    Rel(gcloud, iap, "Abre el túnel SSH", "WebSocket/HTTPS")
    %% @door mynetwork | Entra a la VPC\nallow-iap-ssh:\npermite 22/TCP desde 35.235.240.0/20 (IAP)
    Rel(iap, sshd, "Reenvía la conexión", "TCP :22")
    Rel(sshd, bash_us, "Abre la terminal")
    %% @door vm_eu | nic0 · 10.132.0.2\nmynetwork-allow-custom:\npermite ICMP desde 10.128.0.0/9
    Rel(bash_us, nic_eu, "Hace ping", "ICMP")
    %% @door vm_eu | IP externa · 203.0.113.12\nmynetwork-allow-icmp:\npermite ICMP desde 0.0.0.0/0
    Rel(bash_us, ip_eu, "Hace ping", "ICMP")
    Rel(ip_eu, nic_eu, "Traduce a la IP interna", "NAT 1:1")

    %% @step estudiante navegador | Abre Cloud Shell
    %% @step navegador terminal | Abre la terminal
    %% @step terminal gcloud | gcloud services enable iap.googleapis.com networkmanagement.googleapis.com
    %% @step gcloud api_servicios | Habilita IAP y Network Management | POST /v1/projects/PROYECTO/services:batchEnable HTTP/1.1\nHost: serviceusage.googleapis.com\n\n{"serviceIds": ["iap.googleapis.com", "networkmanagement.googleapis.com"]}
    %% @step estudiante navegador | Crear red de VPC: mynetwork, modo Automático, todas las reglas
    %% @step navegador consola | Envía el formulario
    %% @step consola api_compute | Crea mynetwork en modo automático | POST /compute/v1/projects/PROYECTO/global/networks HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "mynetwork", "autoCreateSubnetworks": true}
    %% @step api_compute api_compute | Crea una subred por región: 10.128.0.0/20 en us-central1, 10.132.0.0/20 en europe-west1…
    %% @step api_compute regla_iap | Crea allow-custom, -icmp, -rdp, -ssh y luego allow-iap-ssh
    %% @step consola api_compute | Crea mynet-us-vm (etiqueta iap-gce) y mynet-notus-vm
    %% @step terminal gcloud | gcloud compute ssh mynet-us-vm --zone=us-central1-c --tunnel-through-iap
    %% @step gcloud iap | Abre el túnel | GET /v4/connect?project=PROYECTO&zone=us-central1-c&instance=mynet-us-vm&port=22 HTTP/1.1\nHost: tunnel.cloudproxy.app\nUpgrade: websocket
    %% @step iap sshd | Entra desde 35.235.240.0/20: allow-iap-ssh deja pasar el puerto 22
    %% @step sshd bash_us | La llave es válida: abre la terminal de la VM
    %% @step bash_us nic_eu | ping -c 3 10.132.0.2: misma red, aunque en otra región
    %% @step nic_eu bash_us | 3 respuestas: allow-custom permite 10.128.0.0/9
    %% @step bash_us ip_eu | ping -c 3 203.0.113.12: sale a internet y vuelve a entrar
    %% @step ip_eu nic_eu | Google la traduce a 10.132.0.2
    %% @step nic_eu ip_eu | Responde: allow-icmp permite ICMP desde 0.0.0.0/0
    %% @step ip_eu bash_us | 3 respuestas, con más demora que por la IP interna
    %% @step estudiante navegador | Editar mynetwork: modo de subredes Personalizado
    %% @step consola api_compute | Pasa mynetwork a modo personalizado | POST /compute/v1/projects/PROYECTO/global/networks/mynetwork/switchToCustomMode HTTP/1.1\nHost: compute.googleapis.com
    %% @step api_compute consola | Modo: Personalizado; ya no se agregan subredes solas
