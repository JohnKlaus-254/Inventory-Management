from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from funtions import Newstock
import pygal

from configs import Development
import psycopg2
#flask object
app = Flask(__name__)

app.config.from_object(Development)
#sql_alchemy instance
db = SQLAlchemy(app)

from models.inventories import InventoryModel
from models.sales import SalesModel

@app.before_first_request
def create_tables():
    db.create_all()
    # db.drop_all()


@app.route('/',methods=['GET'])#defining a route
def hello_world():
    pie_chart = pygal.Pie()
    pie_chart.title = 'Total Products and Services distribution in (%)'
    pie_chart.add('Product', InventoryModel.getCountType("Product"))
    pie_chart.add('Service', InventoryModel.getCountType("Service"))
    graph_data = pie_chart.render_data_uri()


    conn = psycopg2.connect("dbname='NCK_DB' user='postgres' host='localhost' password='Jonitez1'")

    cur = conn.cursor()
    cur.execute("""SELECT (sum(i.buying_price * s.s_qty)) as subtotal, EXTRACT(MONTH FROM s.time_created) as sales_month 
from sales as s 
join inventories as i on s.inv_id = i.id
GROUP BY sales_month
ORDER BY sales_month""")
    rows = cur.fetchall()
    # print(rows)

    x = ['Jan','Feb','Mar','Apl','May','Jun','July','Agt','Sept','Oct','Nov','Dec']
    y = []
    for row in rows:
        # x.append(row[1])
        y.append(row[0])

    line = pygal.Line()
    line.title = '% Change Coolness of programming languages over time.'
    line.x_labels = map(str, x)
    line.add('SubTotal', y)
    line_data = line.render_data_uri()

    linec = pygal.Bar()
    linec.title = '% Change Coolness of programming languages over time.'
    linec.x_labels = map(str, x)
    linec.add('SubTotal', y)
    linec = linec.render_data_uri()


    return render_template('index.html', graph_data=graph_data, line_data = line_data, linec=linec) #always ensure you pass it as a string


#about page route
@app.route('/about')
def about_page():
    return render_template('about.html')
#inventory route
@app.route('/inventory', methods=['GET','POST'])
def inventory_page():

    objquery = InventoryModel.query.all()
    if request.method =='POST':
        Iname = request.form['inventory']
        type = request.form['type']
        buying_price =request.form['bp']
        selling_price =request.form['sp']
        stock =request.form['stock']
        re_order =request.form['rp']

        obj = InventoryModel(inv_name=Iname, inv_type= type,buying_price=buying_price,selling_price=selling_price,
                             stock=stock,re_order_period=re_order)
        db.session.add(obj)
        db.session.commit()
        print('Your record is Succefful')
        return redirect(url_for('inventory_page'))
    return render_template('inventory.html', var = objquery)

@app.route('/sales', methods=['POST'])
def sales():
    if request.method == 'POST':
        qn = request.form['quantity']
        inv_id = request.form['inv_id']

        if InventoryModel.update_stock(id=inv_id,qty=int(qn)):
            print('Success')
            sale = SalesModel(quantity=qn, inv_id=inv_id)
            db.session.add(sale)
            db.session.commit()
        else:
            print('You dont have enough stock to sell {}'.format(qn))



        return redirect(url_for('inventory_page'))

@app.route('/edit/inventory', methods=['POST'])
def edit_record():
    if request.method == 'POST':
        Iname = request.form['inventory']
        type = request.form['type']
        buying_price = request.form['bp']
        selling_price = request.form['sp']
        stock = request.form['stock']
        re_order = request.form['rp']
        inv_id = request.form['inv_id']

        InventoryModel.edit_record(id=inv_id, name=Iname,type=type,bp=buying_price,sp=selling_price,stock=stock,rp=re_order)

        print('success')
        return redirect(url_for('inventory_page'))
 #view sales for a specific inventory
@app.route('/inventory/<int:id>/sales')
def view_sales(id):
    inv = InventoryModel.query.filter_by(id=id).first()

    name = inv.inv_name
    #list of sales
    inv_sales = inv.sales
    return render_template('Sales.html', sales = inv_sales, name=name)



#contact route
@app.route('/contacts')
def contact_page():
    return render_template('Contacts.html')




if __name__ == '__main__':
    app.run(debug=True)
