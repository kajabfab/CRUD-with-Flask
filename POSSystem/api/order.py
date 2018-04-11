from flask import Blueprint, request, Response, json
from datetime import datetime
from models import db, Order, Product

order_blueprint = Blueprint('order_blueprint', __name__)


@order_blueprint.route('/orders/', methods=['POST'])
def create():
    data = request.get_json()
    order = Order(
        customer_id=data['customer_id'],
        date=datetime.strptime(data['date'], "%d/%m/%Y"),
        total=data['total']
    )
    for product_id in data['products']:
        product = Product.query.filter_by(id=product_id).first()
        order.products.append(product)
    db.session.add(order)
    db.session.commit()

    return Response(
        json.dumps({'message': 'Successfully created a new order'}),
        status=201,
        mimetype='application/json'
    )


@order_blueprint.route('/orders/', methods=['GET'])
@order_blueprint.route('/orders/<int:id>', methods=['GET'])
def read(id=None):
    if id:
        order = Order.query.filter_by(id=id).first()
        return Response(
            json.dumps(order.serialize()),
            status=200,
            mimetype='application/json'
        )
    else:
        orders = Order.query.all()
        return Response(
            json.dumps([o.serialize() for o in orders]),
            status=200,
            mimetype='application/json'
        )


@order_blueprint.route('/orders/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    Order.query.filter_by(id=id).update(data)
    db.session.commit()
    return Response(
        json.dumps({'message': 'Successfully updated the order'}),
        status=200,
        mimetype='application/json'
    )


@order_blueprint.route('/orders/<int:id>', methods=['DELETE'])
def delete(id):
    Order.query.filter_by(id=id).delete()
    db.session.commit()
    return Response(
        json.dumps({'message': 'Successfully deleted the order'}),
        status=200,
        mimetype='application/json'
    )
