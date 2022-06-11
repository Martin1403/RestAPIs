import uuid

import shortuuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


from graphqlflaskapp.app import app

db = SQLAlchemy(app)


def generate_uuid():
    return str(shortuuid.encode(uuid.uuid4()))


class Job(db.Model):
    __tablename__ = "jobs"

    id = Column(String, name="id", primary_key=True, default=generate_uuid)
    companyId = Column(String, ForeignKey("companies.id"))
    title = Column(String(64), unique=False, nullable=False)
    description = Column(String(128))
    company = relationship("Company", uselist=True)

    def __init__(self, title, description, companyId=None):
        self.companyId = companyId
        self.title = title
        self.description = description

    def __repr__(self):
        return f'<Job {self.title!r}>'

    @property
    def add_company(self):
        return self.companyId

    @add_company.setter
    def add_company(self, company):
        self.company = [company]

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "companyId": self.companyId,
        }


class Company(db.Model):
    __tablename__ = "companies"

    id = Column(String, name="id", primary_key=True, default=generate_uuid)
    name = Column(String(64), unique=True, nullable=False)
    description = Column(String(128))

    def __init__(self, name, description, id=None):
        self.id = id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Company {self.name!r}>"

    @property
    def get_id(self):
        return self.id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
