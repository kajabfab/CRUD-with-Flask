from flask import Blueprint, request, Response, json

from models import db, Category

category_blueprint = Blueprint('category_blueprint', __name__)


@category_blueprint.route('/categories/', methods=['POST'])
def create():
    data = request.get_json()
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()

    return Response(
        json.dumps({'message': 'Successfully created a new category'}),
        status=201,
        mimetype='application/json'
    )


@category_blueprint.route('/categories/', methods=['GET'])
@category_blueprint.route('/categories/<int:id>', methods=['GET'])
def read(id=None):
    if id:
        category = Category.query.filter_by(id=id).first()
        return Response(
            json.dumps(category.serialize()),
            status=200,
            mimetype='application/json'
        )
    else:
        categories = Category.query.all()
        return Response(
            json.dumps([c.serialize() for c in categories]),
            status=200,
            mimetype='application/json'
        )


@category_blueprint.route('/categories/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    Category.query.filter_by(id=id).update(data)
    db.session.commit()
    return Response(
        json.dumps({'message': 'Successfully updated the category'}),
        status=200,
        mimetype='application/json'
    )


@category_blueprint.route('/categories/<int:id>', methods=['DELETE'])
def delete(id):
    Category.query.filter_by(id=id).delete()
    db.session.commit()
    return Response(
        json.dumps({'message': 'Successfully deleted the category'}),
        status=200,
        mimetype='application/json'
    )
