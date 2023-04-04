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
    sql = """select p.product_id,p.product_name,p.product_desc,p.product_price,
             p.product_quantity,p.category_id,c.category_name
             from Products p join Category c 
             where p.category_id = c.category_id"""
    inventory = execute_read_query(conn, sql)
    results = []
    for product in inventory:
        results.append(product)
    return jsonify(results)


@app.route('/sales', methods=['GET'])
def all_sales():
    sql = "select * from Orders"
    orders = execute_read_query(conn, sql)
    results = []
    for order in orders:
        results.append(order)
    return jsonify(results)


@app.route('/customers', methods=['GET'])
def all_customers():
    sql = "select * from Customers"
    customers = execute_read_query(conn, sql)
    results = []
    for customer in customers:
        results.append(customer)
    return jsonify(results)


@app.route('/employees', methods=['GET'])
def all_employees():
    sql = "select * from Employees"
    employees = execute_read_query(conn, sql)
    results = []
    for employee in employees:
        results.append(employee)
    return jsonify(results)


@app.route('/orderdetails', methods=['GET'])
def order_details():
    sql = "select * from Order_details"
    details = execute_read_query(conn, sql)
    results = []
    for detail in details:
        results.append(detail)
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


@app.route('/employees', methods=['POST'])
def post_emp():
    request_data = request.get_json()
    nEmpid = request_data['Employee_ID']
    nEmpname = request_data['Employee_name']
    nphonenum = request_data['Phone_Number']
    njobtitle = request_data['Job_Title']
    sql = """insert into Employees (employee_id,employee_name,phone_number,job_title) values 
             (%s,'%s',%s,'%s')""" % (nEmpid, nEmpname, nphonenum, njobtitle)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Add Request Successful"


@app.route('/category', methods=['POST'])
def post_cat():
    request_data = request.get_json()
    ncat_id = request_data['Category_ID']
    ncat_name = request_data['Category_name']
    sql = "insert into Category (category_id,category_name) values ($s,'$s')" % (ncat_id, ncat_name)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Add Request Successful"


@app.route('/customers', methods=['POST'])
def post_cus():
    request_data = request.get_json()
    ncus_id = request_data['Customer_ID']
    nfirst_name = request_data['First_name']
    nlast_name = request_data['Last_name']
    phone_num = request_data['Phone_Number']
    sql = "insert into Customers (customer_id,first_name,last_name,phone_number) values (%s,'$s','$s',$s)" % (
    ncus_id, nfirst_name, nlast_name, phone_num)
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
