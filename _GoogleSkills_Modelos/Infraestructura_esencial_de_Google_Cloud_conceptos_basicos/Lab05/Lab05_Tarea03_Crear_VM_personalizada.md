```
C4Deployment
    title Lab05 - Tarea 3 - Crea una máquina virtual personalizada

    %% @pos estudiante x=-52 y=240 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Crea utility-cm con 2 vCPU y 4 GB y lo comprueba por SSH")

    %% @pos equipo x=268 y=188 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=312 y=244 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y la ventana SSH")
    }

    %% @pos consola x=700 y=-40 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Crea utility-cm con tipo de máquina personalizado")

    %% @pos ssh_navegador x=700 y=440 kind=terminal url=https://ssh.cloud.google.com/v2/ssh/projects/PROYECTO/zones/us-central1-c/instances/utility-cm
    Container(ssh_navegador, "SSH en el navegador", "ssh.cloud.google.com", "La terminal de utility-cm en otra pestaña")

    %% @pos proyecto x=1100 y=-176 w=1148 h=836 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1124 y=-40 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea la VM y guarda la llave SSH temporal")
        %% @pos metadatos x=1128 y=220 kind=external
        %% @part metadatos | ssh-keys | estudiante:ssh-rsa AAAA… google-ssh {"expireOn": "…"}
        System_Ext(metadatos, "Servidor de metadatos", "Da a la VM las llaves SSH")
        %% @pos default x=1480 y=-120 w=744 h=756 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos regla_ssh x=1504 y=-64 kind=firewall
            Container(regla_ssh, "default-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 0.0.0.0/0: la trae la red default")
            %% @pos subred x=1504 y=116 w=696 h=496 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1528 y=172 w=648 h=416 kind=appserver
                %% @part vm | Tipo de máquina | Personalizado: e2-custom-2-4096, 2 vCPU y 4 GB
                %% @part vm | Imagen | Debian GNU/Linux 12 (bookworm)
                %% @part vm | Plataforma de CPU | Intel Broadwell
                Deployment_Node(vm, "utility-cm", "Compute Engine · Debian 12", "us-central1-c · e2-custom-2-4096") {
                    %% @pos ip_externa x=1796 y=232 kind=interface
                    Container(ip_externa, "IP externa", "203.0.113.22", "Efímera")
                    %% @pos sshd x=1552 y=440 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos agente x=1552 y=232 kind=generic
                    Container(agente, "Agente invitado", "google-guest-agent", "Instala la llave temporal en ~/.ssh/authorized_keys")
                    %% @pos nic x=2004 y=228 kind=interface
                    Container(nic, "nic0", "10.128.0.4", "La IP interna")
                    %% @pos bash_vm x=1936 y=444 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "free, dmidecode, nproc y lscpu")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea utility-cm", "HTTPS")
    Rel(consola, api_compute, "Crea la VM", "JSON/HTTPS")
    Rel(navegador, ssh_navegador, "Abre la ventana SSH", "WebSocket/HTTPS")
    Rel(ssh_navegador, api_compute, "Agrega una llave temporal", "JSON/HTTPS")
    Rel(api_compute, metadatos, "Guarda la llave en los metadatos")
    Rel(agente, metadatos, "Espera cambios en los metadatos", "HTTP")
    %% @door default | Entra a la VPC\ndefault-allow-ssh:\npermite 22/TCP desde 0.0.0.0/0 (Internet)
    %% @door subred | Ruta de la subred 10.128.0.0/20\n→ 203.0.113.22:22 (TCP)
    %% @door vm | IP externa · 203.0.113.22\ndefault-allow-ssh:\npermite 22/TCP desde 0.0.0.0/0 (Internet)
    %% @door sshd | Escucha en el puerto 22 (SSH)\nCon una llave temporal\nagregada a los metadatos
    Rel(ssh_navegador, sshd, "Abre una sesión", "SSH")
    Rel(sshd, bash_vm, "Abre la terminal")

    %% @step estudiante navegador | Crear instancia: utility-cm, us-central1-c, E2
    %% @step navegador consola | Personalizado: 2 núcleos y 4 GB; Debian 12; Crear
    %% @step consola api_compute | Crea utility-cm | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "utility-cm", "machineType": "zones/us-central1-c/machineTypes/e2-custom-2-4096",\n "disks": [{"boot": true, "initializeParams": {"sourceImage": "projects/debian-cloud/global/images/family/debian-12"}}],\n "networkInterfaces": [{"network": "global/networks/default",\n   "accessConfigs": [{"type": "ONE_TO_ONE_NAT"}]}]}
    %% @step api_compute consola | En ejecución
    %% @step estudiante navegador | SSH en la fila de utility-cm
    %% @step navegador ssh_navegador | Abre la ventana en otra pestaña
    %% @step ssh_navegador api_compute | Agrega una llave temporal | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances/utility-cm/setMetadata HTTP/1.1\nHost: compute.googleapis.com\n\n{"items": [{"key": "ssh-keys", "value":\n  "estudiante:ssh-rsa AAAA… google-ssh {\\"userName\\": \\"estudiante\\", \\"expireOn\\": \\"…\\"}"}]}
    %% @step api_compute metadatos | Guarda la llave
    %% @step agente metadatos | La instala en ~/.ssh/authorized_keys
    %% @step ssh_navegador sshd | Abre la sesión: default-allow-ssh deja pasar el 22
    %% @step sshd bash_vm | estudiante@utility-cm
    %% @step bash_vm bash_vm | free: 4 GB menos lo del sistema | $ free\n               total        used        free      shared  buff/cache   available\nMem:         4063446      278304     3461302         540      323840     4044214\nSwap:              0           0           0
    %% @step bash_vm bash_vm | sudo dmidecode -t 17: un módulo de 4 GB | Handle 0x1100, DMI type 17, 21 bytes\nMemory Device\n\\tTotal Width: 64 bits\n\\tSize: 4 GB\n\\tForm Factor: DIMM\n\\tLocator: DIMM 0\n\\tType: RAM
    %% @step bash_vm bash_vm | nproc: 2
    %% @step bash_vm bash_vm | lscpu: 1 núcleo con 2 hilos | Architecture:            x86_64\nCPU(s):                  2\nVendor ID:               GenuineIntel\n  Model name:            Intel(R) Xeon(R) CPU @ 2.20GHz\n    Thread(s) per core:  2\n    Core(s) per socket:  1\n    Socket(s):           1\nVirtualization features:\n  Hypervisor vendor:     KVM\n  Virtualization type:   full
    %% @step bash_vm bash_vm | exit
```