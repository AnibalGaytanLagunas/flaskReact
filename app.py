from flask import Flask, jsonify
from routes.products_routes import api_bp
from routes.admin_routes import admin_bp
from config import MYSQL_USER,MYSQL_PASSWORD,MYSQL_HOST,MYSQL_PORT,MYSQL_DATABASE
from utils.db import mysql
from error_handlers import register_error_handlers

#from configDev import config
#from configTest import TestingConfig

def create_app(config_object=None):
    app = Flask(__name__)

    #@app.errorhandler(404)
    #def not_found_error(e):
    #    app.logger.exception(e)         
    #    return jsonify({"error": "Error 404"}),404 

    if config_object:
        app.config.from_object(config_object)        
        #app.config.from_object(config['development'])
    app.secret_key = 'planetX0cy56m3vrmx'  
    app.config['MYSQL_HOST'] = MYSQL_HOST
    app.config[MYSQL_PORT] = MYSQL_PORT
    app.config['MYSQL_USER'] = MYSQL_USER
    app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
    app.config['MYSQL_DB'] = MYSQL_DATABASE    
    mysql.init_app(app)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    register_error_handlers(app)  
    #print(app.url_map)   
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)