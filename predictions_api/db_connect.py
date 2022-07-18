
import json
from flaskext.mysql import MySQL
from flask import  jsonify

class DB_Connect:

    def __init__(self, app):
        self.app = app
        #Set database credentials in config.
        self.app.config['MYSQL_DATABASE_USER'] = 'root'
        self.app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
        self.app.config['MYSQL_DATABASE_DB'] = 'nextwordpredection'
        self.app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        self.mysql = MySQL()
        self.mysql.init_app(app)


#function to store all searched queries in the database
    def store(self,user,input_text,seeds_out):
        try:
                conn = self.mysql.connect()
                cursor = conn.cursor()
                json_string = json.dumps(seeds_out)
                insert_predections = """INSERT INTO predections(user_name, input_text,data) 
                                    VALUES(%s, %s, %s)"""
                cursor.execute(insert_predections, (user, input_text,json_string))
                conn.commit()
                response = jsonify('stored data into database.')
        except Exception as e:
                print(e)
                response = jsonify('Failed to add data into database.')         
        finally:
                cursor.close()
                conn.close()
                return(response)



