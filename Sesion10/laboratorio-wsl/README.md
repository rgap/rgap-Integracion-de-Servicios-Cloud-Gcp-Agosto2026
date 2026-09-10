# Laboratorio — Instalación de Windows Subsystem for Linux (WSL)

Acompaña a las diapositivas 22 a 24 de la Sesión 10. El objetivo es tener un
entorno Ubuntu dentro de Windows para practicar el resto del curso (permisos,
servicios, `nginx`, `gcloud`) sin crear una máquina virtual completa.

Si trabajas en macOS o Linux, no necesitas WSL: ya tienes una terminal Unix.
Usa una máquina virtual o la propia VM de GCP para las prácticas.

## Requisitos

- Windows 10 versión 2004 o superior (compilación `19041`+) o Windows 11.
- Virtualización habilitada en el firmware (BIOS/UEFI). En la mayoría de equipos
  ya lo está; solo hace falta revisarlo si WSL 2 no arranca.

## Comprobar si ya está instalado

Abre PowerShell y ejecuta:

```powershell
wsl --version
wsl --status
```

Si el comando no existe, todavía no está instalado: sigue con el paso 1.

## 1. Instalar

Abre **PowerShell como administrador** (clic derecho → *Ejecutar como
administrador*) y ejecuta:

```powershell
wsl --install
```

Esto activa los componentes necesarios, fija **WSL 2** como versión por defecto
y descarga **Ubuntu**.

## 2. Reiniciar

Reinicia el equipo. Al volver, se abre una ventana de Ubuntu que termina la
configuración (tarda unos minutos la primera vez).

## 3. Crear el usuario de Linux

```text
Enter new UNIX username: rgap
New password:
Retype new password:
```

Es una cuenta **de Linux**, distinta de la de Windows. Este usuario pertenece al
grupo `sudo`, así que puede elevar privilegios cuando una tarea lo requiere.

## 4. Comprobar

Desde PowerShell:

```powershell
wsl -l -v            # distribuciones instaladas y su versión (debe decir 2)
wsl --list --online  # distribuciones que se pueden instalar
wsl --shutdown       # apaga WSL
```

Dentro de Ubuntu:

```bash
whoami
uname -r             # kernel de Linux real de WSL 2
sudo apt update
explorer.exe .       # abre la carpeta actual en el Explorador de Windows
```

`explorer.exe` llamado desde Linux, y los archivos que se ven desde ambos lados,
son la **integración** que diferencia a WSL de una máquina virtual tradicional.

## Qué hay que poder explicar

- **Qué es WSL:** una función de Windows para ejecutar un entorno GNU/Linux
  dentro de Windows, sin reiniciar y sin crear tú una máquina virtual.
- **WSL 1 vs WSL 2:** WSL 1 traduce las llamadas al sistema de Linux a las de
  Windows (no hay kernel de Linux). WSL 2 trae un kernel de Linux real dentro de
  una máquina virtual ligera gestionada por la tecnología de hipervisor de
  Windows. WSL 2 es la opción por defecto.
- **¿Es igual que virtualizar con un hipervisor?** WSL 2 usa virtualización por
  debajo, pero no es una máquina virtual tradicional: arranca al instante,
  ajusta sus recursos solo y comparte archivos y red con Windows. WSL 1 no usa
  hipervisor en absoluto.
- **Para qué sirve:** entorno de trabajo local. No reemplaza a un servidor de
  producción, que corre en la nube sobre un hipervisor tipo 1.

## Instalar otra distribución (opcional)

```powershell
wsl --install -d Debian
```

## Comandos de referencia

| Comando | Para qué |
| --- | --- |
| `wsl --install` | Instala WSL 2 y Ubuntu |
| `wsl --install -d <distro>` | Instala otra distribución |
| `wsl -l -v` | Lista distribuciones y su versión |
| `wsl --list --online` | Distribuciones disponibles para instalar |
| `wsl --set-default-version 2` | Fija WSL 2 como versión por defecto |
| `wsl --update` | Actualiza el kernel de WSL 2 |
| `wsl --shutdown` | Apaga todas las distribuciones |
| `wsl --version` / `wsl --status` | Versión y estado de la instalación |
