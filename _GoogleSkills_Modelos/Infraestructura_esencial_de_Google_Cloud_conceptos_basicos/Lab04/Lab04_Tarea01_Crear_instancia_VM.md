```
C4Deployment
    title Lab04 - Tarea 1 - Crea la instancia de VM

    %% @pos estudiante x=-100 y=248 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Crea privatenet y una VM sin IP externa, y entra por IAP")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y Cloud Shell")
    }

    %% @pos consola x=608 y=-156 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Crea privatenet, su regla y vm-internal")

    %% @pos cloudshell x=676 y=260 w=248 h=404 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian") {
        %% @pos terminal x=700 y=316 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Escribe gcloud compute ssh")
        %% @pos gcloud x=700 y=520 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Abre el túnel SSH por IAP")
    }

    %% @pos iap x=1108 y=740 kind=external
    System_Ext(iap, "IAP", "Lleva SSH a vm-internal desde 35.235.240.0/20, sin IP externa")

    %% @pos internet x=2360 y=344 kind=external
    System_Ext(internet, "www.google.com", "Un sitio en Internet")

    %% @pos proyecto x=1088 y=-268 w=1020 h=824 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1112 y=-148 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea la red, la subred, la regla y la VM")
        %% @pos privatenet x=1480 y=-212 w=604 h=744 kind=cloud
        %% @part privatenet | Modo de subredes | Personalizado: solo la subred que se define
        Deployment_Node(privatenet, "privatenet", "Google Cloud VPC", "Red de modo personalizado") {
            %% @pos regla_ssh x=1560 y=-156 kind=firewall
            Container(regla_ssh, "privatenet-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 35.235.240.0/20 (IAP) a todas las instancias")
            %% @pos subred x=1504 y=20 w=556 h=488 kind=generic
            %% @part subred | Acceso privado a Google | Desactivado: así se crea
            Deployment_Node(subred, "Subred privatenet-us", "VPC de Google Cloud · 10.130.0.0/20", "us-central1") {
                %% @pos vm x=1528 y=76 w=508 h=408 kind=appserver
                %% @part vm | IP externa | Ninguna: elegida en Redes > Interfaz de red
                Deployment_Node(vm, "vm-internal", "Compute Engine · Debian 12", "us-central1-c · e2-standard-2") {
                    %% @pos sshd x=1552 y=132 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos nic x=1864 y=132 kind=interface
                    Container(nic, "nic0", "10.130.0.2", "Solo IP interna")
                    %% @pos bash_vm x=1552 y=340 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "estudiante@vm-internal: ping a www.google.com")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea la red, la regla y la VM", "HTTPS")
    Rel(navegador, terminal, "Abre la terminal", "WebSocket/HTTPS")
    Rel(terminal, gcloud, "Ejecuta")
    Rel(consola, api_compute, "Crea la red, la regla y la VM", "JSON/HTTPS")
    Rel(api_compute, regla_ssh, "Crea las reglas de firewall")
    Rel(gcloud, iap, "Abre el túnel SSH", "WebSocket/HTTPS")
    %% @door privatenet | Entra a la VPC\nprivatenet-allow-ssh:\npermite 22/TCP desde 35.235.240.0/20 (IAP)
    %% @door subred | Ruta de la subred 10.130.0.0/20\n→ 10.130.0.2:22 (TCP)
    %% @door vm | nic0 · 10.130.0.2\nprivatenet-allow-ssh:\npermite 22/TCP desde 35.235.240.0/20 (IAP)
    %% @door sshd | Escucha en el puerto 22 (SSH)
    Rel(iap, sshd, "Reenvía la conexión", "TCP :22")
    Rel(sshd, bash_vm, "Abre la terminal")
    %% @door privatenet | Sin IP externa ni Cloud NAT:\nno hay salida a Internet
    %% @door internet | No hay respuesta:\n100% packet loss
    Rel(bash_vm, internet, "No responde: sin IP externa", "ICMP")

    %% @step estudiante navegador | Red de VPC > Crear red de VPC: privatenet, modo Personalizado
    %% @step navegador consola | Subred privatenet-us: 10.130.0.0/20, sin Acceso privado a Google
    %% @step consola api_compute | Crea privatenet | POST /compute/v1/projects/PROYECTO/global/networks HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "privatenet", "autoCreateSubnetworks": false}
    %% @step api_compute api_compute | Crea privatenet-us | POST /compute/v1/projects/PROYECTO/regions/us-central1/subnetworks HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "privatenet-us", "network": "…/global/networks/privatenet",\n "ipCidrRange": "10.130.0.0/20", "privateIpGoogleAccess": false}
    %% @step navegador consola | Crear regla de firewall: privatenet-allow-ssh
    %% @step consola api_compute | Crea la regla | POST /compute/v1/projects/PROYECTO/global/firewalls HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "privatenet-allow-ssh", "network": "…/global/networks/privatenet",\n "direction": "INGRESS", "sourceRanges": ["35.235.240.0/20"],\n "allowed": [{"IPProtocol": "tcp", "ports": ["22"]}]}
    %% @step api_compute regla_ssh | Solo tcp:22 desde 35.235.240.0/20: el rango de IAP
    %% @step navegador consola | Crear instancia vm-internal, IP externa: Ninguna
    %% @step consola api_compute | Crea vm-internal | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "vm-internal", "machineType": "zones/us-central1-c/machineTypes/e2-standard-2",\n "networkInterfaces": [{"subnetwork": "…/subnetworks/privatenet-us"}]}\n\nSin accessConfigs: no tiene IP externa
    %% @step api_compute consola | IP interna 10.130.0.2, IP externa: Ninguna
    %% @step navegador terminal | Activa Cloud Shell
    %% @step terminal gcloud | gcloud compute ssh vm-internal --zone us-central1-c --tunnel-through-iap
    %% @step gcloud iap | Abre el túnel | GET /v4/connect?project=PROYECTO&zone=us-central1-c&instance=vm-internal&interface=nic0&port=22 HTTP/1.1\nHost: tunnel.cloudproxy.app\nUpgrade: websocket
    %% @step iap sshd | Entra desde 35.235.240.0/20: privatenet-allow-ssh deja pasar el puerto 22
    %% @step sshd bash_vm | El prompt cambia a estudiante@vm-internal
    %% @step bash_vm internet | ping -c 2 www.google.com
    %% @step bash_vm bash_vm | 100% packet loss: sin salida a Internet
```