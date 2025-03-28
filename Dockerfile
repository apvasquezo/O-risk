# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que escucha el backend
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]  # Cambiar "main.py" al archivo principal de tu backend
