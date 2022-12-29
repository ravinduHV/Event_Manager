from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from cs50 import SQL
import random
from helper import login_required
from User import User

from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.jinja_env.add_extension('jinja2.ext.do') #Check for this-- no longer will needed

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///manager.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    try:
        events = db.execute("SELECT name, description, id FROM events WHERE user_id=?", session["user_id"])
    except:
        events=[]
    return render_template("index.html", events=events)


@app.route("/new_event" ,methods=["GET","POST"])
@login_required
def new_event():
    if request.method == "POST":
        name = request.form.get("project_name")
        catagory = request.form.get("catagory")
        starting_date = request.form.get("starting_date")
        ending_date = request.form.get("ending_date")
        description = request.form.get("description")

        if not name or not catagory or not starting_date or not ending_date or not description:
            flash("Enter Correct Details!")
            return redirect("/new_event")
        else:
            id_list = db.execute("SELECT id FROM events")
            while True:
                id = random.randint(1000,9999)
                if str(id) not in id_list:
                    db.execute("INSERT INTO events (name, catagory, starting_date, ending_date, description, id, user_id) VALUES(?,?,?,?,?,?,?)", name, catagory, starting_date, ending_date, description,id, int(session["user_id"]))        
                    break
            
        return redirect("/")
    else:
        return render_template("new_event.html")


@app.route("/event", methods=["GET", "POST"])
@login_required
def event():
    if request.method == "POST":
        if request.form.get("insert_form") == "save":
            id = request.form.get("id")
            income_expenditure = int(request.form.get("income_expenditure")) # return integer 1 or 2::::: try to do it else error can happen
            _type = request.form.get("type")
            item = request.form.get("item")
            units = request.form.get("units")
            unit_price = request.form.get("unit_price")
            date = request.form.get("date")

            if not id or not income_expenditure or not _type or not item or not unit_price or not date:
                flash("Mandatory fields should not be empty ")
                return redirect(("/event?id="+id))

            if income_expenditure == 1 and not units:
                units = 1 

            #checks for data
            try:
                units = float(units)
                unit_price = float(unit_price)
            except:
                flash("Units and Unit_price [DATA UNMATCH]")
                return redirect(("/event?id="+id))
            
            #check for valied date by separating and check with regex

            #update tables
            if income_expenditure == 1:
                db.execute("INSERT INTO budget_income (project_id, type, item, amount, units, date) VALUES(?, ?, ?, ?, ?, ?)", int(id), _type, item, unit_price, units, date)
            elif income_expenditure == 2:
                db.execute("INSERT INTO budget_expenditure (project_id, type, item, amount, units, date) VALUES(?, ?, ?, ?, ?, ?)", int(id), _type, item, unit_price, units, date)


            return redirect(("/event?id="+id)) 
        elif request.form.get("delete_row") == "delete":
            id = request.form.get("id")
            row_id = request.form.get("row_id")
            _type = request.form.get("db")
            if _type == "income":
                db.execute("DELETE FROM budget_income WHERE id=?", int(row_id))
            elif _type == "expenditure":
                db.execute("DELETE FROM budget_expenditure WHERE id=?", int(row_id))
            return redirect(("/event?id="+id))
    else:
        id = request.args
        if not id["id"]:
            return redirect("/")
        project = db.execute("SELECT * FROM events WHERE id=?", id["id"])
        income_details = sorted(db.execute("SELECT * FROM budget_income WHERE project_id=?", int(id["id"]) ), key=lambda x: x["date"])
        expenditure_details = sorted(db.execute("SELECT * FROM budget_expenditure WHERE project_id=?", int(id["id"]) ), key=lambda x: x["date"])
        
        catagory=[]
        for _ in income_details:
            catagory.append(_["type"])
        for _ in expenditure_details:
            catagory.append(_["type"])

        return render_template("event.html", project=project, catagory=set(catagory), income=income_details, expenditure=expenditure_details)

@app.route("/login", methods=["POST","GET"])
def login():
    session.clear()
    if request.method == "POST":
        u_name_or_email = request.form.get("username_email")
        password = request.form.get("password")

        if not u_name_or_email or not password:
            return redirect("/login")
        if "@" in u_name_or_email:
            row = db.execute("SELECT hash,id FROM users WHERE email=?", u_name_or_email)
        else:    
            row = db.execute("SELECT hash,id FROM users WHERE user_name=?", u_name_or_email)

        if len(row) != 1 or not check_password_hash(row[0]["hash"], password):
            return redirect("/login")
        session["user_id"] = int(row[0]["id"])
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        c_password = request.form.get("c_password")
        tp_no = request.form.get("tp_no")
        info = db.execute("SELECT * FROM users WHERE user_name=?",username)
        try:
            user = User(username, email, password, c_password, tp_no, info)
            db.execute("INSERT INTO users (user_name, email, hash, contact_no) VALUES(?, ?, ?, ?)", user.name, user.email, generate_password_hash(user.password), user.tp_no)
        except:
            raise
            #return redirect("/register")
        id = db.execute("SELECT id FROM users WHERE user_name=?", user.name)
        print(id)
        session["user_id"] = id[0]
        return redirect("/")
    else:
        session.clear()
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
