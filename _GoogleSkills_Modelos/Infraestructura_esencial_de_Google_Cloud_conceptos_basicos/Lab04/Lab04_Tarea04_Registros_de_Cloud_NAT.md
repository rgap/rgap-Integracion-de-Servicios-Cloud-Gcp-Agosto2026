```
C4Deployment
    title Lab04 - Tarea 4 - Configura y visualiza los registros de Cloud NAT

    %% @pos estudiante x=-124 y=256 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Activa el registro de nat-config y mira sus entradas")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y Cloud Shell")
    }

    %% @pos consola x=700 y=-160 kind=webapp url=console.cloud.google.com
    %% @part consola | Explorador de registros | resource.type="nat_gateway"
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Edita nat-config y abre el Explorador de registros")

    %% @pos cloudshell x=676 y=260 w=248 h=404 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian") {
        %% @pos terminal x=700 y=316 kind=terminal
        Container(terminal, "Terminal web", "Bash", "Escribe gcloud compute ssh")
        %% @pos gcloud x=700 y=520 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Abre el túnel SSH por IAP")
    }

    %% @pos iap x=704 y=788 kind=external
    System_Ext(iap, "IAP", "Lleva SSH a vm-internal desde 35.235.240.0/20")

    %% @pos debian x=1300 y=-640 kind=external url=https://deb.debian.org/debian
    System_Ext(debian, "deb.debian.org", "Repositorio de Debian, en Internet: 151.101.2.132")

    %% @pos proyecto x=1100 y=-240 w=1360 h=976 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1124 y=-160 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Guarda la configuración de registro de nat-config")
        %% @pos logging x=1124 y=200 kind=external url=https://logging.googleapis.com
        %% @part logging | Registro de NAT | compute.googleapis.com/nat_flows
        %% @part logging | Recurso | nat_gateway: nat-config, us-central1
        System_Ext(logging, "Cloud Logging", "Guarda cada traducción de Cloud NAT, que se ve en el Explorador de registros")
        %% @pos privatenet x=1496 y=-184 w=940 h=896 kind=cloud
        Deployment_Node(privatenet, "privatenet", "Google Cloud VPC", "Red de modo personalizado") {
            %% @pos regla_ssh x=1520 y=264 kind=firewall
            Container(regla_ssh, "privatenet-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 35.235.240.0/20 (IAP) a todas las instancias")
            %% @pos router x=1828 y=-128 w=240 h=200 kind=generic
            Deployment_Node(router, "nat-router", "Cloud Router · us-central1") {
                %% @pos nat x=1852 y=-72 kind=generic
                %% @part nat | Registro | Traducción y errores: en Configuración avanzada > Logging
                %% @part nat | IP de NAT | Automáticas: 34.123.45.67
                Container(nat, "nat-config", "Cloud NAT", "Deja salir a Internet a las VMs sin IP externa de privatenet")
            }
            %% @pos subred x=1804 y=200 w=608 h=488 kind=generic
            %% @part subred | Acceso privado a Google | Activo
            Deployment_Node(subred, "Subred privatenet-us", "VPC de Google Cloud · 10.130.0.0/20", "us-central1") {
                %% @pos vm x=1828 y=256 w=560 h=408 kind=appserver
                %% @part vm | IP externa | Ninguna
                Deployment_Node(vm, "vm-internal", "Compute Engine · Debian 12", "us-central1-c · e2-standard-2") {
                    %% @pos sshd x=1852 y=312 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos bash_vm x=2164 y=312 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "sudo apt-get update para generar tráfico")
                    %% @pos nic x=1852 y=520 kind=interface
                    Container(nic, "nic0", "10.130.0.2", "Solo IP interna")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Edita nat-config y mira los registros", "HTTPS")
    Rel(consola, api_compute, "Activa el registro", "JSON/HTTPS")
    Rel(api_compute, nat, "Registra traducción y errores")
    Rel(consola, logging, "Muestra los registros", "HTTPS")
    Rel(navegador, terminal, "Abre la terminal", "WebSocket/HTTPS")
    Rel(terminal, gcloud, "Ejecuta")
    Rel(gcloud, iap, "Abre el túnel SSH", "WebSocket/HTTPS")
    Rel(iap, sshd, "Reenvía la conexión", "TCP :22")
    Rel(sshd, bash_vm, "Abre la terminal")
    %% @rel label=-20,-24
    %% @door vm | nic0 · 10.130.0.2\n→ Internet:443 (TCP)
    %% @door subred | Sin IP externa: la ruta 0.0.0.0/0\nlo lleva a nat-config (Cloud NAT)
    %% @door nat | Traduce 10.130.0.2 y su puerto\na una IP de NAT y un puerto suyo;\nla respuesta vuelve por aquí
    Rel(bash_vm, nat, "Sale a Internet por NAT", "HTTPS")
    %% @door privatenet | Ruta 0.0.0.0/0\n→ puerta de enlace de Internet\ncon la IP de NAT de nat-config
    %% @door debian | Escucha en el puerto 443 (HTTPS)\nTLS: certificado de deb.debian.org
    Rel(nat, debian, "Lo reenvía con su IP de NAT", "HTTPS :443")
    Rel(nat, logging, "Registra cada traducción")

    %% @step estudiante navegador | Cloud NAT > nat-config > Editar
    %% @step navegador consola | Configuración avanzada > Logging: Traducción y errores
    %% @step consola api_compute | Activa el registro | PATCH /compute/v1/projects/PROYECTO/regions/us-central1/routers/nat-router HTTP/1.1\nHost: compute.googleapis.com\n\n{"nats": [{"name": "nat-config",\n  "logConfig": {"enable": true, "filter": "ALL"}}]}
    %% @step api_compute nat | Desde ahora registra cada traducción
    %% @step navegador consola | Ver en el Explorador de registros
    %% @step consola logging | Todavía no hay entradas | POST /v2/entries:list HTTP/1.1\nHost: logging.googleapis.com\n\n{"resourceNames": ["projects/PROYECTO"],\n "filter": "resource.type=\\"nat_gateway\\""}
    %% @step navegador terminal | Entra a vm-internal
    %% @step terminal gcloud | gcloud compute ssh | gcloud compute ssh vm-internal --zone us-central1-c --tunnel-through-iap
    %% @step gcloud iap | Abre el túnel
    %% @step iap sshd | privatenet-allow-ssh deja pasar el puerto 22
    %% @step sshd bash_vm | sudo apt-get update
    %% @step bash_vm nat | Sale por nat-config | 10.130.0.2:45678 → 151.101.2.132:443 (TCP)
    %% @step nat debian | Con la IP de NAT | 34.123.45.67:1024 → 151.101.2.132:443 (TCP)
    %% @step nat logging | Registra la traducción | logName: projects/PROYECTO/logs/compute.googleapis.com%2Fnat_flows\nresource.type: nat_gateway\n\njsonPayload:\n  allocation_status: OK\n  connection: {src_ip: 10.130.0.2, src_port: 45678,\n    dest_ip: 151.101.2.132, dest_port: 443, protocol: 6,\n    nat_ip: 34.123.45.67, nat_port: 1024}\n  endpoint: {vm_name: vm-internal, zone: us-central1-c}\n  vpc: {vpc_name: privatenet, subnetwork_name: privatenet-us}
    %% @step debian nat | Responde: Hit bookworm InRelease
    %% @step nat bash_vm | Devuelve la respuesta a 10.130.0.2
    %% @step estudiante navegador | Vuelve al Explorador de registros
    %% @step consola logging | Aparecen entradas de nat-config: la VPC, la VM y la conexión
```