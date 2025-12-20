from database import db

class Year(db.Model):
    __tablename__ = 'year'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)
    year_brands = db.relationship('YearBrand', backref='year', cascade='all, delete-orphan')


class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String, nullable=False)
    is_truck = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    year_brands = db.relationship('YearBrand', backref='brand', cascade='all, delete-orphan')


class YearBrand(db.Model):
    __tablename__ = 'year_brand'
    id = db.Column(db.Integer, primary_key=True)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)

    __table_args__ = (db.UniqueConstraint('year_id', 'brand_id', name='unique_year_make'),)
    models = db.relationship('Model', backref='year_brand', cascade='all, delete-orphan')


class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    year_brand_id = db.Column(db.Integer, db.ForeignKey('year_brand.id'), nullable=False)
    model_name = db.Column(db.String, nullable=False)
    submodels = db.relationship('Submodel', backref='model', cascade='all, delete-orphan')


class Submodel(db.Model):
    __tablename__ = 'submodel'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)
    vehicle_id = db.Column(db.String, nullable=False)
    submodel_name = db.Column(db.String, nullable=False)

    windshields = db.relationship('Windshield', backref='submodel', cascade='all, delete-orphan')
    backglasses = db.relationship('Backglass', backref='submodel', cascade='all, delete-orphan')
    door_windows = db.relationship('DoorWindow', backref='submodel', cascade='all, delete-orphan')
