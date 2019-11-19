from app import db
from sqlalchemy.sql import func
from datetime import datetime




class SalesModel(db.Model):
    __tablename__='sales'
    s_id = db.Column(db.Integer, primary_key=True) #search for argument to start id from say 1000
    s_qty = db.Column(db.Integer, nullable=False)
    inv_id = db.Column(db.Integer,db.ForeignKey('inventories.id'))
    time_created = db.Column(db.DateTime,default=datetime.utcnow())