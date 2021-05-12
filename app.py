"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

connect_db(app)
db.create_all()

@app.route("/")
def root():
    return render_template("index.html")

@app.route('/api/cupcakes')
def getData():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:c_id>')
def getCupcake(c_id):
    cupcake = Cupcake.query.get_or_404(c_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes", methods=["POST"])
def createCupcake():
    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:c_id>", methods=["PATCH"])
def updateCupcake(c_id):
    data = request.json
    cupcake = Cupcake.query.get_or_404(c_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:c_id>", methods=["DELETE"])
def deleteCupcake(c_id):
    cupcake = Cupcake.query.get_or_404(c_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

