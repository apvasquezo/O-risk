# Usar una imagen base de Python ligera
FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo requirements.txt primero para aprovechar caché de Docker
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY . .

# Exponer el puerto en el que escucha el backend
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]