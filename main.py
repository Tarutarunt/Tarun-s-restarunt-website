import os.path
import time

from flask import Flask, render_template, request, session, redirect, url_for

from Yummy.DBConn import execteQuery, fetchOne, fetchData

app=Flask(__name__)

@app.route("/adminviewusers")
def adminviewusers():
    cols = ["UserId", "FirstName", "LastName", "EmailId", "PhoneNum", "Aadhar", "Address"]
    data = fetchData("select * from customer_table")
    return render_template("adminviewusers.html",
                           data=data, cols=cols)
@app.route("/adminviewfood")
def adminviewfood():
    cols = [ "FoodId","FoodName", "Quantity", "Price", "Ingredients"]
    data = fetchData("select * from food_table")
    return render_template("adminviewfood.html",
                           data=data, cols=cols)
@app.route("/adminviewcart")
def adminviewcart():
    cols = [ "FoodId","FoodName", "Quantity", "Price", "Ingredients"]
    data = fetchData("select * from food_table")
    return render_template("adminviewcart.html",
                           data=data, cols=cols)

app.secret_key="Yummy@123"
app.config['UPLOAD_FOLDER'] = "static/assets/img/"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/logout")
def logout():
    session['id']=None
    return render_template("index.html")

@app.route("/menu1")
def menu():
    return render_template("menu1.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/userviewfood", methods=["POST", "GET"])
def userviewfood():
    data = fetchData("select * from food_table")
    if (request.method == "POST"):
        fname = request.form.get("fname")
        data = fetchData("select * from food_table where foodname like '%"+fname+"%'")
    return render_template("userviewfood.html",data=data)

@app.route("/userviewaddtocart")
def userviewaddtocart():
    userid = session['id']
    cols = [ "FoodId", "UserId", "FoodName", "Price", "Ingredients", "Quantity", "TotalPrice"]
    row = fetchData("select * from cart_table where userid = " + str(userid) + " and paymentstatus = 'Booked'")
    total = 0
    for x in row:
        total += int(x[6])
    print("Row : ", row)
    return render_template("userviewcart.html",
                           data=row, cols=cols, total=total)
@app.route("/userviewcart")
def userviewcart():
    userid = session['id']
    cols = [ "FoodId", "UserId", "FoodName", "Price", "Ingredients", "Quantity", "TotalPrice"]
    row = fetchData("select * from cart_table where userid = " + str(userid) + " and paymentstatus = 'Booked'")
    total=0
    for x in row:
        total += int(x[6])
    print("Row : ", row)
    return render_template("userviewcart.html",
                           data=row, cols=cols,total=total)

@app.route("/useraddtocart", methods=["POST", "GET"])
def useraddtocart():
    id=request.args['fid']
    sql="select * from food_table where fid = "+str(id)
    data = fetchOne(sql)
    return render_template("useraddtocart.html",
                           data=data)

@app.route("/adminviewstaffs")
def adminviewstaffs():
    cols = ["StaffId", "FirstName", "LastName", "EmailId", "PhoneNum", "Aadhar", "Address"]
    data = fetchData("select * from staff_table")
    return render_template("adminviewstaffs.html",
                           data=data, cols=cols)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    msg=""
    if(request.method=="POST"):
        cname = request.form.get("cname")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        sql = ("Insert into ContactTable(cName, email, subject, message) "
                "values('%s','%s','%s','%s')")%(cname, email, subject, message)

        execteQuery(sql)
        msg = "Contact Details Inserted Success"
    return render_template("contact.html", msg=msg)

@app.route("/login", methods=["POST", "GET"])
def login():
    msg=""
    if (request.method == "POST"):
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        print("Uname : ", uname, " Pwd : ", pwd)
        if(uname == "admin" and pwd == "admin"):
            return render_template("adminmainpage.html")
        else:
            sql = ("Select * from customer_table where uname='%s' and "
                   "pwd = '%s'") % (uname, pwd)
            data = fetchOne(sql)
            if (data):
                session['id'] = data[0]
                return render_template("usermainpage.html")
            else:
                msg = "Invalid UserName/Password"
    return render_template("login.html", msg=msg)


@app.route("/forgetpwd")
def forgetpwd():
    return render_template("forgetpwd.html")

@app.route("/forgetpwd1")
def forgetpwd1():
    return render_template("forgetpwd1.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    msg = ""
    if (request.method == "POST"):
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        email = request.form.get("email")
        phnum = request.form.get("phnum")
        aadhar = request.form.get("aadhar")
        address = request.form.get("address")

        sql = (("Select * from customer_table where uname='%s' or "
               "phnum = '%s' or email = '%s' or aadhar = '%s'") %
               (uname, phnum, email, aadhar))

        data = fetchOne(sql)

        if(data):
            msg = "Duplicate Email/Phnum/Uname/Aadhar"
        else:
            sql = (("INSERT INTO customer_table(fname,lname,uname,pwd,"
               "email,phnum,aadhar,address) VALUES "
               "('%s','%s','%s','%s','%s','%s','%s','%s')") %
               (fname, lname, uname, pwd, email, phnum, aadhar, address))
            execteQuery(sql)
            msg = "Register Successfully Done"
    return render_template("register.html", msg=msg)

@app.route("/adminaddstaff", methods=["POST", "GET"])
def adminaddstaff():
    msg = ""
    if (request.method == "POST"):
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        email = request.form.get("email")
        phnum = request.form.get("phnum")
        aadhar = request.form.get("aadhar")
        address = request.form.get("address")

        sql = (("INSERT INTO staff_table(fname,lname,uname,pwd,"
               "email,phnum,aadhar,address) VALUES "
               "('%s','%s','%s','%s','%s','%s','%s','%s')") %
               (fname, lname, uname, pwd, email, phnum, aadhar, address))
        execteQuery(sql)
        msg = "Staff Details Inserted Success"
    return render_template("adminaddstaff.html", msg=msg)

@app.route("/useraddtocart1", methods=["POST", "GET"])
def useraddtocart1():
    msg = ""
    if (request.method == "POST"):
        userid = session['id']
        fid = request.form.get("fid")
        fname = request.form.get("fname")
        required = request.form.get("required")
        price = request.form.get("price")
        ingredients = request.form.get(" ingredients")
        total = request.form.get("total")
        sql = (("INSERT INTO cart_table(foodid,userid,fname,price,ingredients,required,total, paymentstatus)VALUES"
               "('%s','%s','%s','%s','%s','%s','%s','%s')") %
               (fid, userid, fname,price, ingredients,  required, total, 'Booked'))
        execteQuery(sql)
        msg = "Food Added to Cart Success"
    return redirect(url_for("userviewaddtocart"))

@app.route("/adminaddfood", methods=["POST", "GET"])
def adminaddfood():
    msg = ""
    if (request.method == "POST"):
        fname = request.form.get("fname")
        quantity = request.form.get("quantity")
        price = request.form.get("price")
        ingredients = request.form.get(" ingredients")
        image = request.files['image']
        filename = "Img"+str(round(time.time()))+".jpg"
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        sql = (("INSERT INTO food_table(fname,quantity,price, ingredients, filename) VALUES "
               "('%s','%s','%s','%s','%s')") % (fname, quantity,price, ingredients, filename))
        execteQuery(sql)
        msg = "Food Details Inserted Success"
    return render_template("adminaddfood.html", msg=msg)

@app.route("/order")
def order():
    total = request.args['total']
    return render_template("order.html",total=total)
@app.route("/order1", methods=["POST", "GET"])

def order1():
    msg = ""
    if (request.method == "POST"):
        userid = session['id'];
        cardno = request.form.get("cardno")
        cvv = request.form.get("cvv")
        total = request.form.get("total")
        sql = (("INSERT INTO ordertable(userid,cardno,cvv,total)VALUES"
               "('%s','%s','%s','%s')") % (userid,cardno,cvv,total))
        execteQuery(sql)
        sql = "Update cart_table set paymentstatus = 'Paid' where userid = " + str(userid)
        execteQuery(sql)
        msg = "payment Success"
    return redirect(url_for("userviewreport"))

@app.route("/userviewreport")
def userviewreport():
    userid = session['id']
    cols = [ "OrderId","CardNo","CVV","Total"]
    data = fetchData("select * from ordertable where userid = " + str(userid))
    return render_template("userviewreport.html",
                           data=data, cols=cols)
@app.route("/adminviewreports")
def adminviewreports():
    #userid = session['id']
    cols = [ "OrderId","CardNo","CVV","Total"]
    data = fetchData("select * from ordertable ")
    return render_template("adminviewreports.html",
                           data=data, cols=cols)


if __name__== "__main__":
    app.run(debug=True)