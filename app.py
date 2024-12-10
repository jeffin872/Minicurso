#Importações
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Instanciação do flask e do banco de dados
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
