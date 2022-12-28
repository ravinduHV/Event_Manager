from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from cs50 import SQL
import random


app = Flask(__name__)

app.jinja_env.add_extension('jinja2.ext.do')

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
def index():
    events = db.execute("SELECT name, description, id FROM events")
    return render_template("index.html", events=events)

@app.route("/new_event" ,methods=["GET","POST"])
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
                    db.execute("INSERT INTO events (name, catagory, starting_date, ending_date, description, id) VALUES(?,?,?,?,?,?)", name, catagory, starting_date, ending_date, description,id)        
                    break
            
        return redirect("/")
    else:
        return render_template("new_event.html")

@app.route("/event", methods=["GET", "POST"])
def event():
    if request.method == "POST":
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
    else:
        id = request.args
        if not id["id"]:
            return redirect("/")
        project = db.execute("SELECT * FROM events WHERE id=?", id["id"])
        income_catagory = db.execute("SELECT type FROM budget_income WHERE project_id=?", int(id["id"]))
        expenditure_catagory = db.execute("SELECT type FROM budget_expenditure WHERE project_id=?", int(id["id"]))

        income_details = sorted(db.execute("SELECT * FROM budget_income WHERE project_id=?", int(id["id"]) ), key=lambda x: x["date"])
        expenditure_details = sorted(db.execute("SELECT * FROM budget_expenditure WHERE project_id=?", int(id["id"]) ), key=lambda x: x["date"])
        
        catagory=[]
        for _ in income_details:
            catagory.append(_["type"])
        for _ in expenditure_details:
            catagory.append(_["type"])

        return render_template("event.html", project=project, catagory=set(catagory), income=income_details, expenditure=expenditure_details)