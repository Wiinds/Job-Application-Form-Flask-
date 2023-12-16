from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message


import os

password = os.getenv("PROJECTSHOWCASE")

app = Flask(__name__)
#* Parameters of the database being made and email
app.config["SECRET_KEY"] = "toast"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "jeremyabraham17@gmail.com"
app.config["MAIL_PASSWORD"] = password

db = SQLAlchemy(app)

mail = Mail(app)

class Form(db.Model):
    #* Making the database model 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))
    

@app.route("/", methods=["GET","POST"])
def index():
    #* Get the data from the user inputs
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_object = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]
        #* This allows the data to be added to the database 
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_object, occupation=occupation)
        db.session.add(form)
        db.session.commit()
        message_body = f"{first_name}, This is to confirm that your submission was recieved by us."
        message = Message(subject="New Form Submission", sender=app.config["MAIL_USERNAME"],
                          recipients=[email], body=message_body)
        
        mail.send(message)
        
        flash(f"Thank you {first_name}, Your form was submitted successfully.", "success")
        
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)





