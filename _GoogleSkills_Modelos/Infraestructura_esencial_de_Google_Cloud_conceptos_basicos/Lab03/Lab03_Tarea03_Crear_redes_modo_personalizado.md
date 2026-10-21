```
C4Deployment
    title Lab03 - Tarea 3 - Crea redes de modo personalizado

    %% @pos estudiante x=-96 y=260 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Crea managementnet en la consola y privatenet con gcloud")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y Cloud Shell")
    }

    %% @pos consola x=700 y=0 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Formularios con su Línea de comandos equivalente")

    %% @pos cloudshell x=676 y=300 w=248 h=384 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian") {
        %% @pos terminal x=700 y=356 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Escribe los comandos de gcloud")
        %% @pos gcloud x=700 y=540 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Crea privatenet, sus subredes, su regla y su VM")
    }

    %% @pos proyecto x=1320 y=-292 w=1030 h=1256 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1344 y=280 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Recibe lo mismo desde la consola y desde gcloud")
        %% @pos managementnet x=1548 y=-236 w=624 h=360 kind=cloud
        %% @part managementnet | Modo de subredes | Personalizado: solo managementsubnet-us
        Deployment_Node(managementnet, "managementnet", "Google Cloud VPC", "Creada desde la consola") {
            %% @pos regla_mgmt x=1572 y=-180 kind=firewall
            Container(regla_mgmt, "managementnet-allow-icmp-ssh-rdp", "Regla de Cloud Firewall · entrada", "Permite icmp, tcp:22 y tcp:3389 desde 0.0.0.0/0 a todas las instancias")
            %% @pos subred_mgmt x=1856 y=-180 w=292 h=280 kind=generic
            Deployment_Node(subred_mgmt, "managementsubnet-us", "VPC de Google Cloud · 10.240.0.0/20", "us-central1") {
                %% @pos vm_mgmt x=1880 y=-124 w=244 h=200 kind=appserver
                Deployment_Node(vm_mgmt, "managementnet-us-vm", "Compute Engine · Debian 12", "us-central1-c · e2-micro") {
                    %% @pos nic_mgmt x=1908 y=-68 kind=interface
                    Container(nic_mgmt, "nic0", "10.240.0.2", "IP interna en managementsubnet-us")
                }
            }
        }
        %% @pos privatenet x=1452 y=580 w=874 h=360 kind=cloud
        %% @part privatenet | Modo de subredes | Personalizado: privatesubnet-us y privatesubnet-notus
        Deployment_Node(privatenet, "privatenet", "Google Cloud VPC", "Creada con gcloud") {
            %% @pos regla_priv x=1476 y=636 kind=firewall
            Container(regla_priv, "privatenet-allow-icmp-ssh-rdp", "Regla de Cloud Firewall · entrada", "Permite icmp, tcp:22 y tcp:3389 desde 0.0.0.0/0")
            %% @pos subred_priv_us x=1734 y=636 w=292 h=280 kind=generic
            Deployment_Node(subred_priv_us, "privatesubnet-us", "VPC de Google Cloud · 172.16.0.0/24", "us-central1") {
                %% @pos vm_priv x=1758 y=692 w=244 h=200 kind=appserver
                Deployment_Node(vm_priv, "privatenet-us-vm", "Compute Engine · Debian 12", "us-central1-c · e2-micro") {
                    %% @pos nic_priv x=1802 y=748 kind=interface
                    Container(nic_priv, "nic0", "172.16.0.2", "IP interna en privatesubnet-us")
                }
            }
            %% @pos subred_priv_eu x=2102 y=636 kind=generic
            Container(subred_priv_eu, "privatesubnet-notus", "VPC de Google Cloud · 172.20.0.0/20", "europe-west1, sin VMs")
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea managementnet, su regla y su VM", "HTTPS")
    Rel(navegador, terminal, "Abre la terminal", "WebSocket/HTTPS")
    Rel(terminal, gcloud, "Ejecuta")
    Rel(consola, api_compute, "Crea managementnet y managementnet-us-vm", "JSON/HTTPS")
    Rel(gcloud, api_compute, "Crea privatenet y privatenet-us-vm", "JSON/HTTPS")
    Rel(api_compute, regla_mgmt, "Crea la regla")
    Rel(api_compute, regla_priv, "Crea la regla")
    Rel(api_compute, nic_mgmt, "Crea la VM con su IP interna")
    Rel(api_compute, nic_priv, "Crea la VM con su IP interna")
    Rel(api_compute, subred_priv_eu, "Crea la subred")

    %% @step estudiante navegador | Crear red de VPC: managementnet, modo Personalizado
    %% @step navegador consola | Subred managementsubnet-us, 10.240.0.0/20
    %% @step consola api_compute | Crea la red y su subred | POST /compute/v1/projects/PROYECTO/global/networks HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "managementnet", "autoCreateSubnetworks": false}
    %% @step navegador terminal | Abre Cloud Shell
    %% @step terminal gcloud | networks create privatenet
    %% @step gcloud api_compute | Crea privatenet | POST /compute/v1/projects/PROYECTO/global/networks HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "privatenet", "autoCreateSubnetworks": false}
    %% @step terminal gcloud | networks subnets create (2)
    %% @step gcloud api_compute | Crea las dos subredes | POST /compute/v1/projects/PROYECTO/regions/us-central1/subnetworks HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "privatesubnet-us", "network": "…/privatenet", "ipCidrRange": "172.16.0.0/24"}
    %% @step api_compute subred_priv_eu | privatesubnet-notus en europe-west1; privatesubnet-us en us-central1
    %% @step navegador consola | Crear regla de firewall
    %% @step consola api_compute | Crea la regla
    %% @step api_compute regla_mgmt | icmp, tcp:22 y tcp:3389 desde 0.0.0.0/0
    %% @step terminal gcloud | firewall-rules create
    %% @step gcloud api_compute | Crea la regla de privatenet | POST /compute/v1/projects/PROYECTO/global/firewalls HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "privatenet-allow-icmp-ssh-rdp", "network": "…/privatenet",\n "allowed": [{"IPProtocol": "icmp"}, {"IPProtocol": "tcp", "ports": ["22", "3389"]}],\n "sourceRanges": ["0.0.0.0/0"]}
    %% @step api_compute regla_priv | La misma regla, en privatenet
    %% @step navegador consola | Crear instancia managementnet-us-vm
    %% @step consola api_compute | Crea la VM
    %% @step api_compute nic_mgmt | Le da 10.240.0.2 en managementsubnet-us
    %% @step terminal gcloud | instances create
    %% @step gcloud api_compute | Crea privatenet-us-vm | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "privatenet-us-vm", "machineType": "…/e2-micro",\n "networkInterfaces": [{"subnetwork": "…/privatesubnet-us"}]}
    %% @step api_compute nic_priv | Le da 172.16.0.2 en privatesubnet-us
    %% @step gcloud terminal | instances list: 4 VMs, 3 redes
```