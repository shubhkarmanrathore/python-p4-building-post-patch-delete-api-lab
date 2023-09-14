#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>', methods = ["GET", "PATCH"])
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    if request.method == 'GET':

        bakery_serialized = bakery.to_dict()

        response = make_response(
            bakery_serialized,
            200
        )
        return response
    
    elif request.method == "PATCH":
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))
        db.session.add(bakery)
        db.session.commit()

        dict = bakery.to_dict()

        response = make_response(jsonify(dict), 200)

        return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

@app.route('/baked_goods/<int:id>', methods = ['GET', 'DELETE'])
def baked_good_by_id(id):
    good = BakedGood.query.filter(BakedGood.id == id).first()
    if request.method == 'GET':
        dict = good.to_dict()
        
        response = make_response(jsonify(dict), 200)
        return response
    elif request.method == "DELETE":
        db.session.delete(good)
        db.session.commit()
        response_body = {
            "delete successfull": True,
            "message": "The good has been deleted."
        }

        response = make_response(response_body, 200)
        return response
    
@app.route('/baked_goods', methods = ['GET', 'POST'])
def post_good():
    if request.method == "GET":
        baked_goods = []
        for goods in BakedGood.query.all():
            dict = goods.to_dict()
            baked_goods.append(dict)
        response = make_response(jsonify(baked_goods), 200)
        return response
    elif request.method == "POST":
        new_good = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            bakery_id=request.form.get("bakery_id")
        )

        db.session.add(new_good)
        db.session.commit()

        dict = new_good.to_dict()
        response = make_response(jsonify(dict), 201)
        return response
           


if __name__ == '__main__':
    app.run(port=5555, debug=True)
