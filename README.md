# Asfalto App – Constructora Asolca, SRL

Sitio web corporativo para una empresa de asfalto y construcción, desarrollado con **Flask**.

Incluye panel de administración (Flask-Admin), gestión de servicios, proyectos, historias de éxito, mensajes de contacto, popup de bienvenida y usuarios con roles.

## Características principales

- Página de inicio con video hero y carruseles
- Secciones dinámicas (servicios, proyectos, historias de éxito)
- Formularios de contacto (página completa + formulario rápido en el footer)
- Panel de administración protegido con Flask-Login y roles (`admin` / `editor`)
- Subida de imágenes a **Cloudinary**
- Migraciones con Flask-Migrate (Alembic)
- Soporte para PostgreSQL (recomendado) o SQLite local
- Listo para desplegar en Render

## Requisitos

- Python 3.10+
- Cuenta en [Cloudinary](https://cloudinary.com) (para imágenes)
- Base de datos PostgreSQL (recomendado: [Neon](https://neon.tech) – plan gratuito permanente)

## Instalación local

1. Clona el repositorio:

```bash
git clone https://github.com/jrg2705/asfalto_app.git
cd asfalto_app
```

2. Crea un entorno virtual e instala dependencias:

```bash
python -m venv venv
source venv/bin/activate   # En Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

3. Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria
DATABASE_URL=sqlite:///instance/site.db
# O usa Postgres local / Neon:
# DATABASE_URL=postgresql://usuario:password@host/dbname?sslmode=require

CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

4. Inicializa la base de datos y crea un usuario admin:

```bash
flask db upgrade
flask seed-admin
```

> **Importante:** El usuario por defecto es `admin` / `adminpassword`. Cámbialo inmediatamente después del primer login.

5. Ejecuta la aplicación:

```bash
python app.py
# o
flask run
```

Abre http://127.0.0.1:5000

### Comandos CLI útiles

```bash
flask create-db          # Crea las tablas (alternativa a migrate)
flask seed-admin         # Crea el usuario admin por defecto
flask create-admin <user> <password>   # Crea un admin personalizado
flask assign-role <user> <admin|editor>
flask db upgrade         # Aplica migraciones
flask db migrate -m "mensaje"   # Genera una nueva migración
```

## Despliegue en Render (recomendado)

### ¿Por qué no usar la base de datos gratuita de Render?

La Postgres gratuita de Render **expira a los 30 días** y luego se elimina.  
**No es necesario** tener la base de datos en Render.

### Opción recomendada: Neon (Postgres gratuito permanente)

1. Ve a [neon.tech](https://neon.tech) y crea una cuenta (gratis, sin tarjeta).
2. Crea un nuevo proyecto.
3. Copia la **connection string** (usa la que incluye `?sslmode=require`).

### Pasos para desplegar en Render

1. Entra a [render.com](https://render.com) e inicia sesión con GitHub.
2. **New → Web Service** y selecciona el repositorio `asfalto_app`.
3. Configuración:
   - **Name**: `asfalto-app` (o el que prefieras)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
4. En **Environment** agrega estas variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Una cadena larga y aleatoria |
| `DATABASE_URL` | La connection string de Neon |
| `CLOUDINARY_CLOUD_NAME` | Tu cloud name |
| `CLOUDINARY_API_KEY` | Tu API key |
| `CLOUDINARY_API_SECRET` | Tu API secret |

5. Haz clic en **Create Web Service**.
6. Cuando el deploy termine, abre la **Shell** del servicio y ejecuta:

```bash
flask db upgrade
flask seed-admin
```

7. Entra a `/admin` (o la URL que te dio Render + `/login`), inicia sesión con `admin` / `adminpassword` y **cambia la contraseña inmediatamente**.

### Usando el archivo `render.yaml` (Blueprint)

Si prefieres desplegar con Infrastructure as Code:

1. En el dashboard de Render ve a **Blueprints → New Blueprint Instance**.
2. Selecciona el repositorio.
3. Render leerá el `render.yaml` y creará el Web Service.
4. Te pedirá que completes las variables marcadas como secretas (`SECRET_KEY`, `DATABASE_URL`, Cloudinary, etc.).
5. Después del deploy, ejecuta en la Shell:

```bash
flask db upgrade
flask seed-admin
```

> El `render.yaml` incluido **no crea** una base de datos en Render (para evitar el límite de 30 días). Usa Neon u otro proveedor externo.

## Notas importantes

- **Cold starts**: En el plan Free de Render la app se duerme después de ~15 minutos sin tráfico. La primera visita puede tardar 30-60 segundos.
- **Imágenes**: Las imágenes grandes en `static/images` hacen el deploy más lento. Idealmente muévelas a Cloudinary.
- **Seguridad**: Nunca subas el archivo `.env` al repositorio. Cambia la contraseña del admin en producción.
- **Email**: La configuración de correo está preparada en `config.py` pero aún no se usa para notificar nuevos mensajes de contacto.

## Estructura del proyecto

```
asfalto_app/
├── app.py              # Aplicación principal y rutas
├── config.py           # Configuración (env vars)
├── models.py           # Modelos SQLAlchemy
├── forms.py            # Formularios WTForms
├── requirements.txt
├── render.yaml         # Blueprint para Render
├── migrations/         # Migraciones Alembic
├── static/             # CSS, JS, imágenes, videos
└── templates/          # Plantillas Jinja2
```

## Licencia

Proyecto privado / uso interno de la empresa.
