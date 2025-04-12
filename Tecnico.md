# Manual Técnico: Procedimiento de Instalación de la API

## Requisitos Previos

Antes de iniciar la instalación, asegúrese de que el sistema cumpla con los siguientes requisitos:

1. **Python 3.11**: Lenguaje utilizado para el desarrollo de la API.
2. **PostgreSQL 15 o superior**: Base de datos relacional.
3. **PgAdmin** (Opcional): Herramienta gráfica para gestionar PostgreSQL.
4. **Visual Studio Code**: Editor de texto recomendado.
5. **Git**: Herramienta de control de versiones.
6. **Microsoft C++ Redistributable**: Requerido para bibliotecas de Python.
7. **Microsoft C++ Build Tools**: Necesario para compilar extensiones en Python.

## Procedimiento de Instalación

### 1. Clonar el Repositorio

Descargue el código fuente desde el repositorio oficial de GitHub:

```bash
git clone https://github.com/apvasquezo/O-risk.git
cd o-risk
```

### 2. Crear un Entorno Virtual

Configure un entorno virtual para gestionar las dependencias del proyecto:

```bash
python -m venv venv
# Activar el entorno virtual:
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
```

### 3. Instalar Dependencias

Ejecute el siguiente comando para instalar las dependencias necesarias:

```bash
pip install -r requirements.txt
```

### 4. Configuración del Entorno

Cree un archivo `.env` en la raíz del proyecto con las siguientes configuraciones:

```env
DATABASE_URL=postgresql://superrisk:risk2025@localhost:5432/o_risk_db
SECRET_KEY=clave_secreta_para_jwt
INITIAL_SETUP=True
```

### 5. Inicializar la Base de Datos

Inicie el proceso de configuración de la base de datos ejecutando:

```bash
python main.py init-db
```

Este paso:
- Creará las tablas necesarias.
- Registrará un usuario administrador predeterminado con las siguientes credenciales:
  - **Usuario**: `super`
  - **Contraseña**: `risk123`
  - **Rol**: 1

### 6. Ejecutar la API

Para iniciar la API, utilice **Uvicorn** con el siguiente comando:

```bash
uvicorn main:app --reload
```

La API estará disponible en la URL predeterminada: `http://localhost:8000`.

### 7. Verificar el Funcionamiento

1. Abre un navegador o una herramienta como Postman.
2. Realiza una solicitud `POST` al endpoint de inicio de sesión (`/auth/login`) con las credenciales predeterminadas:

**Body (JSON):**

```json
{
  "username": "super",
  "password": "risk123"
}
```

3. Si todo está configurado correctamente, recibirás un token JWT para autenticar futuras solicitudes.

### 8. Configuración Post-Instalación

- **Deshabilitar el Modo de Inicialización**: Modifique el archivo `.env` y establezca `INITIAL_SETUP=False` una vez completada la configuración inicial.

```env
INITIAL_SETUP=False
```

- **Cambiar Contraseña del Administrador**: Por razones de seguridad, cambie la contraseña del usuario administrador mediante el endpoint `/auth/change-password`.

### 9. Opcional: Configurar para Producción

Para un entorno de producción:

- Utilice herramientas como **Gunicorn** o **Uvicorn** en modo asíncrono.
- Configure un proxy inverso con **Nginx**.
- Gestione los procesos con herramientas como **Supervisor** o **PM2**.

---

**Nota:** Para cualquier problema durante la instalación, consulte los registros de errores generados por la API o las herramientas de base de datos.
