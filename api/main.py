from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL  # importando la libreria de mysql 
# instalar pip install Flask-Cors y pip install flask-mysqldb  - pip install flask        
from flask_cors import CORS, cross_origin
app = Flask(__name__) # instancia de flask  __name__ nombre del modulo al q se esta llamndo --
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'  # loclahost de mi bd
app.config['MYSQL_USER'] = 'root' # root o el que tienen ustedes
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'system'  # el nombre de mi base de datos de donde se jalaron los datos para trabajarlos
mysql = MySQL(app)  # instanciar Mysql atravez de la variable mysql
@app.route('/api/customers')   # para manejar el enrutamiento 
@cross_origin() #  permites solicitudes desde cualquier origen. Puedes ajustar la configuración de CORS según tus necesidades, especificando orígenes permitidos, encabezados personalizados, etc.
def getAllCustomers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, firstname, lastname, email, phone, address FROM customers')
    data = cur.fetchall() # en combinacion de un objeto cursor de una conexion de bd para recuperar todas los resultados de una consulta SQL : fetchall se utiliza para obtener todos estos resultados de una vez y devolverlos como listas y tuplas donde cada tupla representa una fila de resultados 
    result = []
    for row in data:
        content = {
                'id':row[0],
                'firstname': row[1],
                'lastname': row[2],
                'email': row[3],
                'phone': row[4],
                'address': row[5]
            }
        result.append(content)
    return jsonify(result)
@app.route('/api/customers/<int:id>')
@cross_origin()
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, firstname, lastname, email, phone, address FROM customers WHERE id = ' + str(id))
    data = cur.fetchall()
    content = {}
    for row in data:
        content = {
                'id':row[0],
                'firstname': row[1],
                'lastname': row[2],
                'email': row[3],
                'phone': row[4],
                'address': row[5]
            }
    return jsonify(content)
@app.route('/api/customers', methods=['POST'])
@cross_origin()
def createCustomer():
    if 'id' in request.json:
        updateCustomer()
    else:
        createCustomer()
    return "ok"
def createCustomer():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `customers` (`id`, `firstname`, `lastname`, `email`, `phone`, `address`) VALUES (NULL, %s, %s, %s, %s, %s);",
                (request.json['firstname'], request.json['lastname'], request.json['email'], request.json['phone'], request.json['address']))
    mysql.connection.commit()
    return "Cliente guardado"
def updateCustomer():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE `customers` SET `firstname` = %s, `lastname` = %s, `email` = %s, `phone` = %s, `address` = %s WHERE `customers`.`id` = %s;",
                (request.json['firstname'], request.json['lastname'], request.json['email'], request.json['phone'], request.json['address'], request.json['id']))
    mysql.connection.commit()
    return "Cliente Actualizado Exitosamente"
@app.route('/api/customers/<int:id>', methods=['DELETE'])
@cross_origin()
def removeCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM `customers` WHERE `customers`.`id` = " + str(id))
    mysql.connection.commit()
    return "Cliente eliminado"
@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')
@app.route('/<path:path>')
@cross_origin()
def publicFiles(path):
    return render_template(path)
if __name__ == '__main__':
    app.run(None, 3000, True) # host : puerto : cada vez que guarda automaticamente sin cancelar etc asi que True