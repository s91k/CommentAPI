import datetime
from flask import Flask, request,jsonify
from model import db, Comment
from config import DevelopmentConfig, ProductionConfig
from flask_migrate import Migrate
import os

app = Flask(__name__)
if os.getenv('RUNENVIRONMENT') == "Production":
    app.config.from_object(ProductionConfig())
else:
    app.config.from_object(DevelopmentConfig())

db.app = app 
db.init_app(app)
migrate = Migrate(app,db)


@app.route("/")
def start():
    s = "<html><head><title>Test</title></head><body><h1>Test</h1></body></html>"
    return s

@app.route("/api/comment", methods=["POST"])
def apiCreateComment():
    data = request.get_json()
    c = Comment()
    c.Name = data["Name"]
    c.Text = data["Text"]
    c.DateTime = datetime.datetime.now()
    db.session.add(c)
    db.session.commit()
    return jsonify({ "Id": c.Id, 
                    "Name":c.Name, 
                    "DateTime":c.DateTime,
                    "Text":c.Text }), 201

@app.route("/api/comments")
def apiComments():
    comments = []
    for c in Comment.query.all():
        cdict = { "Id": c.Id, 
                 "Name":c.Name, 
                 "DateTime":c.DateTime,                
                 "Text":c.Text }
        comments.append(cdict)
 
    return jsonify(comments)    

@app.route("/api/latest_comments")
def apiLatestComments():
    data = request.get_json()

    maxNrOfComments = 10

    if "Max" in data:
        maxNrOfComments = data["Max"]

    comments = []

    for c in Comment.query.order_by(Comment.DateTime).limit(maxNrOfComments):
        cdict = { "Id": c.Id, 
                 "Name":c.Name, 
                 "DateTime":c.DateTime,                
                 "Text":c.Text }
        comments.append(cdict)
 
    return jsonify(comments)    

with app.app_context():
    db.create_all()
    app.run()