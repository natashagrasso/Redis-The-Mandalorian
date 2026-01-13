# 1. Usamos una versión ligera de Python 3.12
FROM python:3.12-slim

# 2. Definimos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos los requerimientos primero (para aprovechar la caché)
COPY requirements.txt .

# 4. Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos TODO el código fuente (app.py, services.py, config.py) a la carpeta /app
COPY . .

# 6. Exponemos el puerto 5000 para que se pueda acceder desde fuera
EXPOSE 5000

# 7. Comando de inicio: Ejecutamos el script principal directamente con Python
CMD ["python", "app.py"]