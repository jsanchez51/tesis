# -*- coding: utf-8 -*-
from flask import Flask, make_response, request
from flask_cors import CORS
from flask_restful import Api
import os
from werkzeug.utils import secure_filename
from flask_restful import reqparse, abort, Api, Resource
import simplejson as json
import csv, operator
import sys
import types
import psycopg2
import random
import requests
import openpyxl
import  re
from datetime import datetime
import json
from json import JSONDecoder
from json import JSONEncoder
import time
from datetime import date, datetime
# from threading import Timer
# import threading
# from threading import Thread
# import thread
# Postgres

# Abrir un cursor para realizar operaciones sobre la base de datos

# Resources
# Postgres
from resources.Student import StudentInsertInitial, StudentUpdate
from resources.Student import StudentInsertInitial, StudentUpdate

# UPLOAD_FOLDER = 'C:/Users\Mariangela Goncalves/Desktop/prueba/test-backend-apis-master'
#UPLOAD_FOLDER = "C:/Users\ESCRITORIO\Desktop\\versiones pruebas\prueba4\\test-backend-apis-master"

UPLOAD_FOLDER = os.getcwd() + '\\'

if(sys.platform == 'linux'):
    UPLOAD_FOLDER = os.getcwd() + '/'

ALLOWED_EXTENSIONS = set([ 'xlsx','csv'])
# random.seed(100)

# instantiate the app
app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# enable CORS
CORS(app)
PSQL_HOST = "localhost"
PSQL_PORT = "5432"
PSQL_USER = "postgres"
PSQL_PASS = "0000"
PSQL_DB   = "estudiante"
connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
conn = psycopg2.connect(connstr)
cur = conn.cursor()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class File(Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    def post(self,id,user):
         file = request.files['file']
         if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            lectura=[]

            if(id=='11'):
                lectura= leer_Archivo_Preg_Info_Estud(UPLOAD_FOLDER + filename,user)
            if(id=='21'):
                lectura= leer_Archivo_Post_Info_Estud(UPLOAD_FOLDER + filename,user)
            return json.dumps({'exitosa':lectura}), 201, { 'Access-Control-Allow-Origin': '*' }
         else:
            # return error
            return json.dumps({'exitosa':'error'}), 201, { 'Access-Control-Allow-Origin': '*' }

def leer_Archivo_Preg_Info_Estud(filename,user):
    
   
    with open(filename) as csvarchivo:
       
        entrada = csv.DictReader(csvarchivo,delimiter=';')
        cont=2
        resul=[]
        orden=entrada.fieldnames
        orden_columna=['a_ci','primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','sexo','fecha_nacimiento','etnia','discapacidad','correo','tlf_local','tlf_celular','edo_procedencia','nro_semestr_anno','nombre_carrera','estudio_adicional','nacionalidad','direccion_actual']
        longitud_orden= len(orden_columna)
        # or user==''
        print(user)
        if(all(i == j for i, j in zip(orden,orden_columna))):    
            for reg in entrada:
             sqlquery10 = "select f.nombre from carrera as c inner join facultad as f on (c.id_facultad=f.id) where c.nombre='{}';".format(reg['nombre_carrera'])
             cur.execute(sqlquery10)
             ressult=cur.fetchone()
             if((ressult and ressult[0]== user.upper()) or 'vicerrector'== user  ):
                if (reg.get("a_ci")):
                    if not (reg['a_ci'].isdigit()):
                        resul.append("En la columna a_ci, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: a_ci\n" in resul ):
                        resul.append("No se encuentra la columna: a_ci\n")
                
                if (reg.get("primer_nombre")):
                    if not (type(reg['primer_nombre'])==str):
                        resul.append("En la columna primer_nombre, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: primer_nombre" in resul ):
                        resul.append("No se encuentra la columna: primer_nombre")
                        
                if (reg.get("segundo_nombre")):
                    if(reg['segundo_nombre']==""):
                        reg['segundo_nombre']= "NO EXITE"
                    if not (type(reg['segundo_nombre'])==str):
                        resul.append("En la columna segundo_nombre , fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: segundo_nombre\n" in resul ):
                        resul.append("No se encuentra la columna: segundo_nombre\n")
            
                if (reg.get("primer_apellido")):
                    if not (type(reg['primer_apellido'])==str):
                        resul.append("En la columna primer_apellido, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: primer_apellido\n" in resul ):
                        resul.append("No se encuentra la columna: primer_apellido\n")

                if (reg.get("segundo_apellido")):
                    if(reg['segundo_apellido']==""):
                        reg['segundo_apellido']= "NO EXITE"            
                        if not (type(reg['segundo_apellido'])==str):
                            resul.append("En la columna segundo_apellido, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: segundo_apellido\n" in resul ):
                        resul.append("No se encuentra la columna: segundo_apellido\n")
                
                if (reg.get("sexo")):
                    if (reg['sexo'].upper()!='M' and reg['sexo'].upper()!='F' ):
                        resul.append("En la columna sexo, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: sexo\n" in resul ):
                        resul.append("No se encuentra la columna: sexo\n")
        
                if (reg.get("fecha_nacimiento")):
                    if not (type(reg['fecha_nacimiento'])==str):
                        resul.append("En la columna fecha_nacimiento, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: fecha_nacimiento\n" in resul ):
                        resul.append("No se encuentra la columna: fecha_nacimiento\n")       

                if (reg.get("etnia")):
                    if(reg['etnia']==""):
                        reg['etnia']= "NO EXITE" 
                    if not (type(reg['etnia'])==str):
                        resul.append("En la columna etnia, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: etnia\n" in resul ):
                        resul.append("No se encuentra la columna: etnia\n")
                
                if (reg.get("discapacidad")):
                    if(reg['discapacidad']==""):
                        reg['discapacidad']= "NO EXITE"
                    if not (type(reg['discapacidad'])==str):
                        resul.append("En la columna discapacidad, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: discapacidad\n" in resul ):
                        resul.append("No se encuentra la columna: discapacidad\n")
                
                if (reg.get("correo")):
                    if re.match('^[(A-Z0-9\_\-\.)]+@[(A-Z0-9\_\-\.)]+\.[(A-Z)]{2,15}$', reg['correo'].upper())==None:
                        resul.append("En la columna correo, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: correo\n" in resul ):
                        resul.append("No se encuentra la columna: correo\n")
                
                if (reg.get("tlf_local")):
                    if(reg['tlf_local']==""):
                        reg['tlf_local']= "0"
                    if not (reg['tlf_local'].isdigit()):
                        resul.append("En la columna tlf_local, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: tlf_local\n" in resul ):
                        resul.append("No se encuentra la columna: tlf_local\n")
                
                if (reg.get("tlf_celular")):
                    if not (reg['tlf_celular'].isdigit()):
                        resul.append("En la columna tlf_celular, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: tlf_celular\n" in resul ):
                        resul.append("No se encuentra la columna: tlf_celular\n")
                
                if (reg.get("edo_procedencia")):
                    if not (type(reg['edo_procedencia'])==str):
                        resul.append("En la columna edo_procedencia, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: edo_procedencia\n" in resul ):
                        resul.append("No se encuentra la columna: edo_procedencia\n")
                
                # if (reg.get("semestre_anno")):
                #     if (reg['semestre_anno'].upper()!='SEMESTRE' and reg['semestre_anno'].upper()!='ANNO'  ):
                #         resul.append("En la columna semestre_anno, fila '{}' hay un campo malo".format(cont))
                # else:
                #     if not ("No se encuentra la columna: semestre_anno\n" in resul ):
                #         resul.append("No se encuentra la columna: semestre_anno\n")
                
                if (reg.get("nro_semestr_anno")):
                    if not (reg['nro_semestr_anno'].isdigit()):
                        resul.append("En la columna nro_semestr_anno, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: nro_semestr_anno\n" in resul ):
                        resul.append("No se encuentra la columna: nro_semestr_anno\n")
                
                if (reg.get("nombre_carrera")):
                    if not (type(reg['nombre_carrera'])==str):
                        resul.append("En la columna nombre_carrera, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: nombre_carrera\n" in resul ):
                        resul.append("No se encuentra la columna: nombre_carrera\n")
                
                if (reg.get("estudio_adicional")):
                    if(reg['estudio_adicional']==""):
                        reg['estudio_adicional']= "NO EXITE"
                    if not (type(reg['estudio_adicional'])==str):
                        resul.append("En la columna estudio_adicional, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: estudio_adicional\n" in resul ):
                        resul.append("No se encuentra la columna: estudio_adicional\n")
                
                if (reg.get("nacionalidad")):
                    if not (type(reg['nacionalidad'])==str):
                        resul.append("En la columna nacionalidad, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: nacionalidad\n" in resul ):
                        resul.append("No se encuentra la columna: nacionalidad\n")
                
                if (reg.get("direccion_actual")):
                    if not (type(reg['direccion_actual'])==str):
                        resul.append("En la columna direccion_actual, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: direccion_actual\n" in resul ):
                        resul.append("No se encuentra la columna: direccion_actual\n")
                
                if(len (resul) == 0 ):
                        
                    try:
    
                        sqlquery = "insert into estudiante(tipo_estudio,nacionalidad,cedula,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,sexo,discapacidad,direccion_actual,telefono1,telefono2,etnia,email,edo_procedencia,fecha_nacimiento,estatus) VALUES ('1','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',1 )on conflict (cedula) do update set tipo_estudio = EXCLUDED.tipo_estudio, nacionalidad=EXCLUDED.nacionalidad, primer_nombre= EXCLUDED.primer_nombre ,segundo_nombre= EXCLUDED.segundo_nombre,primer_apellido=EXCLUDED.primer_apellido,segundo_apellido=EXCLUDED.segundo_apellido,sexo= EXCLUDED.sexo,discapacidad=EXCLUDED.discapacidad,direccion_actual= EXCLUDED.direccion_actual,telefono1=EXCLUDED.telefono1,etnia=EXCLUDED.etnia,email= EXCLUDED.email,edo_procedencia= EXCLUDED.edo_procedencia,fecha_nacimiento=EXCLUDED.fecha_nacimiento,estatus=EXCLUDED.estatus;" .format(reg['nacionalidad'].upper(),reg['a_ci'],reg['primer_nombre'].upper(),reg['segundo_nombre'].upper(),reg['primer_apellido'].upper(),reg['segundo_apellido'].upper(),
                        reg['sexo'].upper(),reg['discapacidad'].upper(),reg['direccion_actual'].upper(),reg['tlf_local'],reg['tlf_celular'],reg['etnia'].upper(),reg['correo'].upper(),
                        reg['edo_procedencia'].upper(),reg['fecha_nacimiento'])
                        cur.execute(sqlquery)

                        sqlquery2 = "insert into estudiante_carrera(id_carrera,id_estudiante) select (select id from carrera f where f.nombre='{}'),(select id from estudiante f where f.cedula='{}') ;".format(reg['nombre_carrera'].upper(),reg['a_ci'])
                        cur.execute(sqlquery2)

                        sqlquery3 = "insert into estatus_estudiante(codigo,estatus,id_estudiante,fecha_creacion,fecha_modificacion) select '{}','1', (select id from estudiante f where f.cedula='{}'), now(),now() on conflict (codigo) do update set estatus = EXCLUDED.estatus,id_estudiante = EXCLUDED.id_estudiante,fecha_creacion = EXCLUDED.fecha_creacion,fecha_modificacion = EXCLUDED.fecha_modificacion ;".format(reg['a_ci'],reg['a_ci'])
                        cur.execute(sqlquery3)

                        sqlquery4 = "insert into estudio_adicional(codigo,descripcion,id_estudiante,fecha_creacion,fecha_modificacion) select '{}','{}', (select id from estudiante f where f.cedula='{}'), now(),now() on conflict (codigo) do update set descripcion = EXCLUDED.descripcion,id_estudiante = EXCLUDED.id_estudiante,fecha_creacion = EXCLUDED.fecha_creacion,fecha_modificacion = EXCLUDED.fecha_modificacion ;".format(reg['a_ci'],reg['estudio_adicional'].upper(),reg['a_ci'])
                        cur.execute(sqlquery4)

                    except psycopg2.DatabaseError as e:
                        if conn:
                            conn.rollback()
                        print ('Error %s' % e) 
                        resul.append('Error %s' % e)   
                cont=cont+1
             else:
                 if not ("No tiene permitido insertar para esta carrera: {}\n".format(reg['nombre_carrera']) in resul ):
                    resul.append("No tiene permitido insertar para esta carrera: {}\n".format(reg['nombre_carrera']))
        else:
            my_lst_str = 'El orden de la(s) columna(s) debe ser: \n'
            i=0
            while (i<longitud_orden-1):
                my_lst_str=my_lst_str + orden_columna[i] + "-> " 
                i=i+1
            my_lst_str=my_lst_str + orden_columna[i]
            resul.append(my_lst_str)
            
    if(len (resul) == 0 ):
        # CONTENT_TYPE={"content-type": "application/json"}
        # print(user)
        data1={"username":user,"action": "Carga de archivo", "module": "Estudiantes"}
        r=requests.post("http://localhost:8084/api/v1/historyaction",data= json.dumps(data1)  )
        # print(r.status_code)

        if(r.status_code==requests.codes.ok):
            print("registro en auditoria")
        conn.commit()
    conn.close()
    cur.close()
    if(filename):
        os.remove(filename)
    return resul

def leer_Archivo_Post_Info_Estud(filename,user):
    
   
    with open(filename) as csvarchivo:
       
        entrada = csv.DictReader(csvarchivo,delimiter=';')
        cont=2
        resul=[]
        orden=entrada.fieldnames
        orden_columna=['a_ci','primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','sexo','fecha_nacimiento','etnia','discapacidad','correo','tlf_local','tlf_celular','edo_procedencia','nombre_carrera','instit_empres_trabaj','tlf_lugar_trabajo','estudio_adicional','nacionalidad','direccion_actual','titulo_universitario']
        longitud_orden= len(orden_columna)
        
        if(all(i == j for i, j in zip(orden,orden_columna))):    
            for reg in entrada:
             sqlquery10 = "select f.nombre from carrera_postgrado as c inner join facultad as f on (c.id_facultad=f.id) where c.nombre='{}';".format(reg['nombre_carrera'])
             cur.execute(sqlquery10)
             ressult=cur.fetchone()
             
             if((ressult and ressult[0]== user.upper()) or 'vicerrector'== user  ):
                
                if (reg.get("a_ci")):
                    if not (reg['a_ci'].isdigit()):
                        resul.append("En la columna a_ci, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: a_ci\n" in resul ):
                        resul.append("No se encuentra la columna: a_ci\n")
                
                if (reg.get("primer_nombre")):
                    if not (type(reg['primer_nombre'])==str):
                        resul.append("En la columna primer_nombre, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: primer_nombre" in resul ):
                        resul.append("No se encuentra la columna: primer_nombre")
                        
                if (reg.get("segundo_nombre")):
                    if(reg['segundo_nombre']==""):
                        reg['segundo_nombre']= "NO EXITE"
                    if not (type(reg['segundo_nombre'])==str):
                        resul.append("En la columna segundo_nombre , fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: segundo_nombre\n" in resul ):
                        resul.append("No se encuentra la columna: segundo_nombre\n")
            
                if (reg.get("primer_apellido")):
                    if not (type(reg['primer_apellido'])==str):
                        resul.append("En la columna primer_apellido, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: primer_apellido\n" in resul ):
                        resul.append("No se encuentra la columna: primer_apellido\n")

                if (reg.get("segundo_apellido")):
                    if(reg['segundo_apellido']==""):
                        reg['segundo_apellido']= "NO EXITE"            
                        if not (type(reg['segundo_apellido'])==str):
                            resul.append("En la columna segundo_apellido, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: segundo_apellido\n" in resul ):
                        resul.append("No se encuentra la columna: segundo_apellido\n")
                
                if (reg.get("sexo")):
                    if (reg['sexo'].upper()!='M' and reg['sexo'].upper()!='F' ):
                        resul.append("En la columna sexo, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: sexo\n" in resul ):
                        resul.append("No se encuentra la columna: sexo\n")
        
                if (reg.get("fecha_nacimiento")):
                    if not (type(reg['fecha_nacimiento'])==str):
                        resul.append("En la columna fecha_nacimiento, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: fecha_nacimiento\n" in resul ):
                        resul.append("No se encuentra la columna: fecha_nacimiento\n")       

                if (reg.get("etnia")):
                    if(reg['etnia']==""):
                        reg['etnia']= "NO EXITE" 
                    if not (type(reg['etnia'])==str):
                        resul.append("En la columna etnia, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: etnia\n" in resul ):
                        resul.append("No se encuentra la columna: etnia\n")
                
                if (reg.get("discapacidad")):
                    if(reg['discapacidad']==""):
                        reg['discapacidad']= "NO EXITE"
                    if not (type(reg['discapacidad'])==str):
                        resul.append("En la columna discapacidad, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: discapacidad\n" in resul ):
                        resul.append("No se encuentra la columna: discapacidad\n")
                
                if (reg.get("correo")):
                    if re.match('^[(A-Z0-9\_\-\.)]+@[(A-Z0-9\_\-\.)]+\.[(A-Z)]{2,15}$', reg['correo'].upper())==None:
                        resul.append("En la columna correo, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: correo\n" in resul ):
                        resul.append("No se encuentra la columna: correo\n")
                
                if (reg.get("tlf_local")):
                    if(reg['tlf_local']==""):
                        reg['tlf_local']= "0"
                    if not (reg['tlf_local'].isdigit()):
                        resul.append("En la columna tlf_local, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: tlf_local\n" in resul ):
                        resul.append("No se encuentra la columna: tlf_local\n")
                
                if (reg.get("tlf_celular")):
                    if not (reg['tlf_celular'].isdigit()):
                        resul.append("En la columna tlf_celular, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: tlf_celular\n" in resul ):
                        resul.append("No se encuentra la columna: tlf_celular\n")
                
                if (reg.get("edo_procedencia")):
                    if not (type(reg['edo_procedencia'])==str):
                        resul.append("En la columna edo_procedencia, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: edo_procedencia\n" in resul ):
                        resul.append("No se encuentra la columna: edo_procedencia\n")
                                
                if (reg.get("nombre_carrera")):
                    if not (type(reg['nombre_carrera'])==str):
                        resul.append("En la columna nombre_carrera, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: nombre_carrera\n" in resul ):
                        resul.append("No se encuentra la columna: nombre_carrera\n")

                if (reg.get("titulo_universitario")):
                    if not (type(reg['titulo_universitario'])==str):
                        resul.append("En la columna titulo_universitario, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: titulo_universitario\n" in resul ):
                        resul.append("No se encuentra la columna: titulo_universitario\n")
                
                if (reg.get("instit_empres_trabaj")):
                    if(reg['instit_empres_trabaj']==""):
                        reg['instit_empres_trabaj']= "NO EXITE"
                    if not (type(reg['instit_empres_trabaj'])==str):
                        resul.append("En la columna instit_empres_trabaj, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: instit_empres_trabaj\n" in resul ):
                        resul.append("No se encuentra la columna: instit_empres_trabaj\n")
                
                if (reg.get("tlf_lugar_trabajo")):
                    if(reg['tlf_lugar_trabajo']==""):
                        reg['tlf_lugar_trabajo']= "0"
                    if not (reg['tlf_lugar_trabajo'].isdigit()):
                        resul.append("En la columna tlf_lugar_trabajo, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: tlf_lugar_trabajo\n" in resul ):
                        resul.append("No se encuentra la columna: tlf_lugar_trabajo\n")
                
                if (reg.get("estudio_adicional")):
                    if(reg['estudio_adicional']==""):
                        reg['estudio_adicional']= "NO EXITE"
                    if not (type(reg['estudio_adicional'])==str):
                        resul.append("En la columna estudio_adicional, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: estudio_adicional\n" in resul ):
                        resul.append("No se encuentra la columna: estudio_adicional\n")
                
                if (reg.get("nacionalidad")):
                    if not (type(reg['nacionalidad'])==str):
                        resul.append("En la columna nacionalidad, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: nacionalidad\n" in resul ):
                        resul.append("No se encuentra la columna: nacionalidad\n")
                
                if (reg.get("direccion_actual")):
                    if not (type(reg['direccion_actual'])==str):
                        resul.append("En la columna direccion_actual, fila '{}' hay un campo malo".format(cont))
                else:
                    if not ("No se encuentra la columna: direccion_actual\n" in resul ):
                        resul.append("No se encuentra la columna: direccion_actual\n")
                
                if(len (resul) == 0 ):
                        
                    try:
    
                        sqlquery = "insert into estudiante_postgrado(tipo_estudio,nacionalidad,cedula,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,sexo,discapacidad,direccion_actual,telefono1,telefono2,etnia,email,edo_procedencia,fecha_nacimiento,estatus) VALUES ('0','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',1 )on conflict (cedula) do update set tipo_estudio = EXCLUDED.tipo_estudio, nacionalidad=EXCLUDED.nacionalidad, primer_nombre= EXCLUDED.primer_nombre ,segundo_nombre= EXCLUDED.segundo_nombre,primer_apellido=EXCLUDED.primer_apellido,segundo_apellido=EXCLUDED.segundo_apellido,sexo= EXCLUDED.sexo,discapacidad=EXCLUDED.discapacidad,direccion_actual= EXCLUDED.direccion_actual,telefono1=EXCLUDED.telefono1,etnia=EXCLUDED.etnia,email= EXCLUDED.email,edo_procedencia= EXCLUDED.edo_procedencia,fecha_nacimiento=EXCLUDED.fecha_nacimiento,estatus=EXCLUDED.estatus;" .format(reg['nacionalidad'].upper(),reg['a_ci'],reg['primer_nombre'].upper(),reg['segundo_nombre'].upper(),reg['primer_apellido'].upper(),reg['segundo_apellido'].upper(),
                        reg['sexo'].upper(),reg['discapacidad'].upper(),reg['direccion_actual'].upper(),reg['tlf_local'],reg['tlf_celular'],reg['etnia'].upper(),reg['correo'].upper(),
                        reg['edo_procedencia'].upper(),reg['fecha_nacimiento'])
                        cur.execute(sqlquery)

                        sqlquery2 = "insert into estudiante_carrera_postgrado(id_carrera,id_estudiante,titulo_universitario,instit_empres_trabaj,tlf_lugar_trabajo) select (select id from carrera_postgrado f where f.nombre='{}'),(select id from estudiante_postgrado f where f.cedula='{}'),'{}','{}','{}' ;".format(reg['nombre_carrera'].upper(),reg['a_ci'],reg['titulo_universitario'].upper(),reg['instit_empres_trabaj'].upper(),reg['tlf_lugar_trabajo'])
                        cur.execute(sqlquery2)


                        sqlquery3 = "insert into estatus_estudiante_postgrado(codigo,estatus,id_estudiante,fecha_creacion,fecha_modificacion) select '{}','1', (select id from estudiante_postgrado f where f.cedula='{}'), now(),now() on conflict (codigo) do update set estatus = EXCLUDED.estatus,id_estudiante = EXCLUDED.id_estudiante,fecha_creacion = EXCLUDED.fecha_creacion,fecha_modificacion = EXCLUDED.fecha_modificacion ;".format(reg['a_ci'],reg['a_ci'])
                        cur.execute(sqlquery3)

                        sqlquery4 = "insert into estudio_adicional_postgrado(codigo,descripcion,id_estudiante,fecha_creacion,fecha_modificacion) select '{}','{}', (select id from estudiante_postgrado f where f.cedula='{}'), now(),now() on conflict (codigo) do update set descripcion = EXCLUDED.descripcion,id_estudiante = EXCLUDED.id_estudiante,fecha_creacion = EXCLUDED.fecha_creacion,fecha_modificacion = EXCLUDED.fecha_modificacion ;".format(reg['a_ci'],reg['estudio_adicional'].upper(),reg['a_ci'])
                        cur.execute(sqlquery4)

                    except psycopg2.DatabaseError as e:
                        if conn:
                            conn.rollback()
                        print ('Error %s' % e) 
                        resul.append('Error %s' % e)   
                cont=cont+1
             else:
                if not ("No tiene permitido insertar para esta carrera: {}\n".format(reg['nombre_carrera']) in resul ):
                    resul.append("No tiene permitido insertar para esta carrera: {}\n".format(reg['nombre_carrera']))
            
        else:
            my_lst_str = 'El orden de la(s) columna(s) debe ser: \n'
            i=0
            while (i<longitud_orden-1):
                my_lst_str=my_lst_str + orden_columna[i] + "-> " 
                i=i+1
            my_lst_str=my_lst_str + orden_columna[i]
            resul.append(my_lst_str)
            
    if(len (resul) == 0 ):
        data1={"username":user,"action": "Carga de archivo", "module": "Estudiantes"}
        r=requests.post("http://localhost:8084/api/v1/historyaction",data= json.dumps(data1)  )
        if(r.status_code==requests.codes.ok):
            print("registro en auditoria")
        conn.commit()
    conn.close()
    cur.close()
    if(filename):
        os.remove(filename)
    return resul
    
def fecha_tope_pregrado(user):

    sqlquery = "select c.fecha_tope from fecha_tope_pregrado as c inner join facultad as f on (c.id_facultad=f.id) where f.nombre='{}';".format(user)
    cur.execute(sqlquery)
    ressult=cur.fetchone()
    res=str(ressult[0])
    res=res[0:10]
 
    return json.dumps({"exitosa": res}), 201, { 'Access-Control-Allow-Origin': '*' }

def fecha_tope_postgrado(user):

    sqlquery = "select c.fecha_tope from fecha_tope_postgrado as c inner join facultad as f on (c.id_facultad=f.id) where f.nombre='{}';".format(user)
    cur.execute(sqlquery)
    ressult=cur.fetchone()
    res=str(ressult[0])
    res=res[0:10]
    return json.dumps({"exitosa": res}), 201, { 'Access-Control-Allow-Origin': '*' }

class fecha_tope(Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    def post(self,id,user):
        lectura=[]
        if(id=='11'):
            lectura=fecha_tope_pregrado(user)
        if(id=='21'):
            lectura=fecha_tope_postgrado(user)
        return json.dumps({'exitosa':lectura}), 201, { 'Access-Control-Allow-Origin': '*' }

class fecha_tope_vicerrector(Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    def post(self):
        sqlquery = "select c.fecha_tope,f.nombre from fecha_tope_pregrado as c inner join facultad as f on (c.id_facultad=f.id) ;"
        cur.execute(sqlquery)
        resultStudent=list(cur)
        sqlquery = "select c.fecha_tope,f.nombre from fecha_tope_postgrado as c inner join facultad as f on (c.id_facultad=f.id) ;"
        cur.execute(sqlquery)
        resultStudent.append(list(cur))
        return json.dumps(resultStudent, default=str), 201, { 'Access-Control-Allow-Origin': '*' } 

class actualizar_fechas_vicerrector(Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    
    def post(self,facyt_pre,faces_pre,face_pre,fcjp_pre,ingenieria_pre,fcs_pre,odontologia_pre,facyt_post,faces_post,face_post,fcjp_post,ingenieria_post,fcs_post,odontologia_post): #pendiente get post
            resul=[]
            try:
                fe=facyt_pre.split('-')
                facyt_pre=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_pregrado set fecha_tope= '{}',estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(facyt_pre,'FACYT')
                cur.execute(sqlquery)

                fe=faces_pre.split('-')
                faces_pre=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_pregrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(faces_pre,'FACES')
                cur.execute(sqlquery)

                fe=face_pre.split('-')
                face_pre=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_pregrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(face_pre,'FACE')
                cur.execute(sqlquery)

                fe=fcjp_pre.split('-')
                fcjp_pre=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_pregrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(fcjp_pre,'FCJP')
                cur.execute(sqlquery)

                fe=ingenieria_pre.split('-')
                ingenieria_pre=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_pregrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(ingenieria_pre,'INGENIERIA')
                cur.execute(sqlquery)

                fe=fcs_pre.split('-')
                fcs_pre=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_pregrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(fcs_pre,'FCS')
                cur.execute(sqlquery)

                fe=odontologia_pre.split('-')
                odontologia_pre=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_pregrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(odontologia_pre,'ODONTOLOGIA')
                cur.execute(sqlquery)


                fe=facyt_post.split('-')
                facyt_post=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_postgrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(facyt_post,'FACYT')
                cur.execute(sqlquery)

                fe=faces_post.split('-')
                faces_post=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_postgrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(faces_post,'FACES')
                cur.execute(sqlquery)

                fe=face_post.split('-')
                face_post=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_postgrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(face_post,'FACE')
                cur.execute(sqlquery)

                fe=fcjp_post.split('-')
                fcjp_post=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_postgrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(fcjp_post,'FCJP')
                cur.execute(sqlquery)

                fe=ingenieria_post.split('-')
                ingenieria_post=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_postgrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(ingenieria_post,'INGENIERIA')
                cur.execute(sqlquery)

                fe=fcs_post.split('-')
                fcs_post=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_postgrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(fcs_post,'FCS')
                cur.execute(sqlquery)

                fe=odontologia_post.split('-')
                odontologia_post=datetime(int(fe[0]),int(fe[1]),int(fe[2]), 0, 0)
                sqlquery = "update fecha_tope_postgrado set fecha_tope= '{}', estatus='1' where id_facultad =  (select id from facultad f where f.nombre='{}');".format(odontologia_post,'ODONTOLOGIA')
                cur.execute(sqlquery)
                
                
                conn.commit()
                resul.append("exito")
            except psycopg2.DatabaseError as e:
                resul.append(e)
                resul
                if conn:
                    conn.rollback()
            return json.dumps(resul, default=str), 201, { 'Access-Control-Allow-Origin': '*' }                        



api.add_resource(fecha_tope, '/fecha_tope/<string:id>/<user>')
api.add_resource(fecha_tope_vicerrector, '/fechasvicerrector')
api.add_resource(actualizar_fechas_vicerrector, '/insertarfecha/<string:facyt_pre>/<string:faces_pre>/<string:face_pre>/<string:fcjp_pre>/<string:ingenieria_pre>/<string:fcs_pre>/<string:odontologia_pre>/<string:facyt_post>/<string:faces_post>/<string:face_post>/<string:fcjp_post>/<string:ingenieria_post>/<string:fcs_post>/<string:odontologia_post>')
api.add_resource(StudentInsertInitial, '/estudiantes')
api.add_resource(StudentUpdate, '/estudiantes/<date_update>')
api.add_resource(File, '/upload/<string:id>/<user>')
# api.add_resource(Api_1,'/api/v1/estudiantes')
# api.add_resource(Api_2,'/api/v1/estudiantes/<fecha_actualiazacion>')




if __name__ == '__main__':
    app.run(debug=True, port=int('8082'))



# def party_time2():
#     """funcion que realiza el trabajo en el thread"""
#     print ('hola1')

#     return


# def party_time():
#     """funcion que realiza el trabajo en el thread"""
#     print ('Estoy trabajando para Genbeta Dev')
#     t = Timer(5.0, party_time2)
#     t.start()
#     return

# def afunc(number):
#     print ("holaa")

# def activate_job():
#     def run_job():
#         while True:
#             print("Run recurring task")
#             time.sleep(3)

#     thread = threading.Thread(target=run_job)
#     thread.start()

# def flaskThread():
#     app.run(debug=True, port=int('8082'),threaded=True)

    # t = Timer(5, party_time, args=None, kwargs=None)
    # threads = list()
    # t = threading.Thread(target=party_time)
    # threads.append(t)
    # t.start()
    # t = threading.Thread(target=app.run(debug=True, port=int('8082'),threaded=True))
    # threads.append(t)

# threads = list()
# for i in range(3):
#     t = threading.Thread(target=worker)
#     threads.append(t)
#     t.start()

#     t = Timer(5.0, party_time)
#     t.start()
#     app.run(debug=True, port=int('8082'),threaded=True)
#     # process = Thread(target=crawl, args=[urls[ii], result, ii])
    # process.start()
    # threads.append(process)
    # Thread.start_new_thread(flaskThread,())
    # t = worker(target=afunc, args=(4,))
    # app.run(t.start())
    # t = worker(target=afunc, args=(4,))





# class DateTimeDecoder(json.JSONDecoder):

#     def __init__(self, *args, **kargs):
#         JSONDecoder.__init__(self, object_hook=self.dict_to_object,
#                              *args, **kargs)
    
#     def dict_to_object(self, d): 
#         if '__type__' not in d:
#             return d

#         type = d.pop('__type__')
#         try:
#             dateobj = datetime(**d)
#             return dateobj
#         except:
#             d['__type__'] = type
#             return d

# class RoundTripDecoder(json.JSONDecoder):
#     def __init__(self, *args, **kwargs):
#         json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

#     def object_hook(self, obj):
#         if '_type' not in obj:
#             return obj
#         type = obj['_type']
#         if type == 'datetime':
#             return {
                
#                 'anno' : obj.year,
#                 'mes' : obj.month,
#                 'dia' : obj.day,
#             } 
#         return obj

# class JSONDebugEncoder(json.JSONEncoder):
#     # transform objects known to JSONEncoder here
#     def encode(self, o, *args, **kw):
#         for_json = o
#         if isinstance(o, mDict):
#             for_json = { 'orig' : o, 'attrs' : vars(o) }
#         elif isinstance(o, mList):
#             for_json = { 'orig' : o, 'attrs' : vars(o) }
#         return super(JSONDebugEncoder, self).encode(for_json, *args, **kw)

#     # handle objects not known to JSONEncoder here
#     def default(self, o, *args, **kw):
#         if isinstance(o, datetime):
#             return o.isoformat()
#         else:
#             return super(JSONDebugEncoder, self).default(o, *args, **kw)


# class mDict(dict):
#     pass

# class mList(list):
#     pass

# class DateTimeEncoder(JSONEncoder):
#     representations = {'application/json': make_response}
#     parser = reqparse.RequestParser()
#     def default(self, o):
#         if isinstance(o, datetime):
#             return {
                
#                 'anno' : o.year,
#                 'mes' : o.month,
#                 'dia' : o.day,
#             }   
#         else:
#             return JSONEncoder.default(self, o)

    # var obj = {
    #   foo: 'foo',
    #   toJSON: function () {
    #     return 'bar';
    #   }
    # };
    # var json = JSON.stringify({x: obj}); // '{"x":"bar"}'.

# for i in xrange(n):
#     for j in xrange(n):
#         print A[i][j],
#     print
# print
        # print(studentList[0][0])
        # print(studentList[1][0])
        # print(list(cur))
        # i=0;
        # for (i=0; i<len(studentList) ; i=i+1):
        #     studentList[i][0]=studentList[i][0].strftime('%Y-%m-%d')
        
        # for row in studentList:
        #         row[0] = row[0].strftime('%Y-%m-%d')
        # #         print(row)
        #         studentList.append(row)
        # i=0
        # while(i<len(studentList)):
        #     studentList[i][0]=studentList[i][0].date()
        #     # row[0] = row[0].strftime('%Y-%m-%d')
        #     studentList.append(studentList[i][0])
        #     i=i+1
        # for row in resultStudent:
        #     print(row[0])
        #     # row['fecha_tope'] = row['fecha_tope'].intftime('%Y-%m-%d')
        #     studentList.append(row)
        # resultStudent = studentList
        # # resultStudent = studentList
        # print( json.stringify({x: studentList}))
   

# def default(o):
#     if type(o) is datetime.date or type(o) is datetime:
#         return o.isoformat()
# def dump_date(thing):
#     if isinstance(thing, datetime):
#         return thing.isoformat()
#     return str(thing)

# class Api_1(Resource):
#        orden_columna=['a_ci','primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','sexo','fecha_nacimiento','etnia','discapacidad','correo','tlf_local','tlf_celular','edo_procedencia','nro_semestr_anno','nombre_carrera','estudio_adicional','nacionalidad','direccion_actual']
     
# #     representations = {'application/json': make_response}
# #     parser = reqparse.RequestParser()

# #     def post(self):
# #         print("entrooooo")
# #         PSQL_HOST = "localhost"
# #         PSQL_PORT = "5432"
# #         PSQL_USER = "postgres"
# #         PSQL_PASS = "0000"
# #         PSQL_DB   = "estudiante"
# #         connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
# #         conn = psycopg2.connect(connstr)
# #         cur = conn.cursor()
# #         cur.execute("select e.cedula, c.nombre as nombre_carrera, f.nombre  from estudiante as e inner join estudiante_carrera as e_c on e.id=e_c.id_estudiante inner join carrera as c on e_c.id_carrera=c.id inner join  facultad as f  on c.id_facultad=f.id ;")
# #         Resultstudent=[]
# #         Resultstudent=cur.fetchall()
        
# #         cur.execute("select nombre  from facultad;")
# #         Facultades=[]
# #         Facultades=cur.fetchall()
        
        
# #         cur.execute("select nombre,tipo_semestr_anno from carrera;")
# #         Carreras=[]
# #         Carreras=cur.fetchall()
        
# #         cur.execute("select fecha_nacimiento,cedula,nacionalidad,primer_nombre,primer_apellido,sexo,telefono1,telefono2,email,edo_procedencia,etnia,discapacidad,estatus,tipo_estudio  from estudiante;")
# #         Estudent=[]
# # #         # Estudent=cur.fetchall()
# # #         for row in cur.fetchall():
# # #             Estudent.append(dict(zip(orden_columna, row)))

# # #         # for reg in Estudent:
# # #         #     # print (datetime.strptime(reg[0], '%Y-%m-%d').date())
# # #         #     reg[0]=str( reg[0] )
        
# # #         # lista = [1, 2, 3, 4, 5]

# # #         # for indice in range(len(lista)):
# # #         #     lista[indice] = lista[indice] * lista[indice]
# # #         #     print(lista[indice])

# # #         # print(reg[0])

# # #         # for indice in range(len(Estudent)):
# # #         #     Estudent[indice][0]= str (Estudent[indice][0] )   
# # #             # print(reg[0].date())     
# # #         # print( Estudent[0][1])
# # #         # print( Estudent[0])
# # # # __str__( )
# # #         # print( datetime.strptime(Estudent, '%b %d %Y %I:%M%p'))
# # #         cur.execute("select fecha_nacimiento,cedula,nacionalidad,primer_nombre,primer_apellido,sexo,telefono1,telefono2,email,edo_procedencia,etnia,discapacidad,estatus,tipo_estudio from estudiante_postgrado;")
# # #         for row in cur.fetchall():
# # #             Estudent.append(dict(zip(orden_columna, row)))

# # #         # Estudent.append(dict(zip(columns, row)) cur.fetchall())
        
# #         # response={
# #         #     "dim-facultad":{"items": Facultades },
# #         #         "dim-carrera": {"items": Carreras },
                
# #         #         "hechos-estudiantes-carreras-facultad": {"items": Resultstudent},
# #         #         "dim-estudiante": {"items": Estudent }
                
# #         # }
# #         # print(Estudent)
# #         # print("-------------------------------------")
# #         # print(Facultades)
# #         print(json.dumps(response,  default=dump_date), 201, { 'Access-Control-Allow-Origin': '*' })
# #         return json.dumps(response, default=dump_date), 201, { 'Access-Control-Allow-Origin': '*' }

#   # for row in cur: # itero sober cada fila
#         #     # row es un diccionario, con las claves = nombres de campos
#         #     print ("Nombre, carrera, facultad: %s, %s,%s"  % (row['cedula'],row['nombre_carrera'],row['nombre']))
#         #     data['estudiante']= row['cedula']
#         #     data['carrera']= row['nombre_carrera']
#         #     data['facultad']= row['nombre']
#         #     Resultstudent
            

#         # JSON = {
#         #     data['estudiante']= row['cedula']
#         #     data['carrera']= row['nombre_carrera']
#         #     data['facultad']= row['nombre']
#         # }

#         # data_string = json.dumps(data)
#         # print ('JSON:', data_string)   
#             #data = {"hechos-estudiante-carrera-facultad": [  {"Fruta":   [    {"Nombre":"Manzana","Cantidad":10},    {"Nombre":"Pera","Cantidad":20},    {"Nombre":"Naranja","Cantidad":30}   ]  },  {"Verdura":   [    {"Nombre":"Lechuga","Cantidad":80},    {"Nombre":"Tomate","Cantidad":15},    {"Nombre":"Pepino","Cantidad":50}   ]  } ]}

#         #Nos imprime en pantalla data como un tipo de dato nativo.
#         # print ('DATA:', repr(data))

#         #Nos devuelve el String con el JSON
        
# # class Api_2():
# #     PSQL_HOST = "localhost"
# #     PSQL_PORT = "5432"
# #     PSQL_USER = "postgres"
# #     PSQL_PASS = "0000"
# #     PSQL_DB   = "estudiante"
# #     connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
# #     conn = psycopg2.connect(connstr)
# #     representations = {'application/json': make_response}
# #     parser = reqparse.RequestParser() 

# # estudiantes route
