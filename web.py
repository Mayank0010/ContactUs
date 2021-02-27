from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ContactUs'
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = 'contact form'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mayank.nitt.00@gmail.com'
app.config['MAIL_PASSWORD'] = 'nitt12345'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

class Contact(db.Model):
    SNo = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Number = db.Column(db.String(10), unique=True, nullable=False)
    Subject = db.Column(db.String(80), unique=False, nullable=False)
    Message = db.Column(db.String(200), unique=False, nullable=False)
    Date = db.Column(db.String(12), unique=True, nullable=True)

@app.route("/")
def index():
    return render_template("contact.html")

@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
       name= request.form.get('name')
       email= request.form.get('email')
       number= request.form.get('number')
       subject= request.form.get('subject')
       message= request.form.get('message')

       entry = Contact(Name= name, Email=email, Number=number, Subject=subject, Message=message, Date=datetime.now()  )
       db.session.add(entry)
       db.session.commit()
       flash('Your form is successfully submitted. We will contact you soon..')
       mail.send_message('New message', 
                           sender= email, 
                           recipients = ['mayank.nitt.00@gmail.com'],
                           body = "Name: " + name + "\n" 
                           + "Email: " + email + "\n" 
                           + "Mobile Number: " + number + "\n" 
                           +  "Subject: " + subject + "\n" 
                           + "Message/Query: " + message)
       
    return render_template('contact.html')
    
    
if __name__ == '__main__':
    app.run(debug=True)
