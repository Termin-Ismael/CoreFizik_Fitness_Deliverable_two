from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

app = Flask(__name__)

app.secret_key = 'termin123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '213ll1$M@'
app.config['MYSQL_DB'] = 'corefizik_fitness'

mysql = MYSQL(app)

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg=''
    return render_template('index.html', msg='')