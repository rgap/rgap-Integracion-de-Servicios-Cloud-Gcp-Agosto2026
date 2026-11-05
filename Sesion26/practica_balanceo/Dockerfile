# Imagen de la tienda de Pedidos Express.
# Parte de una imagen que ya trae Node.js 22.
FROM node:22-alpine

# Carpeta de trabajo dentro del contenedor.
WORKDIR /app

# Copia el programa de la tienda.
COPY package.json server.js ./

# Comando que se ejecuta al encender el contenedor.
CMD ["node", "server.js", "3001"]
