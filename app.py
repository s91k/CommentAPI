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

    if c.Name == "" or c.Text == "":
        return jsonify({ "error": "name and text cannot be empty" }), 400

    c.DateTime = datetime.datetime.now()
    db.session.add(c)
    db.session.commit()
    return jsonify({ "Id": c.Id, 
                    "Name":c.Name, 
                    "DateTime":c.DateTime,
                    "Text":c.Text }), 201

# Get a comment by id
@app.route("/api/comment/<int:id>")
@cross_origin()
def apiGetComment(id):
    c = Comment.query.get(id)
    if c == None:
        return jsonify({ "error": "comment not found" }), 404

    return jsonify({ "id": c.Id, 
                    "name":c.Name, 
                    "dateTime":c.DateTime,
                    "text":c.Text })

# Update a comment by id
@app.route("/api/comment/<int:id>", methods=["PUT"])
@cross_origin()
def apiUpdateComment(id):
    data = request.get_json()
    c = Comment.query.get(id)
    if c == None:
        return jsonify({ "error": "comment not found" }), 404

    c.Name = re.sub(htmlRemover, '', data["name"])
    c.Text = re.sub(htmlRemover, '', data["text"])

    if c.Name == "" or c.Text == "":
        return jsonify({ "error": "name and text cannot be empty" }), 400

    db.session.commit()
    return jsonify({ "id": c.Id, 
                    "name":c.Name, 
                    "dateTime":c.DateTime,
                    "text":c.Text })

# Delete a comment by id
@app.route("/api/comment/<int:id>", methods=["DELETE"])
@cross_origin()
def apiDeleteComment(id):
    c = Comment.query.get(id)
    if c == None:
        return jsonify({ "error": "comment not found" }), 404

    db.session.delete(c)
    db.session.commit()
    return jsonify({ "id": c.Id, 
                    "name":c.Name, 
                    "dateTime":c.DateTime,
                    "text":c.Text })

# Get a list of comments, with optional parameters for ordering and limiting the number of results
@app.route("/api/comments")
@cross_origin()
def apiComments():
    query = Comment.query

    if "order" in request.args:
        if request.args["order"] == "asc":
            query = query.order_by(Comment.DateTime)
        elif request.args["order"] == "desc":
            query = query.order_by(Comment.DateTime.desc())

    if "max" in request.args:
        queryResults = query.limit(int(request.args["max"]))
    else:
        queryResults = query.all()

    comments = []
    for c in queryResults:
        cdict = { "id": c.Id, 
                 "name":c.Name, 
                 "datetime":c.DateTime,                
                 "text":c.Text }
        comments.append(cdict)
 
    return jsonify(comments)    

with app.app_context():
    db.create_all()
    app.run()