#!/usr/bin/env bash
# Arranca el sitio. Necesita permiso de ejecución: chmod u+x iniciar.sh
set -e
cd "$(dirname "$0")"
python3 sitio.py
