```
C4Deployment
    title Lab02 - Tarea 3 - Repaso

    %% @pos estudiante x=-32 y=152 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Implementó una solución lista y comprobó que funciona")

    %% @pos equipo x=220 y=100 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=156 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Usa la consola y abre el sitio de la VM")
    }

    %% @pos consola x=700 y=-160 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Desde Marketplace, un formulario en vez de crear cada recurso a mano")

    %% @pos marketplace x=1140 y=-160 kind=external
    System_Ext(marketplace, "Cloud Marketplace", "La solución preconfigurada: Pila de LAMP de Click to Deploy")

    %% @pos infra_manager x=1580 y=-160 kind=external
    System_Ext(infra_manager, "Infrastructure Manager", "La plantilla que crea todos los recursos de una vez")

    %% @pos internet x=700 y=176 kind=cloud
    Container_Ext(internet, "Internet", "", "Por donde llega cualquier visitante")

    %% @pos proyecto x=1120 y=100 w=1104 h=488 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=2000 y=212 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Crea la VM, el disco y las reglas de firewall")
        %% @pos vm x=1144 y=156 w=588 h=408 kind=appserver
        Deployment_Node(vm, "lamp-1-vm", "Compute Engine · Debian 12", "Linux de la pila LAMP") {
            %% @pos apache x=1168 y=212 kind=webserver
            Container(apache, "Servidor web", "Apache HTTP Server", "La A de LAMP: responde en el puerto 80")
            %% @pos php x=1560 y=212 kind=api
            Container(php, "PHP", "PHP 8.2", "La P: corre dentro de Apache")
            %% @pos mariadb x=1364 y=420 kind=database
            ContainerDb(mariadb, "Base de datos", "MariaDB", "La M: compatible con MySQL")
        }
    }

    %% @pos laboratorio x=1172 y=712 kind=external
    System_Ext(laboratorio, "Google Skills", "Finaliza el lab y borra el proyecto temporal")

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Elige e implementa la solución", "HTTPS")
    Rel(consola, marketplace, "Implementa la Pila de LAMP", "HTTPS")
    Rel(marketplace, infra_manager, "Crea la implementación", "JSON/HTTPS")
    Rel(infra_manager, api_compute, "Crea los recursos de la plantilla", "JSON/HTTPS")
    Rel(navegador, internet, "Abre el sitio", "HTTP")
    Rel(internet, apache, "Llega al puerto 80", "HTTP")
    Rel(apache, php, "Ejecuta los archivos .php", "mod_php")
    Rel(php, mariadb, "Lee y escribe", "SQL/TCP")
    Rel(navegador, laboratorio, "Hace clic en Finalizar lab", "HTTPS")
    Rel(laboratorio, api_compute, "Borra los recursos del proyecto")

    %% @step estudiante navegador | Implementa la Pila de LAMP desde Marketplace
    %% @step navegador consola | Llena un solo formulario: zona y tipo de máquina
    %% @step consola marketplace | Acepta los términos e implementa
    %% @step marketplace infra_manager | Crea la implementación lamp-1
    %% @step infra_manager api_compute | Crea la VM, el disco y las reglas de firewall de una vez
    %% @step estudiante navegador | Abre la URL del sitio
    %% @step navegador internet | Pide la página | GET / HTTP/1.1\nHost: 203.0.113.20
    %% @step internet apache | Llega a Apache por la IP externa
    %% @step apache internet | Responde con la página | HTTP/1.1 200 OK\nContent-Type: text/html
    %% @step internet navegador | Entrega la respuesta
    %% @step navegador estudiante | Ve la página: la pila funciona
    %% @step estudiante navegador | Termina el lab
    %% @step navegador laboratorio | Hace clic en Finalizar lab
    %% @step laboratorio api_compute | Borra lamp-1-vm, su disco y sus reglas
```