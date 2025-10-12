# Usar una imagen base de Python
FROM python:3.11-slim as base


# Crear un usuario y grupo no-root con un directorio home
RUN addgroup --system app && adduser --system --group --home /home/app app

# Establecer variables de entorno para el usuario no-root
ENV HOME=/home/app
ENV PATH=/home/app/.local/bin:$PATH

# Crear directorio de la app
WORKDIR /app

# Copiar archivo de requerimientos y cambiar propietario
COPY --chown=app:app requirements.txt .

# Cambiar al usuario no-root ANTES de instalar pip
USER app

# Instalar dependencias de Python como usuario no-root
RUN pip install --no-cache-dir --user -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Exponer el puerto que la aplicación usa
EXPOSE 8550

# Comando para ejecutar la aplicación
CMD ["python", "-u", "main.py"]