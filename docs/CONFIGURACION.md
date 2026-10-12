# Configuración del backend

## Perfiles de aplicación

El perfil se selecciona mediante `APP_ENV` al crear la aplicación.

| Perfil | Comportamiento |
|---|---|
| `production` | Perfil predeterminado; `DEBUG=False`. |
| `development` | Permite activar la depuración mediante `FLASK_DEBUG`. |
| `testing` | Activa `TESTING=True` y desactiva la depuración. |

Un valor desconocido de `APP_ENV` provoca un error de configuración. Los perfiles utilizan `Config` como base, salvo las opciones que sobrescribe cada perfil.

## Variables de entorno

| Variable | Uso |
|---|---|
| `APP_ENV` | Perfil: `production`, `development` o `testing`. Predeterminado: `production`. |
| `FLASK_DEBUG` | Activa la depuración en desarrollo con `1`, `true`, `yes` u `on`, sin distinguir mayúsculas. |
| `SECRET_KEY` | Clave secreta requerida por la configuración base. |
| `MYSQL_HOST` | Servidor MySQL del perfil normal. |
| `MYSQL_PORT` | Puerto MySQL; predeterminado `3306`. |
| `MYSQL_USER` | Usuario MySQL del perfil normal. |
| `MYSQL_PASSWORD` | Contraseña MySQL del perfil normal. |
| `MYSQL_DATABASE` | Base de datos del perfil normal. |
| `TEST_SECRET_KEY` | Clave para pruebas; tiene un valor predeterminado en `TestingConfig`. |
| `TEST_MYSQL_HOST` | Servidor MySQL de pruebas; predeterminado `127.0.0.1`. |
| `TEST_MYSQL_PORT` | Puerto MySQL de pruebas; predeterminado `3306`. |
| `TEST_MYSQL_USER` | Usuario MySQL de pruebas; predeterminado `root`. |
| `TEST_MYSQL_PASSWORD` | Contraseña MySQL de pruebas; tiene un valor predeterminado local. |
| `TEST_MYSQL_DATABASE` | Base de datos de pruebas; predeterminada `restaurantdb`. |
| `RUN_DB_INTEGRATION` | Variable configurada por el workflow para solicitar pruebas de integración; su efecto concreto depende de cómo la lean las pruebas. |

Las variables `TEST_*` configuran `TestingConfig`. No utilices los valores predeterminados de pruebas en producción. Configura credenciales propias y una base de datos aislada.

## Preparar el entorno local

1. Copia `.env.example` a `.env`.
2. Selecciona el perfil adecuado.
3. Configura una clave secreta y credenciales válidas.
4. Crea una base de datos exclusiva para la aplicación y concede los permisos necesarios al usuario MySQL.
5. Inicia la aplicación con `python app.py`.

La configuración carga las variables de `.env` mediante `python-dotenv`. No subas el archivo `.env`, contraseñas ni claves reales al repositorio.

## Base de datos y pruebas

Ejecuta las pruebas con:

```bash
python -m pytest -q
```

Las pruebas de integración requieren una instancia MySQL accesible y las variables `TEST_MYSQL_HOST`, `TEST_MYSQL_PORT`, `TEST_MYSQL_USER`, `TEST_MYSQL_PASSWORD` y `TEST_MYSQL_DATABASE` configuradas para esa instancia.

El workflow `.github/workflows/tests.yml` configura un servicio MySQL y ejecuta `utils/createdb.sql` antes de pytest. **Inspecciona el script antes de ejecutarlo manualmente**: incluye una modificación de la contraseña de la cuenta `root`. No lo ejecutes sin revisar sus efectos en una instancia que contenga datos importantes.

## Ruff y pip-audit

Ejecuta desde la raíz del repositorio:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pip_audit -r requirements.txt
```

- Ruff detecta problemas de linting y permite comprobar el formato.
- `pip-audit` busca vulnerabilidades conocidas en las dependencias declaradas.
- Pytest ejecuta las pruebas unitarias y las pruebas de integración habilitadas por la configuración.

Para aplicar correcciones automáticas de Ruff cuando proceda:

```bash
python -m ruff check . --fix
python -m ruff format .
```

Revisa los cambios y vuelve a ejecutar las pruebas después de corregir el código. Estas herramientas cubren aspectos diferentes y ninguna garantiza por sí sola que la aplicación esté libre de defectos o vulnerabilidades.

## GitHub Actions

El workflow `.github/workflows/tests.yml` se ejecuta en los eventos configurados para la rama `main`. Instala dependencias, prepara MySQL, ejecuta `pip-audit`, verifica Ruff y ejecuta pytest.

Consulta el resultado de cada ejecución en GitHub Actions. Si cambian las versiones de Python, los comandos, las variables de entorno o la preparación de MySQL, actualiza esta documentación.
