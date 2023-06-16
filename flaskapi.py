import os
from crypt import methods
from distutils.log import debug
from flask import jsonify, request, Flask, render_template, session,redirect, flash,url_for
from flaskext.mysql import MySQL

id = 0

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


def obtener_productos(resp):
    # Aquí iría tu lógica para obtener la lista de productos de la base de datos
    # o de alguna otra fuente de datos
    
    # Por ahora, simplemente devolvemos una lista de ejemplo

    list_json = []
    for e in resp.json:
        dict_json = {}
        dict_json["id"] = e[0]
        dict_json["nombre"] = e[1]
        dict_json["precio"] = e[2]
        dict_json["descripcion"] = e[3]
        dict_json["imagen"] = e[4]
        list_json.append(dict_json)
    return list_json

def obtener_producto_por_id(rows):
    # Aquí iría tu lógica para obtener el producto de la base de datos
    # o de alguna otra fuente de datos en función del ID proporcionado
    
    # Por ahora, simplemente devolvemos un diccionario de ejemplo

    list_json = []
    counter = 1 
    for e in rows:
        dict_json = {}
        dict_json["id"] = e[2]
        dict_json["nombre"] = e[6]
        dict_json["precio"] = e[7]
        dict_json["descripcion"] = e[8]
        dict_json["imagen"] = e[9]
        list_json.append(dict_json)
        #list_json[counter] = dict_json
        #counter += 1
    
    return list_json

def redirect(url):
    # Redireccionar a la URL proporcionada
    return redirect(url)

@app.route("/index")
def reindex():
    index()

@app.route("/")
def index():
    global id
    """Function to test the functionality of the API"""

    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select count(*) from flaskapi.TRANSACCION where status='active'")
        row = cursor.fetchone()

        resp = jsonify(row)
        resp.status_code = 200

        if row[0] == 0:
            sql = "INSERT INTO flaskapi.TRANSACCION(status) " \
              "VALUES(%s)"
            
            data = ("active")
            
            cursor.execute(sql, data)
            conn.commit()

        cursor.execute("select TRANSACCION_ID from flaskapi.TRANSACCION where status='active'")
        row = cursor.fetchone()

        id = row[0]
        
        cursor.close()
        conn.close()
        
        return render_template("index2.html")
    
    except Exception as exception:
        return jsonify(str(exception))




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
        cursor.execute("SELECT * FROM flaskapi.PRODUCTO")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200

        productos = obtener_productos(resp)

        return render_template("productos2.html", productos=productos)
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
    global id
    """Función para el proceso de finalización de compra"""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        address = request.form["address"]

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "UPDATE TRANSACCION SET nombre = %s, direccion = %s, email = %s, status = %s where transaccion_id = %s"
        data = (name,address,email,"terminated",id)

        cursor.execute(sql, data)
        conn.commit()

        # Agrega aquí la lógica para procesar los datos del formulario

        cursor.close()
        conn.close()


        return render_template("modal_checkout.html",total = 0)



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
    global id
    producto_id = request.form.get("producto_id")
    precio = request.form.get("precio")
    if producto_id:

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "INSERT INTO flaskapi.PRODUCTO_TRANSACCION(transaccion_id, producto_id,cantidad,total) " \
              "VALUES(%s,%s,%s,%s)"
            
        data = (id,producto_id,1,precio)
            
        cursor.execute(sql, data)
        conn.commit()

        cursor.close()
        conn.close()


    return render_template("modal.html")#redirect(url_for("productos"))

@app.route("/carrito", methods=["GET"])
def carrito():
    global id
    #productos_carrito = [obtener_producto_por_id(id) for id in lista_carrito]

    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "select * from flaskapi.PRODUCTO_TRANSACCION a " \
          "left join flaskapi.PRODUCTO b on a.producto_id = b.producto_id where transaccion_id = %s"
    data = (id)

    cursor.execute(sql, data)
    rows = cursor.fetchall()

    productos = obtener_producto_por_id(rows)

    suma = sum(item['precio'] for item in productos)

    cursor.close()
    conn.close()

    return render_template("carrito2.html", productos_carrito=productos, total=suma)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
