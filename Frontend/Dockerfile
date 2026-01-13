FROM node:18-alpine

WORKDIR /app

# 1. Copiamos el package.json real
COPY package*.json ./

# 2. Instalamos las dependencias (React, Vite, Bootstrap)
RUN npm install

# 3. Copiamos todo el código fuente (src, index.html, vite.config.js)
COPY . .

# 4. Exponemos el puerto
EXPOSE 5173

# 5. Arrancamos el servidor de desarrollo
CMD ["npm", "run", "dev"]