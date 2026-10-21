```
C4Deployment
    title Lab05 - Tarea 1 - Crea una máquina virtual de utilidad

    %% @pos estudiante x=-120 y=252 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Crea utility-vm sin IP externa y revisa sus detalles y registros")

    %% @pos equipo x=192 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=236 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola")
    }

    %% @pos consola x=700 y=256 kind=webapp url=console.cloud.google.com
    %% @part consola | Estimación de costos | Mensual, a la derecha del formulario: sube con e2-standard-4 y baja con e2-medium
    %% @part consola | Detalles de la VM | Plataforma de CPU, políticas de disponibilidad y la sección Registros
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Crea utility-vm y muestra sus detalles")

    %% @pos proyecto x=1100 y=-40 w=964 h=704 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1124 y=256 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea la VM y su disco")
        %% @pos logging x=1124 y=520 kind=external url=https://logging.googleapis.com
        %% @part logging | Registro de auditoría | cloudaudit.googleapis.com/activity: quién creó la VM y cuándo
        System_Ext(logging, "Cloud Logging", "Guarda el registro de auditoría de cada VM que se crea o cambia")
        %% @pos default x=1480 y=16 w=560 h=360 kind=cloud
        Deployment_Node(default, "default", "Google Cloud VPC", "La red que trae el proyecto") {
            %% @pos subred x=1504 y=72 w=512 h=280 kind=generic
            Deployment_Node(subred, "Subred us-central1", "VPC de Google Cloud · 10.128.0.0/20", "Creada sola en modo automático") {
                %% @pos vm x=1528 y=128 w=464 h=200 kind=appserver
                %% @part vm | Tipo de máquina | e2-medium: 2 vCPU compartidas y 4 GB
                %% @part vm | Plataforma de CPU | Intel Broadwell; no se cambia con la VM en ejecución
                %% @part vm | Políticas de disponibilidad | Estándar (no Spot), migrar en el mantenimiento del host, reinicio automático
                %% @part vm | IP externa | Ninguna
                Deployment_Node(vm, "utility-vm", "Compute Engine · Debian 12", "us-central1-c · e2-medium") {
                    %% @pos nic x=1820 y=184 kind=interface
                    Container(nic, "nic0", "10.128.0.2", "Solo IP interna")
                    %% @pos disco x=1552 y=184 kind=storage
                    ContainerDb(disco, "Disco de arranque", "Persistent Disk (pd-balanced)", "10 GB con Debian 12")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea utility-vm y mira sus detalles", "HTTPS")
    Rel(consola, api_compute, "Crea la VM", "JSON/HTTPS")
    Rel(api_compute, disco, "Crea el disco")
    Rel(api_compute, logging, "Registra cada operación")
    Rel(consola, logging, "Muestra los registros", "HTTPS")

    %% @step estudiante navegador | Compute Engine > Instancias de VM > Crear instancia
    %% @step navegador consola | utility-vm, us-central1-c, serie E2
    %% @step consola consola | e2-standard-4 sube la estimación; e2-medium la baja
    %% @step navegador consola | Redes: IP externa Ninguna; Crear
    %% @step consola api_compute | Crea utility-vm | POST /compute/v1/projects/PROYECTO/zones/us-central1-c/instances HTTP/1.1\nHost: compute.googleapis.com\n\n{"name": "utility-vm", "machineType": "zones/us-central1-c/machineTypes/e2-medium",\n "networkInterfaces": [{"network": "global/networks/default"}],\n "disks": [{"boot": true, "initializeParams": {"sourceImage": "projects/debian-cloud/global/images/family/debian-12"}}],\n "scheduling": {"provisioningModel": "STANDARD", "onHostMaintenance": "MIGRATE", "automaticRestart": true}}\n\nSin accessConfigs: no tiene IP externa
    %% @step api_compute disco | Crea el disco desde debian-12
    %% @step api_compute logging | Registra la creación | logName: projects/PROYECTO/logs/cloudaudit.googleapis.com%2Factivity\nprotoPayload.methodName: v1.compute.instances.insert\nresource.type: gce_instance
    %% @step api_compute consola | En ejecución; Plataforma de CPU: Intel Broadwell
    %% @step navegador consola | Editar: tipo de máquina, CPU y zona no se pueden cambiar; Cancelar
    %% @step navegador consola | Políticas de disponibilidad
    %% @step consola logging | Registros > Logging | POST /v2/entries:list HTTP/1.1\nHost: logging.googleapis.com\n\n{"resourceNames": ["projects/PROYECTO"],\n "filter": "resource.type=\\"gce_instance\\" AND resource.labels.instance_id=\\"…\\""}
    %% @step logging consola | Expande una entrada: la creación de utility-vm
```