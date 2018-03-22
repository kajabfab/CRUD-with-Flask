from flask import Flask

from config import dev_config
from models import db
from api.category import category_blueprint
from api.product import product_blueprint
from api.customer import customer_blueprint
from api.order import order_blueprint

app = Flask(__name__)
app.config.from_object(dev_config)

app.register_blueprint(category_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(customer_blueprint)
app.register_blueprint(order_blueprint)

if __name__ == '__main__':
    db.init_app(app=app)
    db.create_all(app=app)

    app.run()
