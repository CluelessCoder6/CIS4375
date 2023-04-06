import flask
from flask import jsonify
from flask import request, make_response
from sql import create_connection
from sql import execute_read_query
import creds

app = flask.Flask(__name__)
app.config["DEBUG"] = True
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.username, myCreds.password, myCreds.database)


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


@app.route('/orders', methods=['GET'])
def all_sales():
    sql = "select * from Orders"
    orders = execute_read_query(conn, sql)
    results = []
    for order in orders:
        results.append(order)
    return jsonify(results)


@app.route('/products', methods=['GET'])
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


@app.route('/products', methods=['POST'])
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


@app.route('/orderdetails', methods=['POST'])
def order_details_post():
    request_data = request.get_json()
    order_details_id = request_data['order_detail_id']
    quan = request_data['quantity']
    cost = request_data['cost']
    orderid = request_data['order_id']
    productid = request_data['product_id']
    sql = """insert into Order_details (order_detail_id,quantity,cost,order_id,product_id) values
             ($s,$s,%s,%s,%s)""" % (order_details_id, quan, cost, orderid, productid)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Add Request Successful"


@app.route('/orders', methods=['POST'])
def orders_post():
    request_data = request.get_json()
    orderid = request_data['order_id']
    orderdate = request_data['order_date']
    empid = request_data['employee_id']
    custid = request_data['customer_id']
    sql = """insert into Order (order_id,order_date,employee_id,customer_id) values
             ($s,'$s',%s,%s)""" % (orderid, orderdate, empid, custid)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Add Request Successful"


@app.route('/category', methods=['PUT'])
def cat_put():
    request_data = request.get_json()
    ucat_id = request_data['Category_ID']
    ucat_name = request_data['Category_name']
    sql = """update Category
             set category_name = '%s' where category_id = %s
          """ % (ucat_name, ucat_id)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Update Request Successful"


@app.route('/customers', methods=['PUT'])
def cust_put():
    request_data = request.get_json()
    ucus_id = request_data['Customer_ID']
    ufirst_name = request_data['First_name']
    ulast_name = request_data['Last_name']
    uphone_num = request_data['Phone_Number']
    sql = """update Customers
             set first_name = '%s',last_name = '%s',phone_number = %s where customer_id = %s""" % \
          (ufirst_name, ulast_name, uphone_num, ucus_id)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Update Request Successful"


@app.route('/employees', methods=['PUT'])
def emp_put():
    request_data = request.get_json()
    uEmpid = request_data['Employee_ID']
    uEmpname = request_data['Employee_name']
    uphonenum = request_data['Phone_Number']
    ujobtitle = request_data['Job_Title']
    sql = """update Employees 
             set employee_name = '%s',phone_number = %s,job_title = '%s'
             where employee_id = %s
             """ % (uEmpname, uphonenum, ujobtitle, uEmpid)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Update Request Successful"


@app.route('/orderdetails', methods=['PUT'])
def ord_deits_put():
    request_data = request.get_json()
    uorder_details_id = request_data['order_detail_id']
    uquan = request_data['quantity']
    ucost = request_data['cost']
    uorderid = request_data['order_id']
    uproductid = request_data['product_id']
    sql = """update Order_details 
             set quantity = %s,cost = %s,order_id = %s ,product_id = %s
             where order_detail_id = %s
             """ % (uquan, ucost, uorderid, uproductid, uorder_details_id)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Add Request Successful"


@app.route('/orders', methods=['PUT'])
def orders_put():
    request_data = request.get_json()
    uorderid = request_data['order_id']
    uorderdate = request_data['order_date']
    uempid = request_data['employee_id']
    ucustid = request_data['customer_id']
    sql = """update Order 
             set order_date = $s,employee_id = %s,customer_id = %s
             where order_id = $s
             """ % (uorderdate, uempid, ucustid, uorderid)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Update Request Successful"


@app.route('/products', methods=['PUT'])
def products_put():
    request_data = request.get_json()
    uproductname = request_data['productName']
    uproductdescription = request_data['Description']
    uproductprice = request_data['productprice']
    uproductquan = request_data['Quantity']
    uproductcat = request_data['productType']
    uproductid = request_data['productID']
    sql = """ update Products 
              set product_name = '%s',product_desc = '%s',product_price =%s,product_quantity = %s,catergory_id = %s
              where product_id = %s 
              """ % (uproductname, uproductdescription, uproductprice, uproductquan, uproductcat, uproductid)
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Update Request Successful"


@app.route('/category', methods=['DELETE'])
def cat_del():
    request_data = request.get_json()
    dcat_id = request_data['Category_ID']
    sql = " delete from Category where category_id = %s" % dcat_id
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Delete Request Successful"


@app.route('/customers', methods=['DELETE'])
def cust_del():
    request_data = request.get_json()
    dcustid = request_data['Customer_ID']
    sql = "delete from Customers where customer_id = %s" % dcustid
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Delete Request successful"


@app.route('/employees', methods=['DELETE'])
def emp_del():
    request_data = request.get_json()
    Empid = request_data['Employee_ID']
    sql = "delete from Employees where Employee_id = %s" % Empid
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Delete Request Successful"


@app.route('/orderdetails', methods=['DELETE'])
def ord_deits_del():
    request_data = request.get_json()
    order_details_id = request_data['order_detail_id']
    sql = "Delete from Order_details where order_detail_id = %s" % order_details_id
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Delete Request Successful"


@app.route('/orders', methods=['DELETE'])
def orders_del():
    request_data = request.get_json()
    orderid = request_data['order_id']
    sql = "delete from Orders where Order_id = %s" % orderid
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Delete Request Successful"


@app.route('/products', methods=['DELETE'])
def product_delete():
    request_data = request.get_json()
    prodid = request_data["ProductID"]
    sql = "delete from Products where Product_id = %s" % prodid
    execute_read_query(conn, sql)
    execute_read_query("commit")
    return "Delete Request Successful"


app.run()
