import flask
from flask import jsonify
from flask import request, make_response
from sql import create_connection
from sql import execute_read_query
import creds

app = flask.Flask(__name__)
app.config["DEBUG"] = True
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.username,
                         myCreds.password, myCreds.database)


@app.route('/inventory', methods=['GET'])
def all_inventory():
    sql = "SELECT * FROM Products"
    inventory = execute_read_query(conn, sql)
    results = []
    for product in inventory:
        results.append(product)
    return jsonify(results)


@app.route('/sales', methods=['GET'])
def all_sales():
    sql = "SELECT * FROM Orders"
    orders = execute_read_query(conn, sql)
    results = []
    for order in orders:
        results.append(order)
    return jsonify(results)


@app.route('/inventory', methods=['POST'])
def inventory_post():
    request_data = request.get_json()
    newproductname = request_data['productName']
    newproductdescription = request_data['Description']
    newproductprice = request_data['productprice']
    newproductquan = request_data['Quantity']
    newproductcat = request_data['productType']
    sql = "INSERT INTO Products (product_name,product_desc,product_price,product_quantity,catergory_id) VALUES ('%s', '%s' , $s , $s)" % (
        newproductname, newproductdescription, newproductprice, newproductquan, newproductcat
    )
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Add Request Successful"


@app.route('/inventory', methods=['PUT'])
def inventory_put():
    request_data = request.get_json()
    productname = request_data['productName']
    productdescription = request_data['Description']
    productprice = request_data['productprice']
    productquan = request_data['Quantity']
    productcat = request_data['productType']
    sql = """UPDATE Products 
    set product_name = '$s',
    set product_desc = '$s',
    set product_price = $s,
    set product_quantity = $s,
    set catergory_id)  = $s """ % (
        productname, productdescription, productprice, productquan, productcat
    )
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Add Request Successful"


app.run()
