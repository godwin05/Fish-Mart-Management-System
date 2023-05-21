import random
from flask import Flask, render_template, request, redirect , flash, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy import text
import flask_session  as fs
from werkzeug.utils import secure_filename
from base64 import b64encode, b64decode
import jinja2
import os
import razorpay
import json


dict={
    'Tuna' : " A large fish that is popular in sushi and sashimi dishes. Tuna is known for its firm, meaty texture and rich flavor.",
    'Salmon' : "A fish that is popular for its flavor and nutritional value. Salmon has a distinctive pink flesh and is often used in sushi, smoked, or grilled dishes.",
    'Parai' : "Parai (False Trevally) - Parai is a saltwater fish that is popular in Tamil Nadu. It has a firm, meaty texture and a mild, slightly sweet flavor. It is often grilled or fried with spices.",
    'Red Snapper' : "Sankara (Red Snapper) - Sankara is a popular saltwater fish in Tamil Nadu. It has a firm, white flesh and a mild, slightly sweet flavor. It is often grilled or fried with spices",
    'Nangu' : "Nangu (Queen Fish) - Nangu is a saltwater fish that is popular in Tamil Nadu. It has a firm, meaty texture and a mild, slightly sweet flavor. It is often grilled or fried with spices.",
    'Rohu' :"Rohu - A freshwater fish that is widely consumed in North and East India, Rohu has a sweet, delicate flavor and a firm texture. It is often cooked in curries, fried, or grilled.",
    'Pearl Spot' : "Pearl Spot (Karimeen) - Pearl spot is a freshwater fish that is popular in Kanyakumari. It has a delicate, sweet flavor and a tender texture. It is often grilled or fried with spices.",
    'Nethili' : "Nethili (Anchovy) - Nethili is a small, saltwater fish that is commonly consumed in Tamil Nadu. It has a rich, strong flavor and is often grilled or fried.",
    'Ayira Meen' : "Ayira Meen (Indian Mackerel) - Ayira Meen is a small, oily fish that is commonly found in the waters around Tamil Nadu. It has a rich, strong flavor and is often grilled or fried.",
    'Seer Fish' : "Seer Fish (Ney Meen) - Seer fish is a popular saltwater fish in Kanyakumari. It has a firm, meaty texture and a mild, slightly sweet flavor. It is often grilled, fried, or used in curries.",
    'Vanjaram' : "Vanjaram (King Fish) - Vanjaram is a popular saltwater fish in Tamil Nadu. It has a firm, meaty texture and a mild, slightly sweet flavor. It is often grilled, fried, or used in curries.",
    'Sardine' : "Sardine (Mathi) - Sardine is a small, oily fish that is commonly consumed in Kanyakumari. It has a rich, strong flavor and is often grilled or fried.",
    'King Prawn' : "King Prawn (Eral) - King prawn is a popular seafood in Kanyakumari. It has a sweet, delicate flavor and a firm, meaty texture. It is often used in curries or grilled with spices.",
    'Squid' : "Squid (Kanava) - Squid is a popular seafood in Kanyakumari. It has a mild, slightly sweet flavor and a tender, chewy texture. It is often used in curries or fried with spices.",
    'Indian Mackerel' : "Indian Mackerel (Ayila) - Indian mackerel is a small, oily fish that is commonly found in the waters around Kanyakumari. It has a rich, strong flavor and is often grilled or fried.",
    'Barracuda' : "Barracuda (Sheela) - Barracuda is a saltwater fish that is popular in Kanyakumari. It has a firm, meaty texture and a mild, slightly sweet flavor. It is often grilled or fried with spices."
}




app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,'fish_mart.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANT'] = False
app.config['SESSION_TYPE'] = "filesystem"
app.secret_key='123'
fs.Session(app)
db = SQLAlchemy(app)

razorpay_client = razorpay.Client(auth=("<enter id>", "<enter u r key>"))

str_date = str(datetime.now()).split(" ")
timee= str_date[0].split("-")


class User_Register(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    pin = db.Column(db.Integer, nullable=False)
    password = db.Column(db.Integer, nullable=False, unique=True)
    Address = db.Column(db.String(150), nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<User : {self.email}>"

class Seller_Registion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    shop = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Integer, nullable=False, unique=True)
    details = db.Column(db.String(50), nullable=False)
    img_file = db.Column(db.Text, nullable=False)
    file_name = db.Column(db.Text, nullable=False)
    file_type = db.Column(db.Text, nullable=False)
    verify = db.Column(db.Integer, nullable= False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<User : {self.details}>"

class Fisheries(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    offer = db.Column(db.Integer, nullable=False)
    catch = db.Column(db.Integer, nullable=False)
    perishable = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(550), nullable=False)
    image =  db.Column(db.Text, nullable=False)
    seller_id= db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<User : {self.name}>"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)
    def __repr__(self):
        return f"<User : {self.id}>"

class BuyedProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    sucess= db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.Date, default=date.today())
    def __repr__(self):
        return f"<User : {self.id}>"

class Bidding_fishes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(550), nullable=False)
    image1 = db.Column(db.Text, nullable=False)
    image2 = db.Column(db.Text, nullable=False)
    image3 = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    highest_bid = db.Column(db.Integer, nullable=False)
    bid = db.Column(db.Integer, nullable=False)
    user_address = db.Column(db.String(150), nullable=False)
    user_phone = db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.Date, nullable= False)
    def __repr__(self):
        return f"<User : {self.id}>"

class Bidding_entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bidding_id = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<User : {self.id}>"

class FeedBack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(100))
    rating = db.Column(db.String(10))
    verify = db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.Date, default=date.today())
    def __repr__(self):
        return f"<User : {self.id}>"

with app.app_context():
    db.create_all()


@app.route('/')
def home_page():
    data = Fisheries.query.order_by(Fisheries.id.desc()).all()
    # User.query.order_by(User.age.desc()).all()
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    encode = jinja_env.filters['b64encode'] = b64encode
    decode = jinja_env.filters['b64decode'] = b64decode
    if 'userid' in session:
        id= session['userid']
        user_data= User_Register.query.filter_by(id=id).first()
        if user_data is None:
            logout()
            return render_template("index.html", data=data, encode=encode, decode=decode, user_data=0)
        else:
            return render_template("index.html", data=data, encode=encode, decode=decode,user_data=user_data)
    else:
        return render_template("index.html", data=data, encode=encode, decode=decode, user_data=0)

@app.route('/register')
def register_page():
    if 'userid' in session:
        id= session['userid']
        user_data= User_Register.query.filter_by(id=id).first()
        return render_template("registration.html",user_data=user_data)
    return  render_template("registration.html",user_data=0)

@app.route('/seller_register')
def seller_register():
    if 'userid' in session:
        id = session['userid']
        user_data = User_Register.query.filter_by(id=id).first()
        return render_template("seller_registration.html", user_data=user_data)
    return  render_template("seller_registration.html", user_data=0)

@app.route('/signin')
def signin():
    if 'userid' in session:
        id= session['userid']
        user_data= User_Register.query.filter_by(id=id).first()
        return render_template('signin.html', user_data=user_data)
    return render_template('signin.html',user_data=0)



@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        query = Fisheries.query.filter(Fisheries.name.like("%" + search + "%")).all()
        print(query)
        if 'userid' in session:
            id = session['userid']
            user_data = User_Register.query.filter_by(id=id).first()
            return render_template('search_fisheries.html', data=query, encode=encode, decode=decode, length=len(query),user_data=user_data)
        return render_template('search_fisheries.html', data=query, encode=encode, decode=decode, length=len(query),user_data=0)


@app.route('/view_orders')
def view_orders():
    if 'userid' in session:
        user_id = session['userid']
        user_data= User_Register.query.filter_by(id=user_id).first()

        user_feedback = FeedBack.query.filter_by(user_id=user_id,verify =0).all()
        buyer_products =[]
        feedback_id = []
        for product in user_feedback:
            fishes = Fisheries.query.filter_by(id= product.product_id).first()
            if fishes is not None:
                print(fishes)
                buyer_products.insert(0,fishes)
                feedback_id.insert(0,product)
        print(buyer_products)
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        return render_template("view_orders.html", orders = zip(buyer_products,feedback_id), user_data=user_data,encode=encode, decode=decode)

    else:
        flash("u r not yet login..!")
        return redirect('/signin')

@app.route('/view_orders/feedback',methods=['GET','POST'])
def user_feedback():
    if request.method == 'POST':
        user_id = session['userid']
        feedback_id = request.form['feedback_id']
        user = User_Register.query.filter_by(id=user_id).first()
        return  render_template("user_feedback.html",user_data=user,feedback_id=feedback_id,)

@app.route('/view_orders/feedback/submit', methods=['GET','POST'])
def submit_feedback():
    if request.method == 'POST':

        feedback_id = request.form['feedback_id']
        print(f'seller:{feedback_id}')
        feedback = request.form['feedback']
        rating = request.form['rate']

        data = FeedBack.query.filter_by(id=feedback_id).first()
        data.rating = rating
        data.feedback = feedback
        data.verify = 1
        db.session.commit()


        return redirect('/view_orders')


@app.route('/user_details' , methods =['GET', 'POST'])
def user_details():
    if request.method =="POST":
        name= request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        pin = request.form['pin']
        pwd = request.form['pwd']
        conform_pwd = request.form['re_pwd']
        address = request.form['address']
        if pwd == conform_pwd:
            email_exist = bool(User_Register.query.filter_by(email=email).first())
            password_exist = bool(User_Register.query.filter_by(password=pwd).first())
            if email_exist:
                flash("This email already exist.", "danger")
                return redirect('/register')
            elif password_exist:
                flash("This password already exist.", "danger")
                return redirect('/register')
            else:
                query = User_Register(name=name, phone= phone, email=email, pin = pin, password= pwd, Address=address)
                db.session.add(query)
                db.session.commit()
                return redirect('/signin')
        else:
            flash("the password are not same...","danger")
            return redirect('/register')

@app.route('/seller_detail', methods=["GET","POST"])
def seller_detail():
    if request.method == "POST":
        name = request.form['name']
        shop = request.form['shop']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['pwd']
        conform_pwd = request.form['re_pwd']
        detail = request.form['details']
        img = request.files['filee']
        verify = request.form['verify']

        if  password == conform_pwd:
            email_exist = bool(Seller_Registion.query.filter_by(email=email).first())
            password_exist = bool(Seller_Registion.query.filter_by(password=password).first())
            if email_exist:
                flash("This email already exist.", "danger")
                return redirect('/seller_register')
            elif password_exist:
                flash("This password already exist.", "danger")
                return redirect('/seller_register')
            else:
                filename = secure_filename(img.filename)
                filetype=img.mimetype
                query = Seller_Registion(name=name,shop=shop, phone=phone, email=email, password=password, details=detail, img_file= img.read(), file_name=filename, file_type=filetype, verify = verify)
                db.session.add(query)
                db.session.commit()
                return redirect('/signin')

        else:
            flash("the password are not same...", "danger")
            return redirect('/seller_register')
    
@app.route('/signin_detail', methods=['GET','POST'])
def signin_detail():
    if request.method == "POST":
        username=request.form['name']
        password = request.form['password']
        # print(f"name: {username}, pwd ={password} ")
        buyer = User_Register.query.filter_by(name=username, password=password).first()
        seller = Seller_Registion.query.filter_by(name=username, password=password).first()
        admin_name="admin@123"
        admin_pwd = "admin@pwd"

        if buyer is not None:

            session['userid']=buyer.id

            # flash("Welcome buyer")
            return redirect("/")
        elif seller is not None:
            id = seller.verify
            if id==0:
                flash("Your request is under processing")
                return redirect('/signin')
            else:
                session['userid']=seller.id
                # flash("Welcome seller")
                return redirect("/seller")
        elif username==admin_name and password ==admin_pwd:
            session['userid'] = 1
            return  redirect('/admin')
        else:
            flash("make sure you enter the correct details")
            return redirect("/signin")
# admin pages


@app.route('/admin')
def admin():
    if 'userid' in session:
        cart_product_amount=[]
        cart = BuyedProducts.query.order_by(BuyedProducts.date_joined).all()
        print(cart)
        for ids in cart:
            print(ids.product_id)
            fish = Fisheries.query.filter_by(id=ids.product_id).first()
            if fish is not None:
                print(fish)
                print(fish.price)
                amount = fish.price-((fish.price/100)*fish.offer)
                cart_product_amount.append(amount)
        seller = Seller_Registion.query.filter_by(verify=1).all()
        user = User_Register.query.order_by(User_Register.date_joined).all()
        allfish = Fisheries.query.order_by(Fisheries.date_joined).all()
        req_seller = Seller_Registion.query.filter_by(verify=0).all()
        feedback = FeedBack.query.filter_by(verify =1).all()
        return render_template('admin_dashboard.html', revenue=round(sum(cart_product_amount)),user = len(user),
                               seller=len(seller), fishes= len(allfish),req_seller=len(req_seller), feedback=len(feedback))




@app.route("/admin/requested_seller",methods=['GET', 'POST'])
def admin_request():
    if "userid" in session:
        data = Seller_Registion.query.filter_by(verify=0).all()
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        return render_template("admin_requested_seller.html", data = data, encode=encode, decode=decode)
    else:
        flash("you are not yet login")
        return redirect('/signin')
# @app.route('/admin')


@app.route('/verify', methods=['GET','POST'])
def verify():
    if request.method=='POST':
        id = request.form['id']
        update=Seller_Registion.query.filter_by(id=id).first()
        update.verify=1
        db.session.commit()
        return redirect('/admin/requested_seller')
@app.route('/reject_seller', methods=['GET','POST'])
def reject_request():
    id = request.form['id']
    deleted = Seller_Registion.query.get(id)
    db.session.delete(deleted)
    db.session.commit()
    return  redirect('/admin/requested_seller')

@app.route('/admin/verifiedSeller', methods=['GET','Post'])
def verified_seller():
    if "userid" in session:
        data = Seller_Registion.query.filter_by(verify=1).all()
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        return render_template("verifiedSeller.html", data = data, encode=encode, decode=decode)
    else:
        flash("you are not yet login")
        return redirect('/signin')

@app.route('/remove_verifier', methods=['GET','POST'])
def remove_verifier():
    if request.method == "POST":
        id = request.form['id']
        deleted = Seller_Registion.query.get(id)
        deleted.verify = 2
        db.session.commit()
        seller_fishes =  Fisheries.query.filter_by(seller_id = id).all()
        for data in seller_fishes:
            db.session.delete(data)
            db.session.commit()
        return redirect("/admin/verifiedSeller")
@app.route('/admin/view_all_products')
def admin_view_buyer():
    all_data= BuyedProducts.query.order_by(BuyedProducts.date_joined).all()
    fishes=[]
    user=[]
    for id in all_data:
        fish_data = Fisheries.query.filter_by(id=id.product_id).first()
        if fish_data is not None:
            fish_data= Fisheries.query.filter_by(id=id.product_id).first()
            user_data= User_Register.query.filter_by(id= id.user_id).first()
            fishes.insert(0,fish_data)
            user.insert(0,user_data)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    encode = jinja_env.filters['b64encode'] = b64encode
    decode = jinja_env.filters['b64decode'] = b64decode
    print(fishes)
    print(user)
    return render_template("admin_view_ordered_products.html", data=zip(fishes,user), encode= encode, decode= decode)

@app.route('/admin/view_all_buyers')
def admin_view_all_buyers():
    users= User_Register.query.order_by(User_Register.date_joined).all()
    return  render_template("admin_view_customer.html", data=users)

@app.route('/admin/allfisheries')
def all_fisheries():
    fishes= Fisheries.query.order_by(Fisheries.date_joined).all()
    seller_data=[]
    for id in fishes:
        seller = Seller_Registion.query.filter_by(id=id.seller_id).first()
        seller_data.append(seller)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    encode = jinja_env.filters['b64encode'] = b64encode
    decode = jinja_env.filters['b64decode'] = b64decode
    return  render_template('admin_view_fisheries.html', encode=encode, decode= decode, data= zip(fishes,seller_data))


@app.route('/admin/view_feedback')
def view_feedback():
    feedback = FeedBack.query.filter_by(verify=1).all()
    user_data=[]
    feedback_data=[]
    seller_data=[]
    for feedback in feedback:
        seller = Seller_Registion.query.filter_by(id=feedback.seller_id).first()
        user = User_Register.query.filter_by(id=feedback.user_id).first()
        user_data.insert(0,user)
        feedback_data.insert(0,feedback)
        seller_data.insert(0,seller)
    return render_template('admin_view_feedback.html',data=zip(user_data,feedback_data,seller_data))

@app.route('/admin/view_feedback/remove',methods=['GET','POST'])
def remove_feedback():
    if request.method == 'POST':
        feedback_id = request.form['feedback_id']
        feedback = FeedBack.query.filter_by(id=feedback_id).first()
        feedback.verify=2
        db.session.commit()
        return redirect('/admin/view_feedback')



# fish seller pagee

@app.route('/seller')
def seller_dashboard():
    if 'userid' in session:
        seller_id=session['userid']
        total_customer = []
        total_order=[]
        total_revenue=[]
        seller = Seller_Registion.query.filter_by(id=seller_id).first()
        fish = Fisheries.query.filter_by(seller_id=seller_id).all()
        # print(f"{fish}, length ={len(fish)}")
        total_fisheries=0
        for fish in fish:
            total_fisheries+=1
            cart=BuyedProducts.query.filter_by(product_id=fish.id,sucess=3).all()
            for cart in cart:
                cost=Fisheries.query.filter_by(id=cart.product_id).first()
                price=(cost.price/100)*(100-cost.offer)
                total_revenue.append(price)
                if cart.user_id not in total_customer:
                    total_customer.append(cart.user_id)
                total_order.insert(0,cart)
        user_data=[]
        product_data=[]
        purchase_date=[]
        cart_data=total_order[slice(2)]
        for data in cart_data:
            purchase=BuyedProducts.query.filter_by(id=data.id).first()
            product=Fisheries.query.filter_by(id=data.product_id).first()
            user= User_Register.query.filter_by(id=data.user_id).first()
            user_data.append(user)
            product_data.append(product)
            purchase_date.append(purchase)
        print(date.today())
        today_order= BuyedProducts.query.filter_by(date_joined=date.today(),seller_id=seller_id,sucess=3).all()
        return render_template("seller_dashboard.html",seller=seller,customers=len(total_customer), orders=len(total_order),
                               revenue=round(sum(total_revenue)),products=total_fisheries,data=zip(user_data,product_data,purchase_date),
                               today_order=len(today_order))
    else:
        flash("you are not yet login")
        return redirect('/signin')


@app.route('/seller/upload_fisheries', methods=['GET','POST'])
def upload_fisheries():
    id=session['userid']
    seller = Seller_Registion.query.filter_by(id=id).first()
    return render_template("upload_fisheries.html", seller=seller)


@app.route('/seller/update_seller_detail')
def update_seller_detail():
    id= session['userid']
    seller= Seller_Registion.query.filter_by(id=id).first()
    return  render_template("seller_detail_update.html",seller=seller)


@app.route('/fishery_details', methods=['GET','POST'])
def fishery_details():
    if 'userid' in session:
        if request.method == "POST":
            name= request.form['names']
            price = request.form['price']
            offer = request.form['offer']
            date = request.form['date']
            perishable = request.form['perishable']
            image = request.files['file']
            # detail = request.form['detail']
            detail= dict[name]
            seller_id = session['userid']
            query = Fisheries(name=name,price=price, offer = offer, catch = date, perishable= perishable, image = image.read(), detail = detail, seller_id=seller_id)
            db.session.add(query)
            db.session.commit()
            flash("sucessfully uploaded..")
            return redirect('/seller/upload_fisheries')

    else:
        return redirect('/signin')

@app.route('/seller/view_fisheries')
def view_fisheries():
    if 'userid' in session:
        id = session['userid']
        data = Fisheries.query.filter_by(seller_id=id).all()
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        seller = Seller_Registion.query.filter_by(id=id).first()
        return render_template("view_product.html", data = data, encode=encode, decode=decode, seller=seller)
    else:
        return redirect('/signin')

@app.route("/seller/view_fisheries/update", methods=['GET','POST'])
def update_page():
    if request.method=="POST":
        id = request.form['update']
        data = Fisheries.query.filter_by(id=id).first()
        seller = Seller_Registion.query.filter_by(id= session['userid']).first()
        return  render_template("update_fisheries.html",data=data,seller=seller)


@app.route('/seller/view_fisheries/update_fisheries', methods=['GET','POST'])
def update_fisheries():
    if request.method=='POST':
        id = request.form['update']
        name = request.form['names']
        price = request.form['price']
        offer = request.form['offer']
        catch = request.form['date']
        perishable = request.form['perishable']
        detail = dict[name]
        # Fisheries.query.filter_by(id=id).update(dict(name=name, price=price, offer=offer, catch = catch, perishable = perishable, detail= detail))
        update = Fisheries.query.filter_by(id=id).first()
        update.name = name
        update.price = price
        update.offer = offer
        update.catch = catch
        update.perishable = perishable
        update.detail = detail
        db.session.commit()

        return  redirect('/seller/view_fisheries')

@app.route('/seller/view_fisheries/delete', methods=['GET','POST'])
def delete_fisheries():
    if request.method== 'POST':
        id = request.form['remove']
        deleted = Fisheries.query.get(id)
        db.session.delete(deleted)
        db.session.commit()
        return  redirect('/seller/view_fisheries')



@app.route('/seller/view_orders')
def view_user_orders():
    seller_id = session['userid']
    seller_data=[]
    cart_prod_id=[]
    user_data=[]
    fish_data=[]
    buy_product=[]
    data = Fisheries.query.filter_by(seller_id=seller_id).all()
    for prod in data:
        seller_data.append(prod.id)
    for cart_id in seller_data:
        cart_data = BuyedProducts.query.filter_by(product_id=cart_id,sucess=3).all()
        cart_prod_id.append(cart_data)

    for x in cart_prod_id:
        for y in x:
            user= User_Register.query.filter_by(id=y.user_id).first()
            fish= Fisheries.query.filter_by(id=y.product_id).first()
            user_data.insert(0,user)
            fish_data.insert(0,fish)
            buy_product.insert(0,y)
    # user_product_data = zip(user_data,fish_data)
    seller = Seller_Registion.query.filter_by(id=seller_id).first()
    return  render_template("seller_view_cart.html",data=zip(user_data,fish_data,buy_product),seller=seller)


# seller bidding system

@app.route('/seller/bidding_home')
def bidding_home():
    query = Bidding_fishes.query.order_by(Bidding_fishes.date_joined).all()
    bid_data = []
    seller = Seller_Registion.query.filter_by(id=session['userid']).first()
    for data in query:
        if data.user_id != 0:
            bidding = Bidding_fishes.query.filter_by(user_id=data.user_id).first()
            bid_data.append(bidding)
    return render_template("seller_bidding_page.html",seller=seller,num = len(bid_data))


@app.route('/seller/bidding_upload_fisheries')
def bidding_upload_fisheries():
    if 'userid' in session:
        seller_id = session['userid']
        seller = Seller_Registion.query.filter_by(id=seller_id).first()
        today = date.today()
        return  render_template("seller_upload_bidding_fisheries.html",seller=seller,today_date=today)


@app.route("/seller/bidding_fishery", methods=['GET','POST'])
def bidding_fishery():
    if request.method=='POST':
        name = request.form['names']
        highest_bid = request.form['price']
        time = request.form['stime']
        date_joined = date.today()
        img1 = request.files['file1']
        img2 = request.files['file2']
        img3 = request.files['file3']
        seller_id = session['userid']
        details=dict[name]
        weight=request.form['weight']
        user_id =0
        user_address=0
        user_phone=0
        query = Bidding_fishes(name=name, user_id= user_id, seller_id= seller_id, image1 = img1.read(), image2=img2.read(), image3=img3.read(), time=time,
                               details=details, bid=weight, highest_bid=highest_bid,user_address=user_address,
                               user_phone=user_phone,date_joined=date_joined)
        db.session.add(query)
        db.session.commit()
        flash("sucessfully uploaded..")
        return redirect('/seller/bidding_upload_fisheries')

@app.route('/seller/bidding_records')
def bidding_records():
    query = Bidding_fishes.query.filter_by(seller_id=session['userid']).all()
    bid_data=[]
    user_data =[]
    seller = Seller_Registion.query.filter_by(id=session['userid']).first()
    for data in query:
        if data.user_id !=0:
            bidding = Bidding_fishes.query.filter_by(user_id = data.user_id).first()
            bid_data.append(bidding)
            user= User_Register.query.filter_by(id = data.user_id).first()
            user_data.append(user)
    return render_template("seller_view_bidding_details.html",bidding = zip(bid_data,user_data),seller=seller)


# billing page
@app.route('/seller/billing')
def billing_home():
    id = session['userid']
    seller = Seller_Registion.query.filter_by(id=id).first()
    fishes = BuyedProducts.query.filter_by(seller_id=id, sucess=1).all()
    generate_user_id=[]
    issuing_user_id=[]
    for fish in fishes:

        if fish.user_id not in generate_user_id:
            generate_user_id.append(fish.user_id)
    user = len(generate_user_id)
    buyed_fish = BuyedProducts.query.filter_by(seller_id=id, sucess=2).all()
    for fishs in buyed_fish:
        if fishs.user_id not in issuing_user_id:
            issuing_user_id.append(fishs.user_id)
    issuing = len(issuing_user_id)
    return  render_template("seller_billing_page.html",seller= seller,user=user,issuing=issuing)

@app.route('/seller/billing/issue_billing')
def issue_billing():
    id = session['userid']
    seller = Seller_Registion.query.filter_by(id=id).first()
    fishes = BuyedProducts.query.filter_by(seller_id=id, sucess=1).all()

    user_ids=[]
    count_fish=[]
    user_data=[]
    for fish in fishes:
        if fish.user_id not in user_ids:
            user_ids.append(fish.user_id)
    for ids in user_ids:
        #  name, email, place,fish_nos, issue_bill
        count_fishes = BuyedProducts.query.filter_by(seller_id=id, sucess=1,user_id=ids).all()
        count_fish.append(len(count_fishes))
        user = User_Register.query.filter_by(id=ids).first()
        user_data.append(user)

    return render_template("seller_issue_bill.html",seller= seller,data=zip(user_data,count_fish))

@app.route('/seller/billing/issue_billing/generate',methods=['GET','POST'])
def generate_bill():
    if request.method == 'POST':
        user_id = request.form['user_id']
        seller_id = session['userid']
        all_fish=[]
        total_amount=[]
        number=[]
        fishes = BuyedProducts.query.filter_by(seller_id=seller_id, sucess=1,user_id=user_id).all()
        num=0
        for fish in fishes:
            fisheries= Fisheries.query.filter_by(id=fish.product_id).first()
            all_fish.append(fisheries)
            price = fisheries.price
            offer = fisheries.offer
            result = round((price / 100) * (100 - offer))
            total_amount.append(result)

            num+=1
            number.append(num)
            # update data

            fish.sucess = 2
            db.session.commit()
        user = User_Register.query.filter_by(id=user_id).first()
        seller = Seller_Registion.query.filter_by(id=seller_id).first()
        today = date.today()
        return render_template("invoice_generation.html",user=user,seller=seller, date=today,
                               fishes=zip(number,all_fish,total_amount), total = sum(total_amount))


@app.route('/seller/billing/sent')
def sent_bill():
    id = session['userid']
    issuing_user_id=[]
    all_users =[]
    all_fish=[]
    buyed_fish_id=[]
    buyed_fish = BuyedProducts.query.filter_by(seller_id=id, sucess=2).all()
    for fishs in buyed_fish:
        if fishs.user_id not in issuing_user_id:
            issuing_user_id.append(fishs.user_id)
            buyed_fish_id.append(fishs)

    for users in issuing_user_id:
        user = User_Register.query.filter_by(id=users).first()
        all_users.append(user)
        fishes = BuyedProducts.query.filter_by(seller_id=id, sucess=2,user_id=users).all()
        all_fish.append(len(fishes))

    seller = Seller_Registion.query.filter_by(id=id).first()
    return  render_template("seller_sent_bill.html",seller = seller, data = zip(all_users,all_fish,buyed_fish_id))


@app.route('/seller/billing/sent/sucess',methods=['GET','POST'])
def sent_bill_sucess():
    if request.method == 'POST':
        user_id = request.form['user_id']
        seller = session['userid']
        buyed_product = BuyedProducts.query.filter_by(user_id=user_id,sucess=2,seller_id=seller).all()
        for buyed_product in buyed_product:
            buyed_product.sucess=3
            db.session.commit()
        return redirect('/seller/billing/sent')

@app.route('/product_detail/shop', methods=['GET','POST'])
def shop_now():
    if 'userid'  in session:
        if request.method=='POST':
            user_id = session['userid']
            product_id = request.form['product_id']
            product=Fisheries.query.filter_by(id=product_id).first()
            seller_id=product.seller_id
            details=0
            phone=0
            success=0
            fisheries=[]
            total_amount=[]
            query = BuyedProducts(product_id=product_id,user_id=user_id,seller_id=seller_id,details=details,phone=phone, sucess=success)
            db.session.add(query)
            db.session.commit()
            user= User_Register.query.filter_by(id=user_id).first()

            buys = BuyedProducts.query.filter_by(user_id=user_id,sucess=0).all()

            items=0
            for buy in buys:
                items+=1
                fish = Fisheries.query.filter_by(id=buy.product_id).first()
                fisheries.insert(0,fish)
                price = fish.price
                offer = fish.offer
                result = round((price / 100) * (100 - offer))
                total_amount.append(result)
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
            encode = jinja_env.filters['b64encode'] = b64encode
            decode = jinja_env.filters['b64decode'] = b64decode
            # amout = sum(total_amount), items = len(buy)
            return render_template("user_shop.html",data=zip(fisheries,buys),user_data=user,encode=encode,decode=decode,
                               amount = sum(total_amount), items = items)
        else:
            user_id = session['userid']
            fisheries = []
            total_amount = []
            user = User_Register.query.filter_by(id=user_id).first()

            buys = BuyedProducts.query.filter_by(user_id=user_id, sucess=0).all()
            print(buys)
            items = 0
            for buy in buys:
                items += 1
                fish = Fisheries.query.filter_by(id=buy.product_id).first()
                fisheries.insert(0, fish)
                price = fish.price
                offer = fish.offer
                result = round((price / 100) * (100 - offer))
                total_amount.append(result)
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
            encode = jinja_env.filters['b64encode'] = b64encode
            decode = jinja_env.filters['b64decode'] = b64decode
            # amout = sum(total_amount), items = len(buy)

            return render_template("user_shop.html", data=zip(fisheries, buys), user_data=user, encode=encode,decode=decode,
                                   amount=sum(total_amount), items=items)
    else:
        print("redirexct")
        return redirect('/signin')

@app.route('/product_detail/shop/remove', methods=['GET','POST'])
def remove_shop():
    if request.method=='POST':
        shop_id=request.form['shop_id']
        data = BuyedProducts.query.filter_by(id=shop_id).first()
        db.session.delete(data)
        db.session.commit()
        return  redirect('/product_detail/shop')

@app.route('/product_detail/shop/ordered',methods=['GET','POST'])
def sucessfully_ordered():
    if request.method=='POST':
        user_id= session['userid']
        address= request.form['address']
        print(address)
        phone= request.form['phone']
        buyed = BuyedProducts.query.filter_by(user_id=user_id, sucess=0).all()
        print(buyed)
        for buy in buyed:
            update=BuyedProducts.query.filter_by(id=buy.id).first()
            update.details=address
            update.phone=phone
            update.sucess=1
            product_id = update.product_id
            seller_id = update.seller_id
            feedback = FeedBack(user_id=user_id, seller_id=seller_id,product_id=product_id, feedback=0, rating=0, verify=0)
            db.session.add(feedback)
            db.session.commit()
        user = User_Register.query.filter_by(id=user_id).first()
        flash("Successfully ordered !.. ")
        return redirect('/view_orders')

@app.route('/charge', methods=['POST'])
def app_charge():
    amount = int(request.form['amount'])*100
    payment_id = request.form['razorpay_payment_id']
    razorpay_client.payment.capture(payment_id, amount)
    return json.dumps(razorpay_client.payment.fetch(payment_id))


@app.route('/cart', methods=['GET','POST'])
def cart():
    if 'userid' in session :
        if request.method=='POST':
            product_id = request.form['product_id']
            user_id = g.res
            print(f"cart: {g.res}")
            query = Cart(product_id= product_id, user_id= user_id)
            db.session.add(query)
            db.session.commit()
            return redirect('/user_cart')
    else:
        return  redirect('/signin')

@app.route('/user_cart')
def user_cart():
    if 'userid' in session:
        if request.method=="POST":
            user_id = session['userid']
            cart = Cart.query.filter_by(user_id=user_id).all()
            list1 = []
            for x in cart:
                data = Fisheries.query.filter_by(id=x.product_id).first()
                list1.insert(0, data)
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
            encode = jinja_env.filters['b64encode'] = b64encode
            decode = jinja_env.filters['b64decode'] = b64decode

            id = session['userid']
            user_data = User_Register.query.filter_by(id=id).first()
            return render_template("User_cart.html", list1=list1, encode=encode, decode=decode,user_data=user_data)
        else:
            user_id = session['userid']
            cart = Cart.query.filter_by(user_id=user_id).all()
            # print(cart)
            list1=[]
            list2=[]
            for x in cart:
                data=Fisheries.query.filter_by(id=x.product_id).first()
                if data is not None:
                    print(data)
                    print(x.product_id)
                    list1.insert(0,data)
                    price = data.price
                    offer = data.offer
                    result = round((price/100)*(100-offer))
                    list2.append(result)
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
            encode = jinja_env.filters['b64encode'] = b64encode
            decode = jinja_env.filters['b64decode'] = b64decode
            id = session['userid']
            user_data = User_Register.query.filter_by(id=id).first()
            return render_template("User_cart.html", list1=list1, encode=encode, decode=decode, total_length=len(cart),total=sum(list2), delivery_charge=20,user_data=user_data)
    else:
        flash("you are not yet login..")
        return redirect('/signin')

@app.route('/user_cart/remove', methods=['GET','POST'])
def remove_cart_data():
    if request.method=='POST':
        id= request.form['remove']
        # print(id)
        data = Cart.query.filter_by(product_id=id).first()
        db.session.delete(data)
        db.session.commit()
        return redirect('/user_cart')

@app.route('/user_cart/go_to_shop',methods=['GET','POST'])
def go_to_shop():
    if request.method=='POST':
        user_id= session['userid']
        cart = Cart.query.filter_by(user_id=user_id).all()
        for data in cart:
            fish = Fisheries.query.filter_by(id= data.product_id).first()
            if fish is not None:
                seller_id= fish.seller_id
                product_id=fish.id
                details = 0
                phone = 0
                success = 0
                fisheries = []
                total_amount = []
                query = BuyedProducts(product_id=product_id, user_id=user_id, seller_id=seller_id, details=details,
                                      phone=phone, sucess=success)
                db.session.add(query)
                db.session.delete(data)
                db.session.commit()
        user = User_Register.query.filter_by(id=user_id).first()

        buys = BuyedProducts.query.filter_by(user_id=user_id, sucess=0).all()

        items = 0
        for buy in buys:
            items += 1
            fish = Fisheries.query.filter_by(id=buy.product_id).first()
            fisheries.insert(0, fish)
            price = fish.price
            offer = fish.offer
            result = round((price / 100) * (100 - offer))
            total_amount.append(result)
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        # amout = sum(total_amount), items = len(buy)
        return render_template("user_shop.html", data=zip(fisheries, buys), user_data=user, encode=encode,decode=decode,
                                   amount=sum(total_amount), items=items)




@app.route('/product_detail', methods=['GET','POST'])
def product_details():
    if request.method=='POST':
        id = request.form['product_id']
        data = Fisheries.query.filter_by(id=id).first()
        seller = Seller_Registion.query.filter_by(id=data.seller_id).first()
        suggest = Fisheries.query.order_by(Fisheries.id.desc()).all()
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        if 'userid' in session:
            sid = session['userid']
            user_data = User_Register.query.filter_by(id=sid).first()
            return render_template("productdetails.html", data= data,encode=encode, decode=decode, suggestion=suggest,user_data=user_data,seller =seller)
        return render_template("productdetails.html", data= data,encode=encode, decode=decode, suggestion=suggest,user_data=0,seller=seller)


# user bidding section


@app.route('/bidding')
def bidding():
    if 'userid' in session:
        id = session['userid']
        seller_id=[]
        # data = Bidding_fish.query.filter_by(date_joined=date.today()).all()
        data = Bidding_fishes.query.filter_by(date_joined = date.today()).all()
        print(f"data : {data}")
        for sid in data:
            seller=Seller_Registion.query.filter_by(id=sid.seller_id).first()
            seller_id.append(seller)
        print(data)
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        user = User_Register.query.filter_by(id=id).first()
        print(f"user {user}")

        return render_template("user_view_bidding_fisheries.html",user_data=user,data=zip(data,seller_id),
                               encode=encode, decode= decode,length = len(data))
    else:
        return  redirect('/signin')

bid_id=[]

@app.route('/bidding/enter_bidding',methods=['GET','POST'])
def enter_bidding():
    myobj = datetime.now()
    if request.method=='POST':
        if len(bid_id) > 0:
            bid_id.clear()
        user_id = session['userid']
        seller_id = request.form['seller']
        bidding_id = request.form['bid']
        bid_id.append(bidding_id)
        bid_id.append(seller_id)
        seller = Seller_Registion.query.filter_by(id=seller_id).first()
        user = User_Register.query.filter_by(id=user_id).first()
        print(user)
        entry = bool(Bidding_entry.query.filter_by(user_id=user_id).first())
        bid_fish = Bidding_fishes.query.filter_by(id = bidding_id).first()
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        # date = timee[1] + " " + timee[2] + " ," + timee[0] + " 23:50:00"
        t=str(bid_fish.time).split(":")
        t_str = str(int(t[1])+3)

        date = timee[1] + " " + timee[2] + " ," + timee[0] + " "+ t[0] +":"+t_str+":00"
        print(date)
        if bid_fish.user_id == 0:
            uname = user.name
            uaddress= user.Address
            uphone = user.phone
        else:
            uname = user.name
            uaddress = bid_fish.user_address
            uphone = bid_fish.user_phone
        bidder_entry = Bidding_entry.query.filter_by(seller_id=seller_id).all()
        recent_bidder = []
        if len(bidder_entry) > 4:
            for x in range(4):
                entry = random.choice(bidder_entry)
                users = User_Register.query.filter_by(id=entry.user_id).first()
                recent_bidder.append(users)
        else:
            for x in bidder_entry:
                users = User_Register.query.filter_by(id=x.user_id).first()
                recent_bidder.append(users)
        print(f" recent :{recent_bidder}")
        cur_min = myobj.minute
        cur_hour = myobj.hour
        print(f"min {int(t[1])} ,hour {int(t[0])}, cur_min {cur_min}, cur_hour {cur_hour}")
        if entry:
            return render_template("user_enter_bidding.html",user_data=user, name = uname,adress=uaddress,phone=uphone,encode=encode, decode= decode,
                                   fish =bid_fish,seller= seller,date=date,recent = recent_bidder,hour=int(t[0]),min = int(t[1]),cur_min=cur_min,cur_hour=cur_hour)
        else:
            query = Bidding_entry(user_id=user_id, seller_id=seller_id, bidding_id=bidding_id)
            db.session.add(query)
            db.session.commit()
            return render_template("user_enter_bidding.html",user_data=user, name = uname,adress=uaddress,phone=uphone,encode=encode, decode= decode,
                                   fish=bid_fish,seller= seller,date=date,recent = recent_bidder,hour=int(t[0]),min = int(t[1]),cur_min=cur_min,cur_hour=cur_hour)
    else:
        print(bid_id)
        user_id = session['userid']
        bidding_id = bid_id[0]
        seller_id= bid_id[1]
        seller = Seller_Registion.query.filter_by(id=seller_id).first()
        user = User_Register.query.filter_by(id=user_id).first()
        print(user)
        # entry = bool(Bidding_entry.query.filter_by(user_id=user_id).first())
        bid_fish = Bidding_fishes.query.filter_by(id=bidding_id).first()
        if bid_fish.user_id == 0:
            uname = user.name
            uaddress= user.Address
            uphone = user.phone
        else:
            uname = user.name
            uaddress = bid_fish.user_address
            uphone = bid_fish.user_phone
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        encode = jinja_env.filters['b64encode'] = b64encode
        decode = jinja_env.filters['b64decode'] = b64decode
        # date = timee[1] + " " + timee[2] + " ," + timee[0] + " 23:50:00"
        t = str(bid_fish.time).split(":")
        print(f"timezzzz{t}")
        t_str = str(int(t[1]) + 3)
        bidder_entry = Bidding_entry.query.filter_by(seller_id=seller_id).all()
        recent_bidder = []
        if len(bidder_entry) > 4:
            for x in range(4):
                entry = random.choice(bidder_entry)
                users = User_Register.query.filter_by(id=entry.user_id).first()
                recent_bidder.append(users)
        else:
            for x in bidder_entry:
                users = User_Register.query.filter_by(id=x.user_id).first()
                recent_bidder.append(users)
        print(f" recent :{recent_bidder}")
        date = timee[1] + " " + timee[2] + " ," + timee[0] + " " + t[0] + ":" + t_str + ":00"
        print(date)
        cur_min = myobj.minute
        cur_hour  = myobj.hour
        print(f"min {int(t[1])} ,hour {int(t[0])}, cur_min {cur_min}, cur_hour {cur_hour}")
        return render_template("user_enter_bidding.html",user_data=user, name = uname,adress=uaddress,phone=uphone, encode=encode, decode=decode, fish=bid_fish,
                               seller=seller,date=date,recent = recent_bidder,hour=int(t[0]),min = int(t[1]),cur_min=cur_min,cur_hour=cur_hour)


@app.route('/bidding/enter_bidding/amount',methods=['GET','POST'])
def enter_bidding_amount():
    if request.method == 'POST':
        user_address = request.form['user_address']
        user_phone = request.form['user_phone']
        amount = int(request.form['amount'])
        bid_id = request.form['bid_id']
        user_id = session['userid']
        bid_fish = Bidding_fishes.query.filter_by(id=bid_id).first()
        if bid_fish.highest_bid < amount:
            bid_fish.user_id = user_id
            bid_fish.highest_bid = amount
            bid_fish.user_address=user_address
            bid_fish.user_phone = user_phone
            db.session.commit()
            return redirect('/bidding/enter_bidding')
        else:
            return redirect('/bidding/enter_bidding')


@app.before_request
def beforerequest():
    if "userid" in session:
        g.res=session['userid']
        print(f"before request--{g.res}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)

