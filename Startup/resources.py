import os
import json
from flask import request, abort, render_template, redirect, url_for
from flask.ext import restful
from flask.ext.restful import reqparse
from Startup import app, api
from bson.objectid import ObjectId
# import psycopg2
import urlparse
import requests
import sqlite3

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

from jinja2 import Environment, PackageLoader, FileSystemLoader
env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)


@app.route('/')
def show_main():   


    template = env.get_template('templates/index.html')
    return render_template(template)

class Status(restful.Resource):
    def get(self):
        return {
            'status': 'OK'
            # 'mongo': str(mongo.db),
        }

class Metodos(restful.Resource):
    def get(self):
        return [
            1,2,3,4
        ]
        

class Comments(restful.Resource):
    def get(self):

        conn = sqlite3.connect('Comments')
        cur = conn.cursor()

        cur.execute("SELECT * FROM comment")

        r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]

        conn.close()
        return r

    def post(self):

        conn = sqlite3.connect('Comments')
        cur = conn.cursor()

        text = request.form["text"]
        author = request.form["author"]

        # cur.execute("INSERT INTO salas VALUES (%(idSala)s,%(nombre)s,%(minutos)s,%(ubicacion)s,%(idAc)s);",{ 'idSala' : idSala, 'nombre' : sala["sala"], 'minutos' : sala["minutos"], 'ubicacion' : sala["ubicacion"], 'idAc' : idAc })
        cur.execute("INSERT INTO comment values (?,?)",(author,text))
        conn.commit()

        conn.close()
        return {
            "status" : "ok"
        }

@app.route('/recetaSimple')
def receta_Simple():   


    template = env.get_template('templates/RecetasSimples.html')
    return render_template(template)

api.add_resource(Status, '/status')
api.add_resource(Metodos, '/metodos')
api.add_resource(Comments, '/comments')
# api.add_resource(Reading, '/readings/<ObjectId:reading_id>')