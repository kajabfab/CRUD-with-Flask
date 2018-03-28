from flask import Blueprint, render_template

store_blueprint = Blueprint('store_blueprint', __name__)


@store_blueprint.route('/view/categories/', methods=['GET'])
def category():
    return render_template('categories.html')
