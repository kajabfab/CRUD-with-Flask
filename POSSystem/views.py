from flask import Blueprint, render_template

store_blueprint = Blueprint('store_blueprint', __name__)


@store_blueprint.route('/view/<page>/', methods=['GET'])
def view_page(page):
    return render_template('{}.html'.format(page))
