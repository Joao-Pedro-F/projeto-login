from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.secret_key = os.urandom(24) 

bcrypt = Bcrypt(app)

# Configuração do MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

# Rota inicial de teste
@app.route("/")
def home():
    return "Servidor Flask funcionando!"

#rota cadastro
@app.route("/cadastro_form")
def cadastro_form():
    return render_template("cadastro.html")  # formulário de cadastro

@app.route("/register", methods=["POST"])
def register():
    # aceita JSON ou form-data
    data = request.get_json(silent=True) or request.form or {}
    nome = data.get("nome")
    email = data.get("email")
    password = data.get("password") or data.get("senha")

    if not nome or not email or not password:
        return jsonify({"error": "nome, email e senha são obrigatórios."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (nome, email, password) VALUES (%s, %s, %s)",
            (nome, email, hashed_password)
        )
        mysql.connection.commit()
    except Exception as e:
        if mysql.connection:
            mysql.connection.rollback()
        return jsonify({"error": "Falha ao cadastrar usuário.", "detail": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

#rota login
@app.route("/login")
def login_form():
    return render_template("login.html")  # formulário de login

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or request.form or {}
    email = data.get("email")
    password = data.get("password") or data.get("senha")

    if not email or not password:
        return jsonify({"error": "email e senha são obrigatórios."}), 400

    cursor = None
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nome, email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        user_id, nome, user_email, hashed_password = user
        if not bcrypt.check_password_hash(hashed_password, password):
            return jsonify({"error": "Senha incorreta."}), 401

        # Login bem-sucedido, salvando na sessão
        session["user_id"] = user_id
        session["user_nome"] = nome
        return jsonify({"message": f"Bem-vindo {nome}!"}), 200
    finally:
        if cursor:
            cursor.close()

#rota sair(logout)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)