import os
import uuid
import shutil
from datetime import datetime
from contextlib import contextmanager

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

# MAKE DATABASE DIRECTORY
base = os.path.abspath(os.path.dirname(__name__))
database = os.path.join(base, "database")
# shutil.rmtree(database, ignore_errors=True)
os.makedirs(database, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{database}/test.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class Order(Base):

    __tablename__ = "orders"

    id = Column(String, name="uuid", primary_key=True, default=generate_uuid)
    created = Column(String, default=datetime.utcnow())
    status = Column(String, default="created")

    product = Column(String, unique=False)
    size = Column(String)
    quantity = Column(Integer, default=1)

    def __init__(self, product, size, quantity):
        self.product = product
        self.size = size
        self.quantity = quantity

    def json(self):
        return {
            "order": [{
                "product": self.product,
                "size": self.size,
                "quantity": self.quantity}],
            "id": self.id,
            "created": self.created,
            "status": self.status

        }


class OrderDAL(object):
    """Data Access Layer for Order"""

    def __init__(self, db_session):
        self.db_session = db_session

    def create_order(self, product, size, quantity):
        new_order = Order(product=product, size=size, quantity=quantity)
        self.db_session.add(new_order)
        self.db_session.commit()
        self.db_session.refresh(new_order)
        return new_order

    def get_order(self, order_id):
        return self.db_session.query(Order).filter(Order.id == order_id).first()

    def get_orders(self, skip: int = 0, limit: int = 100):
        orders = self.db_session.query(Order).offset(skip).limit(limit).all()
        return [order.json() for order in orders]

    def update_order(self, order_id, product, size, quantity):
        order = self.get_order(order_id)
        if order:
            order.product = product
            order.size = size.value
            order.quantity = quantity
            self.db_session.commit()
            self.db_session.refresh(order)
            return order.json()
        return {}

    def delete_order(self, order_id):
        order = self.get_order(order_id)
        if order:
            self.db_session.delete(order)
            self.db_session.commit()
            return True
        return {}

    def cancel_order(self, order_id):
        order = self.get_order(order_id)
        if order:
            order.status = 'cancelled'
            self.db_session.commit()
            self.db_session.refresh(order)
            return order.json()
        return {}

    def pay_order(self, order_id):
        order = self.get_order(order_id)
        if order:
            order.status = 'progress'
            self.db_session.commit()
            self.db_session.refresh(order)
            return order.json()
        return {}


@contextmanager
def order_dal():
    with SessionLocal() as session:
        yield OrderDAL(session)
