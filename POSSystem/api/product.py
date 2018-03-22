from flask import Blueprint, request, Response, json
from datetime import datetime
from models import db, Product

product_blueprint = Blueprint('product_blueprint', __name__)


@product_blueprint.route('/products/', methods=['POST'])
def create():
    data = request.get_json()
    product = Product(
        category_id=data['category_id'],
        name=data['name'],
        mfd=datetime.strptime(data['mfd'], "%m/%y"),
        exd=datetime.strptime(data['exd'], "%m/%y"),
        cost=data['cost']
    )
    db.session.add(product)
    db.session.commit()

    return Response(
        json.dumps({'message': 'Successfully created a new product'}),
        status=201,
        mimetype='application/json'
    )


@product_blueprint.route('/products/', methods=['GET'])
@product_blueprint.route('/products/<int:id>', methods=['GET'])
def read(id=None):
    if id:
        product = Product.query.filter_by(id=id).first()
        return Response(
            json.dumps(product.serialize()),
            status=200,
            mimetype='application/json'
        )
    else:
        products = Product.query.all()
        return Response(
            json.dumps([p.serialize() for p in products]),
            status=200,
            mimetype='application/json'
        )


@product_blueprint.route('/products/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    Product.query.filter_by(id=id).update(data)
    db.session.commit()
    return Response(
        json.dumps({'message': 'Successfully updated the product'}),
        status=200,
        mimetype='application/json'
    )


@product_blueprint.route('/products/<int:id>', methods=['DELETE'])
def delete(id):
    Product.query.filter_by(id=id).delete()
    db.session.commit()
    return Response(
        json.dumps({'message': 'Successfully deleted the product'}),
        status=200,
        mimetype='application/json'
    )
