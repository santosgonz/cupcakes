"""Flask app for Cupcakes"""
from flask import Flask, request, render_template,  redirect, flash, session, jsonify
from models import db,  connect_db, Cupcake
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretlmao123123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

@app.route('/')
def index_page():
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes')
def cupcakes():
    all_cupcakes = [cupcakes.serialize() for cupcakes in Cupcake.query.all()]
    return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcakes(id):
    cupcakes = Cupcake.query.get_or_404 (id)
    return jsonify(cupcakes = cupcakes.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    new_cupcake = Cupcake(flavor=request.json["flavor"],
                          size=request.json["size"],
                          rating=request.json["rating"],
                          image = request.json["image"])
    db.session.add(new_cupcake)
    db.session.commit()
    return (jsonify(cupcakes = new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    cupcakes = Cupcake.query.get_or_404(id)
    ##Getting each individual object from class, the 2nd part is to set as default in case developer only needs to change one thing
    cupcakes.flavor = request.json.get('flavor', cupcakes.flavor)
    cupcakes.size = request.json.get('size', cupcakes.size)
    cupcakes.rating = request.json.get('rating', cupcakes.rating)
    cupcakes.image = request.json.get('image', cupcakes.image)
    db.session.commit()
    return jsonify(cupcakes=cupcakes.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcakes = Cupcake.query.get_or_404(id)
    db.session.delete(cupcakes)
    db.session.commit()
    ##reminder to self the first part message is object amd deleted is key
    return jsonify(message="deleted")