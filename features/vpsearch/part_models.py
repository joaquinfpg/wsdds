from database import db


class NagsGlass(db.Model):
    __tablename__ = 'nags_glass'
    id = db.Column(db.String, primary_key=True)
    prefix_cd = db.Column(db.String, nullable=False)
    part_num = db.Column(db.String, nullable=False)
    tube_qty = db.Column(db.Numeric)
    adas = db.Column(db.Boolean)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric)
    glass_type = db.Column(db.String, nullable=False)

    configurations = db.relationship('GlassConfiguration', backref='nags_glass', cascade='all, delete-orphan')
    interchanges = db.relationship('GlassInterchange', backref='nags_glass', cascade='all, delete-orphan')
    windshields = db.relationship('Windshield', backref='nags_glass', cascade='all, delete-orphan')
    backglasses = db.relationship('Backglass', backref='nags_glass', cascade='all, delete-orphan')
    door_windows = db.relationship('DoorWindow', backref='nags_glass', cascade='all, delete-orphan')


class Windshield(db.Model):
    __tablename__ = 'windshield'
    bodystyle_id = db.Column(db.Integer, db.ForeignKey('submodel.id'), primary_key=True)
    nags_glass_id = db.Column(db.String, db.ForeignKey('nags_glass.id'), primary_key=True)
    part_side = db.Column(db.String)


class Backglass(db.Model):
    __tablename__ = 'backglass'
    bodystyle_id = db.Column(db.Integer, db.ForeignKey('submodel.id'), primary_key=True)
    nags_glass_id = db.Column(db.String, db.ForeignKey('nags_glass.id'), primary_key=True)
    part_side = db.Column(db.String)


class DoorWindow(db.Model):
    __tablename__ = 'door_window'
    bodystyle_id = db.Column(db.Integer, db.ForeignKey('submodel.id'), primary_key=True)
    nags_glass_id = db.Column(db.String, db.ForeignKey('nags_glass.id'), primary_key=True)
    part_posi = db.Column(db.String)
    part_side = db.Column(db.String)


class GlassConfiguration(db.Model):
    __tablename__ = 'glass_configuration'
    config_id = db.Column(db.Integer, primary_key=True)
    nags_glass_id = db.Column(db.String, db.ForeignKey('nags_glass.id'), nullable=False)
    nags_part_number = db.Column(db.String)
    atchmnt_dsc = db.Column(db.String)
    nags_labor = db.Column(db.Numeric)
    prc = db.Column(db.Numeric)


class GlassInterchange(db.Model):
    __tablename__ = 'glass_interchange'
    interchange_id = db.Column(db.Integer, primary_key=True)
    nags_glass_id = db.Column(db.String, db.ForeignKey('nags_glass.id'), nullable=False)
    rplmt_glass_id = db.Column(db.String)
