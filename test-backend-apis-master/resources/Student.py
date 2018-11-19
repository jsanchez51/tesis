from flask_restful import abort, Resource, reqparse
import simplejson as json
from psycopg2 import DatabaseError
from textwrap import dedent
from common.BD import BD
from flask import make_response, jsonify, request
from datetime import datetime
#base  de datos
import psycopg2
# Postgres
PSQL_HOST = "localhost"
PSQL_PORT = "5432"
PSQL_USER = "postgres"
PSQL_PASS = "0000"
PSQL_DB   = "sistemaDocente"

class StudentInsertInitial(BD, Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()

    def get(self):
        try:
            # consultar facultad
            resultfaculty = self.queryAll(dedent("""SELECT nombre FROM facultad"""))

            # consultar carrera
            resultProfession = self.queryAll(dedent("""SELECT nombre, tipo FROM carrera"""))

            # consultar estudiantes
            resultStudent = self.queryAll(dedent("""\
            SELECT cedula, nacionalidad, nombre, apellido, sexo, fecha_nacimiento, telefono1, telefono2, email, edo_procedencia 
            FROM estudiante"""))
            studentList = []
            for row in resultStudent:
                row['fecha_nacimiento'] = row['fecha_nacimiento'].strftime('%Y-%m-%d')
                studentList.append(row)
            resultStudent = studentList

            # consultar relaciones
            resultRelationship = self.queryAll(dedent("""\
            SELECT e.cedula AS estudiante, c.nombre AS carrera, f.nombre AS facultad
	        FROM estudiante AS e 
	        INNER JOIN carrera AS c ON (e.id_carrera = c.id)
	        INNER JOIN facultad AS f ON (c.id_facultad = f.id)"""))
            print(resultRelationship)     
            response = {
                "hechos-estudiante-carrera-facultad": {"items": resultRelationship},
                "dim-facultad": {"items": resultfaculty}, 
                "dim-carrera": {"items":resultProfession}, 
                "dim-estudiante": {"items": resultStudent} 
                
            }  
        except DatabaseError as e:
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))

        return json.dumps(response), 200, { 'Access-Control-Allow-Origin': '*' }

        
        
class StudentUpdate(BD, Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    
    def get(self, date_update):

        try:
            date_update = datetime.strptime(date_update, '%Y-%m-%d %H:%M:%S')
            print(date_update)
            # consultar facultad
            resultfaculty = self.queryAll(dedent("""SELECT nombre FROM facultad WHERE updated_date = %s"""), [date_update])
            # consultar carrera
            resultProfession = self.queryAll(dedent("""SELECT nombre, tipo FROM carrera WHERE updated_date = %s"""), [date_update])

            # consultar estudiantes
            resultStudent = self.queryAll(dedent("""\
            SELECT cedula, nacionalidad, nombre, apellido, sexo, fecha_nacimiento, telefono1, telefono2, email, edo_procedencia 
            FROM estudiante
            WHERE updated_date >= %s"""), [date_update])
            studentList = []
            for row in resultStudent:
                row['fecha_nacimiento'] = row['fecha_nacimiento'].strftime('%Y-%m-%d')
                studentList.append(row)
            resultStudent = studentList
            print(resultStudent)
            # consultar relaciones
            resultRelationship = self.queryAll(dedent("""\
            SELECT e.cedula AS estudiante, c.nombre AS carrera, f.nombre AS facultad
	        FROM estudiante AS e 
	        INNER JOIN carrera AS c ON (e.id_carrera = c.id)
	        INNER JOIN facultad AS f ON (c.id_facultad = f.id)"""))
            response = {
                "hechos-estudiante-carrera-facultad": {"items": resultRelationship},
                "dim-facultad": {"items": resultfaculty}, 
                "dim-carrera": {"items":resultProfession}, 
                "dim-estudiante": {"items": resultStudent}
            }  
            
        except DatabaseError as e:
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))

        return jsonify(response), 200, { 'Access-Control-Allow-Origin': '*' }



    

