import datetime
import re
from flask import Flask, request,jsonify
from model import db, Comment
from config import DevelopmentConfig, ProductionConfig
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app)

if os.getenv('RUNENVIRONMENT') == "Production":
    app.config.from_object(ProductionConfig())
else:
    app.config.from_object(DevelopmentConfig())

db.app = app 
db.init_app(app)
migrate = Migrate(app,db)

# Used to remove HTML tags from text
htmlRemover = re.compile(r'<.*?>')

# Routes
# Start page for testing
@app.route("/")
def start():
    s = "<html><head><title>Test</title></head><body><h1>Test</h1></body></html>"
    return s

# Create a comment
@app.route("/api/comment", methods=["POST"])
@cross_origin()
def apiCreateComment():
    data = request.get_json()
    c = Comment()
    c.Name = re.sub(htmlRemover, '', data["name"])
    c.Text = re.sub(htmlRemover, '', data["text"])
    c.DateTime = datetime.datetime.now()
    db.session.add(c)
    db.session.commit()
    return jsonify({ "Id": c.Id, 
                    "Name":c.Name, 
                    "DateTime":c.DateTime,
                    "Text":c.Text }), 201

# Get all comments
@app.route("/api/comments")
@cross_origin()
def apiComments():
    comments = []
    for c in Comment.query.all():
        cdict = { "id": c.Id, 
                 "name":c.Name, 
                 "datetime":c.DateTime,                
                 "text":c.Text }
        comments.append(cdict)
 
    return jsonify(comments)    

# Get the latest comments based on the Max parameter
@app.route("/api/latest_comments")
@cross_origin()
def apiLatestComments():
    data = request.args

    maxNrOfComments = 10

    if "max" in data:
        maxNrOfComments = int(data["max"])

    comments = []

    for c in Comment.query.order_by(Comment.DateTime).limit(maxNrOfComments):
        cdict = { "id": c.Id, 
                 "name":c.Name, 
                 "datetime":c.DateTime,                
                 "text":c.Text }
        comments.append(cdict)
 
    return jsonify(comments)    

with app.app_context():
    db.create_all()
    app.run()