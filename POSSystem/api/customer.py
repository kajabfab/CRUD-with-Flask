from flask import Blueprint, request, Response, json
from models import db, Customer

customer_blueprint = Blueprint('customer_blueprint', __name__)


@customer_blueprint.route('/customers/', methods=['POST'])
def create():
    data = request.get_json()
    customer = Customer(
        name=data['name'],
        age=data['age'],
        phone=data['age']
    )
    db.session.add(customer)
    db.session.commit()

    return Response(
        json.dumps({'message': 'Successfully created a new customer'}),
        status=201,
        mimetype='application/json'
    )


@customer_blueprint.route('/customers/', methods=['GET'])
@customer_blueprint.route('/customers/<int:id>', methods=['GET'])
def read(id=None):
    if id:
        customer = Customer.query.filter_by(id=id).first()
        return Response(
            json.dumps(customer.serialize()),
            status=200,
            mimetype='application/json'
        )
    else:
        customers = Customer.query.all()
        return Response(
            json.dumps([c.serialize() for c in customers]),
            status=200,
            mimetype='application/json'
        )


@customer_blueprint.route('/customers/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    Customer.query.filter_by(id=id).update(data)
    db.session.commit()
    return Response(
        json.dumps({'message': 'Successfully updated the customer'}),
        status=200,
        mimetype='application/json'
    )


@customer_blueprint.route('/customers/<int:id>', methods=['DELETE'])
def delete(id):
    Customer.query.filter_by(id=id).delete()
    db.session.commit()
    return Response(
        json.dumps({'message': 'Successfully deleted the customer'}),
        status=200,
        mimetype='application/json'
    )
