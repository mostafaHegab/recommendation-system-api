import os
from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
app =Flask(__name__)
mail = Mail(app)
app.config['DEBUG']=True
app.config['TESTING']=False
app.config['MAIL_SERVER']='smtp.hushmail.com'
app.config['MAIL_PORT'] = 587

#app.config['MAIL_DEFAULT_SENDER']='anything@prettyprinted.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_ASCII_ATTACHMENTS']=False
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app) 
   
# message object mapped to a particular URL ‘/’ 
@app.route("/") 
def index(): 
   msg = Message(' ',sender =['anything@prettyprinted.com'], recipients =['alyxandra285@cybergfl.com']) 
   msg.body='fjjgjgjjfjkdd'
   mail.send(msg) 
   
   return 'Sent'
   
if __name__ == '__main__': 
   app.run() 