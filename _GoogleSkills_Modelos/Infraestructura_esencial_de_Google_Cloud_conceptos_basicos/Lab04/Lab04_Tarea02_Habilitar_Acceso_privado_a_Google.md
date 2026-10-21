```
C4Deployment
    title Lab04 - Tarea 2 - Habilita el Acceso privado a Google

    %% @pos estudiante x=-144 y=252 kind=person avatar=end-user-male
    Person(estudiante, "Estudiante", "Copia una imagen al bucket y desde él, en Cloud Shell y en la VM")

    %% @pos equipo x=220 y=200 w=244 h=200 kind=client
    Deployment_Node(equipo, "Computadora del estudiante", "Equipo local") {
        %% @pos navegador x=264 y=256 kind=browser url=console.cloud.google.com
        Container(navegador, "Navegador", "Chrome", "Muestra la consola y Cloud Shell")
    }

    %% @pos consola x=700 y=-160 kind=webapp url=console.cloud.google.com
    Container(consola, "Consola de Google Cloud", "Google Cloud Console", "Crea el bucket y edita la subred")

    %% @pos cloudshell x=676 y=260 w=248 h=608 kind=appserver
    Deployment_Node(cloudshell, "Cloud Shell", "Google Cloud Shell · Debian", "Tiene IP externa") {
        %% @pos terminal x=700 y=316 kind=terminal
        Container(terminal, "Terminal web", "Bash", "export MY_BUCKET y gcloud storage cp")
        %% @pos gcloud x=700 y=520 kind=terminal
        Container(gcloud, "gcloud CLI", "Google Cloud CLI", "Copia la imagen y abre el túnel SSH")
        %% @pos home_cs x=700 y=724 kind=storage
        %% @file home_cs | access.svg | | 9 kB
        ContainerDb(home_cs, "Directorio personal", "$HOME", "La copia de access.svg en Cloud Shell")
    }

    %% @pos cloud_training x=308 y=520 kind=storage
    %% @file cloud_training | gcpnet/private/access.svg | | 9 kB
    SystemDb_Ext(cloud_training, "gs://cloud-training", "Bucket público de Google con la imagen del lab")

    %% @pos iap x=1136 y=1080 kind=external
    System_Ext(iap, "IAP", "Lleva SSH a vm-internal desde 35.235.240.0/20")

    %% @pos proyecto x=1100 y=-272 w=1052 h=1188 kind=cloud
    Deployment_Node(proyecto, "Proyecto temporal del lab", "Proyecto de Google Cloud") {
        %% @pos api_compute x=1124 y=-160 kind=api
        Container(api_compute, "API de Compute Engine", "REST · googleapis.com", "Activa el Acceso privado a Google en la subred")
        %% @pos bucket x=1124 y=240 kind=storage url=https://storage.googleapis.com/qwiklabs-gcp-04-8f2c1d
        %% @file bucket | access.svg | | 9 kB
        ContainerDb(bucket, "qwiklabs-gcp-04-8f2c1d", "Cloud Storage · multirregión US", "El bucket del lab, con access.svg")
        %% @pos privatenet x=1480 y=-216 w=648 h=1108 kind=cloud
        Deployment_Node(privatenet, "privatenet", "Google Cloud VPC", "Red de modo personalizado") {
            %% @pos regla_ssh x=1504 y=-160 kind=firewall
            Container(regla_ssh, "privatenet-allow-ssh", "Regla de Cloud Firewall · entrada", "Permite tcp:22 desde 35.235.240.0/20 (IAP) a todas las instancias")
            %% @pos subred x=1504 y=20 w=600 h=848 kind=generic
            %% @part subred | Acceso privado a Google | Activo: se activa en esta tarea; antes estaba desactivado
            Deployment_Node(subred, "Subred privatenet-us", "VPC de Google Cloud · 10.130.0.0/20", "us-central1") {
                %% @pos vm x=1528 y=76 w=552 h=768 kind=appserver
                %% @part vm | IP externa | Ninguna
                Deployment_Node(vm, "vm-internal", "Compute Engine · Debian 12", "us-central1-c · e2-standard-2") {
                    %% @pos sshd x=1552 y=132 kind=generic
                    Container(sshd, "Servidor SSH", "OpenSSH · TCP 22", "Abre la sesión del estudiante")
                    %% @pos nic x=1864 y=132 kind=interface
                    Container(nic, "nic0", "10.130.0.2", "Solo IP interna")
                    %% @pos bash_vm x=1672 y=328 kind=terminal
                    Container(bash_vm, "Terminal de la VM", "Bash", "estudiante@vm-internal")
                    %% @pos gcloud_vm x=1700 y=512 kind=terminal
                    Container(gcloud_vm, "gcloud de la VM", "Google Cloud CLI", "gcloud storage cp desde el bucket")
                    %% @pos home_vm x=1860 y=700 kind=storage
                    %% @file home_vm | access.svg | | 9 kB
                    ContainerDb(home_vm, "Directorio personal", "$HOME", "access.svg, copiada cuando ya hay acceso")
                }
            }
        }
    }

    Rel(estudiante, navegador, "Utiliza")
    Rel(navegador, consola, "Crea el bucket y edita la subred", "HTTPS")
    Rel(consola, bucket, "Crea el bucket y muestra access.svg", "HTTPS")
    Rel(consola, api_compute, "Edita privatenet-us", "JSON/HTTPS")
    Rel(navegador, terminal, "Abre la terminal", "WebSocket/HTTPS")
    Rel(terminal, gcloud, "Ejecuta")
    Rel(gcloud, cloud_training, "Lee access.svg", "JSON/HTTPS")
    Rel(gcloud, bucket, "Copia access.svg", "JSON/HTTPS")
    Rel(gcloud, home_cs, "Guarda access.svg")
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
    Rel(gcloud_vm, home_vm, "Guarda access.svg")

    %% @step estudiante navegador | Cloud Storage > Crear bucket
    %% @step navegador consola | Nombre: el ID del proyecto; Multirregión
    %% @step consola bucket | Crea el bucket | POST /storage/v1/b?project=PROYECTO HTTP/1.1\nHost: storage.googleapis.com\n\n{"name": "qwiklabs-gcp-04-8f2c1d", "location": "US"}
    %% @step navegador terminal | Guarda el nombre del bucket | export MY_BUCKET=qwiklabs-gcp-04-8f2c1d\necho $MY_BUCKET
    %% @step terminal gcloud | Copia la imagen al bucket | gcloud storage cp gs://cloud-training/gcpnet/private/access.svg gs://$MY_BUCKET
    %% @step gcloud cloud_training | Lee la imagen | GET /storage/v1/b/cloud-training/o/gcpnet%2Fprivate%2Faccess.svg?alt=media HTTP/1.1\nHost: storage.googleapis.com
    %% @step gcloud bucket | La sube al bucket | POST /upload/storage/v1/b/qwiklabs-gcp-04-8f2c1d/o?uploadType=media&name=access.svg HTTP/1.1\nHost: storage.googleapis.com\nContent-Type: image/svg+xml
    %% @step consola bucket | Abre access.svg en el bucket
    %% @step terminal gcloud | La copia a Cloud Shell | gcloud storage cp gs://$MY_BUCKET/*.svg .
    %% @step gcloud bucket | Llega: Cloud Shell tiene IP externa
    %% @step gcloud home_cs | Guarda access.svg en $HOME
    %% @step terminal gcloud | Entra a vm-internal | gcloud compute ssh vm-internal --zone us-central1-c --tunnel-through-iap
    %% @step gcloud iap | Abre el túnel
    %% @step iap sshd | privatenet-allow-ssh deja pasar el puerto 22
    %% @step sshd bash_vm | estudiante@vm-internal
    %% @step bash_vm gcloud_vm | La copia a la VM | export MY_BUCKET=qwiklabs-gcp-04-8f2c1d\ngcloud storage cp gs://$MY_BUCKET/*.svg .
    %% @step gcloud_vm bucket | Queda esperando (Ctrl+C) | Sin IP externa y sin Acceso privado a Google en privatenet-us,\nvm-internal no llega a storage.googleapis.com
    %% @step navegador consola | Edita privatenet-us: Acceso privado a Google Activo
    %% @step consola api_compute | Activa el Acceso privado a Google | POST /compute/v1/projects/PROYECTO/regions/us-central1/subnetworks/privatenet-us/setPrivateIpGoogleAccess HTTP/1.1\nHost: compute.googleapis.com\n\n{"privateIpGoogleAccess": true}
    %% @step bash_vm gcloud_vm | Vuelve a copiarla | gcloud storage cp gs://$MY_BUCKET/*.svg .
    %% @step gcloud_vm bucket | Ahora llega
    %% @step gcloud_vm home_vm | Guarda access.svg en la VM
```