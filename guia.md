### Proyecto Flask VERSION SQL  (crud_flask) REST API for REACT

### Requerimientos BD:
 - XAMPP 
 - https://github.com/alexferl/flask-mysqldb
 - https://bootswatch.com/

 
### Indicaciones iniciales

crea carpeta de proyecto y abrir con code.
Desde la terminal integrada ejecutar los comandos siguientes:

### instalar la extención oficial de python para vs code

### instalar virtualenv 

`pip install virtualenv`

### Crea el entorno virtual (aísla todas las dependencias y herramientas )
`virtualenv venv`

### activar el entorno virtual

`.\venv\Scripts\activate`
otra forma que no he probado es
`source env/bin/activate`
### seleccionar el virtualenv creado 
pulsa F1 y escribir
  python: select interpreter 
    busca en el listado el entorno virtual venv, creado en pasos anteriores  

### instalar flask
`pip install flask`
pip install flask, flask-mysqldb, python-dotenv, pydantic, pytest
### instalar mysqldb
`pip install flask-mysqldb`

### instalar dotenv
`pip install python-dotenv`

### instalar Pydantic
`pip install pydantic`

### instalar pytest para las pruebas unitarias
`pip install pytest`

### Elaborar los archivos de configuracion y pruebaspp
`python -c "from app import create_app; print('IMPORT OK')"`

`python -m pytest`

Orden de pruebas
pytest -q tests/test_product_repository.py
pytest -q

### Ejecutar proyecto flask

`python index.py`
Ctrl + c para cancelar ejecucion 

### otros requerimientos

`pip install flask-login`
`pip install flask-WTF`

### listar paquetes del entorno V
`pip list`

### Recursos y recordatorios
https://github.com/alexferl/flask-mysqldb
https://fontawesome.com/
https://flask.palletsprojects.com/en/stable/templating/
https://flask.palletsprojects.com/en/stable/patterns/flashing/
https://getbootstrap.com/
https://uigradients.com/
https://www.pexels.com/
TEMPLATE STRING ALT 96 `
ALT 124  |

### crear la BD desde la linea de comandos
por defecto root no tienen password 
`mysql -u root -p`

presiona enter para ignorar el password

para cambiar la contraseña

`ALTER USER 'root'@'localhost' IDENTIFIED BY 'root1234';`
`FLUSH PRIVILEGES;`

Crear la BD

`CREATE DATABASE restaurantdb;`
`SHOW DATABASES;`

`use restaurantdb;`
`show tables;`

`exit`

no olvidar configurar phpMyAdmin con el nuevo password de root/mysql

### Al terminar el proyecto crear el archivo con la lista de dependencias
`pip freeze > requirements.txt`

### git 
`git init`
`git add .`
`git commit -m "Proyecto Flask-React"`
`git branch -M main`
`git remote add origin https://github.com/AnibalGaytanLagunas/flaskReact.git`
`git push -u origin main`

deshacer cambios en un proyecto que no ha ejecutado `git add .`
Usar:
 `git restore .`  recuperas todos los archivos y líneas borradas



descarga las actualizaciones
`git pull https://github.com/AnibalGaytanLagunas/flaskReact.git main`

El repositorio local tiene un repositorio remoto vinculado.
Confirma esto ejecutando `git remote -v`


### Extenciones VSC
- REST Client (Huachao Mao)
- python (Microsoft)
