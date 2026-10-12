# FlaskReact — Backend API

API REST para la gestión de productos, desarrollada con Flask y MySQL.

## Requisitos

- Python 3.12 recomendado, coincidiendo con la versión usada en GitHub Actions.
- MySQL compatible con `Flask-MySQLdb`.
- Bibliotecas de desarrollo de MySQL necesarias para instalar el controlador, según el sistema operativo.

## Instalación

Clona el repositorio y entra en el directorio:

```bash
git clone https://github.com/AnibalGaytanLagunas/flaskReact.git
cd flaskReact
python -m venv .venv
```

Activa el entorno virtual.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux o macOS:

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si la instalación de `Flask-MySQLdb` falla, instala primero las bibliotecas de desarrollo de MySQL requeridas por tu sistema operativo.

## Configuración

Copia `.env.example` a `.env` y configura los valores de tu entorno. La configuración normal requiere `SECRET_KEY`, `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD` y `MYSQL_DATABASE`; `MYSQL_PORT` usa por defecto el puerto 3306.

Consulta [Configuración del backend](docs/CONFIGURACION.md) para los perfiles y las variables de entorno, incluidas las de pruebas.

No subas `.env`, contraseñas ni claves reales al repositorio. Usa credenciales y una base de datos dedicadas a pruebas.

## Base de datos

Crea la base de datos `restaurantdb` y la tabla `products` con una estructura compatible con el backend. `utils/createdb.sql` contiene instrucciones de inicialización y datos de ejemplo. **Revísalo antes de ejecutarlo**: incluye un cambio de contraseña para la cuenta MySQL `root` y no debe ejecutarse indiscriminadamente en una instalación existente.

## Iniciar la aplicación

Con el entorno virtual activo y las variables configuradas:

```bash
python app.py
```

El perfil predeterminado es `production`. Para desarrollo local, configura `APP_ENV=development`. `FLASK_DEBUG` controla la depuración en ese perfil; no habilites la depuración en producción.

## API

Los endpoints se describen en la [Referencia de la API](docs/API.md).

| Método | Ruta | Operación |
|---|---|---|
| `GET` | `/products` | Listar productos |
| `GET` | `/products/{product_id}` | Consultar un producto |
| `POST` | `/products` | Crear un producto |
| `PUT` | `/products/{product_id}` | Sustituir todos los datos de un producto |
| `DELETE` | `/products/{product_id}` | Eliminar un producto |

`PUT` es una actualización completa: requiere `name`, `price` y `description`. Las rutas `/admin` y `/login` están deshabilitadas hasta implementar autenticación y responden con HTTP 503.

## Pruebas

Ejecuta las pruebas disponibles:

```bash
python -m pytest -q
```

Las pruebas de integración con MySQL requieren una base de datos de pruebas configurada. Consulta [Configuración del backend](docs/CONFIGURACION.md).

## Calidad y seguridad de dependencias

```bash
python -m ruff check .
python -m ruff format --check .
python -m pip_audit -r requirements.txt
```

Para aplicar correcciones automáticas cuando proceda:

```bash
python -m ruff check . --fix
python -m ruff format .
```

Revisa los cambios y vuelve a ejecutar las pruebas después de aplicar correcciones.

## Integración continua

El workflow [Backend CI](.github/workflows/tests.yml) se ejecuta en los eventos configurados para la rama `main`. Instala dependencias, prepara MySQL, ejecuta `pip-audit`, verifica Ruff y ejecuta pytest.

Consulta el resultado de cada ejecución en GitHub Actions. La existencia del workflow no garantiza por sí sola que todas las comprobaciones hayan pasado.
