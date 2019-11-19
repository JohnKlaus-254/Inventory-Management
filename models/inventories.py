from app import db

class InventoryModel(db.Model):
    __tablename__='inventories'
    id = db.Column(db.Integer, primary_key=True) #search for argument to start id from say 1000
    inv_name = db.Column(db.String(200), nullable=False)
    inv_type = db.Column(db.String(20),nullable=False)
    buying_price = db.Column(db.Float,nullable=False)
    selling_price = db.Column(db.Float,nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    re_order_period = db.Column(db.Integer, nullable=False)
    sales = db.relationship('SalesModel', backref='inventory', lazy = True)

    @classmethod
    def update_stock(cls, id, qty):
        record = InventoryModel.query.filter_by(id=id).first()

        if record:
            if qty > record.stock:
                return False
            else:
                record.stock = record.stock - qty
                db.session.commit()
                return True
        else:
            return False

    #edit record
    @classmethod
    def edit_record(cls, id, name, type, bp,sp,stock,rp):
        record = cls.query.filter_by(id=id).first()
        if record:
            record.inv_name = name
            record.type = type
            record.buying_price = bp
            record.selling_price = sp
            record.stock = stock
            record.re_order_period = rp
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def getCountType(cls, name):
        record = cls.query.filter_by(inv_type=name).count()
        return record


