```
C4Deployment
    title Lab02 - Tarea 2 - Verifica la implementación

    %% @pos estudiante x=-68 y=164 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Abre la URL del sitio y comprueba que Apache responde")

    %% @pos equipo x=240 y=100 w=248 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=156 kind=browser url=http://203.0.113.20
        %% @file navegador | / (index.html) | 200 | 0.9 kB
        Container(navegador, "Navegador", "Chrome", "http://203.0.113.20<br/>¡Felicitaciones! Tu pila LAMP está funcionando")
    }

    %% @pos consola x=700 y=-180 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Muestra los detalles de lamp-1-vm y el resumen de lamp-1")

    %% @pos infra_manager x=1160 y=-180 kind=external
    %% @part infra_manager | Resumen | URL del sitio: http://203.0.113.20
    System_Ext(infra_manager, "Infrastructure Manager", "Guarda el resumen de lamp-1")

    %% @pos internet x=700 y=176 kind=cloud
    Container_Ext(internet, "Internet", "", "La red pública entre el equipo y Google Cloud")

    %% @pos proyecto x=1136 y=52 w=1556 h=576 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos vpc x=1160 y=108 w=1508 h=496 kind=cloud
        Deployment_Node(vpc, "default", "Google Cloud VPC") {
            %% @pos ip_externa x=1184 y=170 kind=interface
            Container(ip_externa, "IP externa", "203.0.113.20", "Efímera: Google la traduce a la IP interna")
            %% @pos firewall x=1184 y=460 kind=firewall
            %% @part firewall | lamp-1-tcp-80 | TCP 80 desde 0.0.0.0/0 a la etiqueta lamp-1-deployment
            Container(firewall, "Regla lamp-1-tcp-80", "Cloud Firewall", "Deja entrar el puerto 80 desde internet")
            %% @pos vm x=1616 y=164 w=1028 h=200 kind=appserver
            %% @part vm | Etiqueta de red | lamp-1-deployment: la que elige la regla
            Deployment_Node(vm, "lamp-1-vm", "Compute Engine · Debian 12") {
                %% @pos nic0 x=1640 y=220 kind=interface
                Container(nic0, "nic0", "10.128.0.2", "La IP interna de la VM")
                %% @pos apache x=2040 y=220 kind=webserver
                %% @file apache | /var/www/html/index.html | | 0.9 kB
                %% @file apache | /var/www/html/info.php | | 20 B
                Container(apache, "Servidor web", "Apache HTTP Server", "Escucha en el puerto 80")
                %% @pos disco x=2420 y=220 kind=storage
                ContainerDb(disco, "Disco de arranque", "Persistent Disk (pd-balanced)", "Guarda /var/www/html")
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Abre los detalles de lamp-1-vm", "HTTPS")
    Rel(consola, infra_manager, "Lee el resumen de lamp-1", "JSON/HTTPS")
    Rel(navegador, internet, "Abre la URL del sitio", "HTTP")
    Rel(internet, ip_externa, "Envía la petición", "HTTP")
    Rel(ip_externa, firewall, "Traduce a 10.128.0.2", "NAT 1:1")
    Rel(firewall, nic0, "Permite TCP 80", "TCP")
    Rel(nic0, apache, "Entrega al puerto 80", "TCP")
    Rel(apache, disco, "Lee index.html")

    %% @step estudiante navegador | Abre la implementación lamp-1
    %% @step navegador consola | Pide los detalles de lamp-1 | GET /products/solutions/deployments HTTP/1.1\nHost: console.cloud.google.com
    %% @step consola infra_manager | Lee el resumen | GET /v1/projects/PROYECTO/locations/REGION/deployments/lamp-1 HTTP/1.1\nHost: config.googleapis.com
    %% @step infra_manager consola | Devuelve la URL del sitio y el usuario de MySQL
    %% @step consola navegador | Muestra «URL del sitio: http://203.0.113.20»
    %% @step estudiante navegador | Hace clic en «URL del sitio»: se abre una pestaña nueva
    %% @step navegador internet | Pide la página por HTTP | GET / HTTP/1.1\nHost: 203.0.113.20\nAccept: text/html
    %% @step internet ip_externa | Llega a la IP externa de lamp-1-vm
    %% @step ip_externa firewall | Google la traduce a 10.128.0.2
    %% @step firewall nic0 | La VM tiene la etiqueta lamp-1-deployment: deja pasar el puerto 80
    %% @step nic0 apache | Entrega la petición al puerto 80
    %% @step apache disco | Busca el índice de /var/www/html
    %% @step disco apache | Devuelve index.html
    %% @step apache nic0 | Responde con la página | HTTP/1.1 200 OK\nServer: Apache/2.4.62 (Debian)\nContent-Type: text/html\n\n<!DOCTYPE html>\n<title>Pila LAMP implementada</title>…
    %% @step nic0 firewall | Sale de la VM: la respuesta de una conexión permitida pasa sola
    %% @step firewall ip_externa | Sale con la IP externa como origen
    %% @step ip_externa internet | Viaja de vuelta por Internet
    %% @step internet navegador | Entrega la respuesta
    %% @step navegador estudiante | Muestra «¡Felicitaciones! Tu pila LAMP está funcionando»
```