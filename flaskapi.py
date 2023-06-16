import os
from crypt import methods
from distutils.log import debug
from flask import jsonify, request, Flask, render_template, session,redirect, flash,url_for
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'supersecretkey'
mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
mysql.init_app(app)


def obtener_productos():
    # Aquí iría tu lógica para obtener la lista de productos de la base de datos
    # o de alguna otra fuente de datos
    
    # Por ahora, simplemente devolvemos una lista de ejemplo
    productos = [
        {
            "id": "1",
            "nombre": "Producto 1",
            "descripcion": "Descripción del producto 1",
            "precio": 10.99
        },
        {
            "id": "2",
            "nombre": "Producto 2",
            "descripcion": "Descripción del producto 2",
            "precio": 19.99
        },
        {
            "id": "3",
            "nombre": "Producto 3",
            "descripcion": "Descripción del producto 3",
            "precio": 15.99
        }
    ]

    return productos

def obtener_producto_por_id(producto_id):
    # Aquí iría tu lógica para obtener el producto de la base de datos
    # o de alguna otra fuente de datos en función del ID proporcionado
    
    # Por ahora, simplemente devolvemos un diccionario de ejemplo
    productos = {
        "1": {
            "id": "1",
            "nombre": "Producto 1",
            "descripcion": "Descripción del producto 1",
            "precio": 10.99
        },
        "2": {
            "id": "2",
            "nombre": "Producto 2",
            "descripcion": "Descripción del producto 2",
            "precio": 19.99
        },
        "3": {
            "id": "3",
            "nombre": "Producto 3",
            "descripcion": "Descripción del producto 3",
            "precio": 15.99
        }
    }

    return productos.get(producto_id)

def redirect(url):
    # Redireccionar a la URL proporcionada
    return redirect(url)


@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return render_template("index2.html")


@app.route("/create", methods=["POST"])
def add_user():
    """Function to create a user to the MySQL database"""
    json = request.json
    name = json["name"]
    email = json["email"]
    pwd = json["pwd"]
    if name and email and pwd and request.method == "POST":
        sql = "INSERT INTO users(user_name, user_email, user_password) " \
              "VALUES(%s, %s, %s)"
        data = (name, email, pwd)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("User created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide name, email and pwd")


@app.route("/users", methods=["GET"])
def users():
    """Function to retrieve all users from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/user/<int:user_id>", methods=["GET"])
def user(user_id):
    """Function to get information of a specific user in the MSQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=%s", user_id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/update", methods=["POST"])
def update_user():
    """Function to update a user in the MYSQL database"""
    json = request.json
    name = json["name"]
    email = json["email"]
    pwd = json["pwd"]
    user_id = json["user_id"]
    if name and email and pwd and user_id and request.method == "POST":
        # save edits
        sql = "UPDATE users SET user_name=%s, user_email=%s, " \
              "user_password=%s WHERE user_id=%s"
        data = (name, email, pwd, user_id)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("User updated successfully!")
            resp.status_code = 200
            cursor.close()
            conn.close()
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide id, name, email and pwd")


@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    """Function to delete a user from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=%s", user_id)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify("User deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))

@app.route("/productos")
def productos():
    """Function to handle the '/productos' route"""
    # Agrega el código para manejar la lógica de la página de productos
    # return render_template("productos.html")
    
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PRODUCTO")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        productos = resp
        resp.status_code = 200
        render_template("productos2.html", productos=productos)
    except Exception as exception:
        return jsonify(str(exception))
    
    #productos = obtener_productos()  # Función para obtener la lista de productos
    #return render_template("productos2.html", productos=productos)

# @app.route("/carrito")
# def carrito():
#     """Function to handle the '/carrito' route"""
#     # Agrega el código para manejar la lógica de la página de carrito
#     return render_template("carrito.html")

@app.route("/checkout", methods=["GET","POST"])
def checkout():
    """Función para el proceso de finalización de compra"""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        address = request.form["address"]

        # Agrega aquí la lógica para procesar los datos del formulario

        return "¡Gracias por tu compra!"

    return render_template("checkout.html")



# @app.route("/carrito")
# def carrito():
#     carrito = session.get("carrito", [])

#     return render_template("carrito.html", carrito=carrito)


# @app.route("/add_to_cart", methods=["POST"])
# def add_to_cart():
#     producto_id = request.form.get("producto_id")
#     producto = obtener_producto_por_id(producto_id)

#     if producto:
#         # Aquí iría tu lógica para agregar el producto al carrito
#         # Por ahora, simplemente almacenaremos el producto en una lista en memoria
#         carrito.append(producto)
#         return redirect("/carrito")
#     else:
#         flash("El producto no existe")
#         return redirect("/productos")
    
lista_carrito = []

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    producto_id = request.form.get("producto_id")
    if producto_id:
        lista_carrito.append(producto_id)
    return render_template("modal.html")#redirect(url_for("productos"))

@app.route("/carrito", methods=["GET"])
def carrito():
    productos_carrito = [obtener_producto_por_id(id) for id in lista_carrito]
    return render_template("carrito2.html", productos_carrito=productos_carrito)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
