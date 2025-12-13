# Estimador de Precios Airbnb (Frontend con Flet)

**🌟 Proyecto presentado en la PyConES 2025**

Este proyecto es una aplicación de escritorio multiplataforma construida con **Flet** que sirve como frontend para un servicio de estimación de precios de Airbnb. La aplicación permite a los usuarios seleccionar una ubicación en un mapa, ingresar detalles de la propiedad y recibir una sugerencia de precio basada en un modelo de IA a través de una API externa.

## 🎤 Sobre la Charla (PyConES 2025 - Sevilla España)

Este proyecto fue parte de mi ponencia **"Más allá del modelo: Presenta tus proyectos Python 🐍 como aplicaciones interactivas con Flet"**. Aquí explico cómo transformar scripts de análisis en productos interactivos.

👉 **[Descargar Presentación Completa (PDF)](https://github.com/MayumyCH/Airbnb-Pricing-frontend-flet/blob/main/assets/PyConES%202025%20-%20Mayumy.pdf)**



## 🚀 Características del Proyecto

- **Mapa Interactivo**: Selecciona la ubicación de la propiedad con un simple clic.
- **Formulario Dinámico**: Ingresa detalles como número de huéspedes, habitaciones y noches.
- **Estimación en Tiempo Real**: Comunica con una API de backend para obtener predicciones de precios.
- **Visualización de Resultados**: Muestra el precio sugerido, justificaciones detalladas y un análisis competitivo del vecindario.
- **Docker Ready**: Incluye un `Dockerfile` para una fácil contenerización y despliegue.

## 🛠️ Tech Stack

- **Python 3.11+**
- **Flet**: Framework para crear aplicaciones interactivas en Python.
- **flet-map**: Librería para integrar mapas interactivos en Flet.
- **httpx**: Cliente HTTP asíncrono para comunicarse con la API.
- **Docker**: Para la contenerización de la aplicación.

## 📋 Requisitos Previos

- Python 3.9 o superior.
- `pip` (el gestor de paquetes de Python).
- Opcional: [Docker Desktop](https://www.docker.com/products/docker-desktop/) si deseas ejecutar la aplicación en un contenedor.

## ⚙️ Instalación y Ejecución Local

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### 1. Clonar el Repositorio

```bash
git clone <URL-del-repositorio>
cd Airbnb-Pricing-frontend-flet
```

### 2. Crear y Activar un Entorno Virtual

Es una buena práctica aislar las dependencias del proyecto.

```bash
# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activarlo (los comandos varían según el sistema operativo)

# En Windows (cmd.exe):
.venv\Scripts\activate

# En Windows (bash):
source .venv/Scripts/activate

# En macOS y Linux (bash/zsh):
source .venv/bin/activate

```
Una vez activado, verás `(.venv)` al principio de la línea de comandos de tu terminal.

### 3. Instalar Dependencias

Instala todas las librerías necesarias con un solo comando:

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

**Importante**: Esta es una aplicación frontend. Asegúrate de que el **servicio de backend** que expone el endpoint `/api/v1/predict` esté en funcionamiento. La URL de la API está configurada en `services/api_client.py`.

```bash
flet run main.py
```

La aplicación se abrirá en una ventana de escritorio.

## 🐳 Ejecución con Docker

Si prefieres no instalar las dependencias localmente, puedes usar Docker para ejecutar la aplicación en un entorno aislado.

### 1. Construir la Imagen de Docker

Desde la raíz del proyecto, ejecuta:

```bash
docker build -t airbnb-pricing-frontend .
```

### 2. Ejecutar el Contenedor

```bash
docker run -p 8550:8550 airbnb-pricing-frontend
```
- El comando publica el puerto `8550` del contenedor a tu máquina local.
- Abre tu navegador y ve a `http://localhost:8550` para ver la aplicación web.

## 📂 Estructura del Proyecto

```
Airbnb-Pricing-frontend-flet/
├── assets/             # Recursos estáticos (marcador del mapa).
├── components/         # Componentes de UI reutilizables (mapa, formulario, panel de resultados).
├── services/           # Lógica para comunicarse con servicios externos (API client).
├── views/              # Vistas principales que ensamblan los componentes.
├── .dockerignore       # Archivos a ignorar por Docker.
├── Dockerfile          # Define el entorno para la imagen de Docker.
├── main.py             # Punto de entrada de la aplicación Flet.
└── requirements.txt    # Dependencias de Python.
```
