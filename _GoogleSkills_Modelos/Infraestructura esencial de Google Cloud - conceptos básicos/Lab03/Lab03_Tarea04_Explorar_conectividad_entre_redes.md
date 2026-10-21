C4Deployment
    title Lab03 - Tarea 4 - Explora la conectividad entre redes

    %% @pos estudiante x=-76 y=260 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Hace ping desde mynet-us-vm a las otras tres VMs")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra Cloud Shell")
    }

    %% @pos cloudshell x=666 y=200 w=248 h=384 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian") {
        %% @pos terminal x=690 y=256 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Escribe gcloud compute ssh")
        %% @pos gcloud x=690 y=440 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Abre el túnel SSH por IAP")
    }

    %% @pos iap x=1116 y=436 kind=external
    System_Ext(iap, "IAP", "Lleva SSH a mynet-us-vm desde 35.235.240.0/20")

    %% @pos proyecto x=1400 y=-200 w=1280 h=1204 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos mynetwork x=1424 y=-144 w=1186 h=452 kind=cloud
        Deployment_Node(mynetwork, "mynetwork", "Google Cloud VPC", "Las dos VMs se ven por IP interna") {
            %% @pos vm_us x=1448 y=-88 w=560 h=200 kind=appserver
            Deployment_Node(vm_us, "mynet-us-vm", "Compute Engine · Debian 12", "us-central1-c · 10.128.0.2") {
                %% @pos sshd x=1472 y=-32 kind=generic
                Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                %% @pos bash_us x=1784 y=-32 kind=terminal
                Container(bash_us, "Terminal de la VM", "Bash", "ping -c 3 a cada IP externa e interna")
            }
            %% @pos vm_eu x=2342 y=-88 w=244 h=372 kind=appserver
            Deployment_Node(vm_eu, "mynet-notus-vm", "Compute Engine · Debian 12", "europe-west1-b") {
                %% @pos ip_eu x=2384 y=-32 kind=interface
                Container(ip_eu, "IP externa", "203.0.113.12", "Responde")
                %% @pos nic_eu x=2384 y=140 kind=interface
                Container(nic_eu, "nic0", "10.132.0.2", "Responde: misma red de VPC")
            }
        }
        %% @pos managementnet x=1432 y=492 w=524 h=280 kind=cloud
        Deployment_Node(managementnet, "managementnet", "Google Cloud VPC", "Otra red: aislada de mynetwork") {
            %% @pos vm_mgmt x=1456 y=548 w=476 h=200 kind=appserver
            Deployment_Node(vm_mgmt, "managementnet-us-vm", "Compute Engine · Debian 12", "us-central1-c, la misma zona") {
                %% @pos ip_mgmt x=1480 y=604 kind=interface
                Container(ip_mgmt, "IP externa", "203.0.113.13", "Responde")
                %% @pos nic_mgmt x=1760 y=604 kind=interface
                Container(nic_mgmt, "nic0", "10.240.0.2", "No responde: otra red de VPC")
            }
        }
        %% @pos privatenet x=2132 y=472 w=524 h=280 kind=cloud
        Deployment_Node(privatenet, "privatenet", "Google Cloud VPC", "Otra red: aislada de mynetwork") {
            %% @pos vm_priv x=2156 y=528 w=476 h=200 kind=appserver
            Deployment_Node(vm_priv, "privatenet-us-vm", "Compute Engine · Debian 12", "us-central1-c, la misma zona") {
                %% @pos ip_priv x=2180 y=584 kind=interface
                Container(ip_priv, "IP externa", "203.0.113.14", "Responde")
                %% @pos nic_priv x=2460 y=584 kind=interface
                Container(nic_priv, "nic0", "172.16.0.2", "No responde: otra red de VPC")
            }
        }
        %% @pos reglas x=1464 y=844 kind=firewall
        %% @part reglas | mynetwork-allow-icmp | icmp desde 0.0.0.0/0
        %% @part reglas | managementnet-allow-icmp-ssh-rdp | icmp, tcp:22 y tcp:3389 desde 0.0.0.0/0
        %% @part reglas | privatenet-allow-icmp-ssh-rdp | icmp, tcp:22 y tcp:3389 desde 0.0.0.0/0
        Container(reglas, "Reglas que permiten ICMP", "Reglas de Cloud Firewall", "Una en cada red, desde 0.0.0.0/0: por eso responden todas las IP externas")
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, terminal, "Abre la terminal", "WebSocket/HTTPS")
    Rel(terminal, gcloud, "Ejecuta gcloud compute ssh")
    Rel(gcloud, iap, "Abre el túnel SSH", "WebSocket/HTTPS")
    Rel(iap, sshd, "Reenvía la conexión", "TCP :22")
    Rel(sshd, bash_us, "Abre la terminal")
    %% @door vm_eu | IP externa · 203.0.113.12\nmynetwork-allow-icmp:\npermite ICMP desde 0.0.0.0/0
    Rel(bash_us, ip_eu, "Hace ping", "ICMP")
    %% @door managementnet | Entra a la VPC\nmanagementnet-allow-icmp-ssh-rdp:\npermite ICMP desde 0.0.0.0/0
    Rel(bash_us, ip_mgmt, "Hace ping", "ICMP")
    %% @door privatenet | Entra a la VPC\nprivatenet-allow-icmp-ssh-rdp:\npermite ICMP desde 0.0.0.0/0
    Rel(bash_us, ip_priv, "Hace ping", "ICMP")
    Rel(bash_us, nic_eu, "Hace ping", "ICMP")
    %% @door managementnet | Otra red de VPC: aislada\nsin peering ni VPN no hay ruta\na sus IP internas
    Rel(bash_us, nic_mgmt, "No responde: otra red de VPC", "ICMP")
    %% @door privatenet | Otra red de VPC: aislada\nsin peering ni VPN no hay ruta\na sus IP internas
    Rel(bash_us, nic_priv, "No responde: otra red de VPC", "ICMP")

    %% @step estudiante navegador | Anota las IP de las tres VMs y abre Cloud Shell
    %% @step navegador terminal | Abre la terminal
    %% @step terminal gcloud | gcloud compute ssh mynet-us-vm --zone=us-central1-c --tunnel-through-iap
    %% @step gcloud iap | Abre el túnel | GET /v4/connect?project=PROYECTO&zone=us-central1-c&instance=mynet-us-vm&port=22 HTTP/1.1\nHost: tunnel.cloudproxy.app\nUpgrade: websocket
    %% @step iap sshd | Entra desde 35.235.240.0/20 por el puerto 22
    %% @step sshd bash_us | Abre la terminal de mynet-us-vm
    %% @step bash_us ip_eu | ping -c 3 203.0.113.12 (IP externa)
    %% @step ip_eu bash_us | Responde: mynetwork-allow-icmp permite ICMP desde 0.0.0.0/0
    %% @step bash_us ip_mgmt | ping -c 3 203.0.113.13
    %% @step ip_mgmt bash_us | Responde: managementnet-allow-icmp-ssh-rdp
    %% @step bash_us ip_priv | ping -c 3 203.0.113.14
    %% @step ip_priv bash_us | Responde: privatenet-allow-icmp-ssh-rdp
    %% @step bash_us nic_eu | ping -c 3 10.132.0.2 (IP interna)
    %% @step nic_eu bash_us | Responde: misma red de VPC, aunque esté en europe-west1
    %% @step bash_us nic_mgmt | ping -c 3 10.240.0.2
    %% @step bash_us bash_us | 100% packet loss: managementnet es otra red, aunque comparta zona
    %% @step bash_us nic_priv | ping -c 3 172.16.0.2
    %% @step bash_us bash_us | 100% packet loss: sin peering ni VPN, las IP internas no cruzan entre redes de VPC
    %% @step bash_us bash_us | Por IP interna solo se llega dentro de la misma red de VPC
