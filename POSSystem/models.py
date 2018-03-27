from flask_sqlalchemy import SQLAlchemy, event
from sqlalchemy import engine

db = SQLAlchemy()


# noinspection PyUnusedLocal
@event.listens_for(engine.Engine, 'connect')
def __set_sqlite_pragma(db_conn, conn_record):
    cursor = db_conn.cursor()
    cursor.execute('PRAGMA foreign_keys=ON;')
    cursor.close()


class Category(db.Model):
    # Default __tablename__ = category
    __tablename__ = 'category-table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship(
        'Product',
        backref=db.backref('category-table', lazy='joined'),
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return self.serialize().__repr__()


class Customer(db.Model):
    # Default __tablename__ = customer
    __tablename__ = 'customer-table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    orders = db.relationship(
        'Order',
        backref=db.backref('customer-table', lazy='joined'),
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'phone': self.phone
        }

    def __repr__(self):
        return self.serialize().__repr__()


class Product(db.Model):
    # Default __tablename__ = product
    __tablename__ = 'product-table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category-table.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mfd = db.Column(db.DateTime, nullable=False)
    exd = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(*['available', 'sold']), nullable=False, default='available')

    def serialize(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'mfd': self.mfd.strftime("%m/%y"),
            'exd': self.exd.strftime("%m/%y"),
            'cost': self.cost,
            'status': self.status
        }

    def __repr__(self):
        return self.serialize().__repr__()


sold_products = db.Table('sold-products',
                         db.Column('order_id', db.Integer, db.ForeignKey('order-table.id', ondelete='CASCADE')),
                         db.Column('product_id', db.Integer, db.ForeignKey('product-table.id', ondelete='CASCADE'))
                         )


class Order(db.Model):
    # Default __tablename__ = order
    __tablename__ = 'order-table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer-table.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    products = db.relationship(
        'Product',
        secondary=sold_products,
        backref=db.backref('order-table', lazy='joined'),
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True
    )
    total = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'date': self.date.strftime("%d/%m/%y"),
            'products': [p.serialize() for p in self.products],
            'total': self.total
        }

    def __repr__(self):
        return self.serialize().__repr__()
