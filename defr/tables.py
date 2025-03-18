from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    customer_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Customer: {self.customer_name}>'

class Service(db.Model):
    __tablename__ = 'service'
    service_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    service_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Service: {self.service_name}>'
    
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<User: {self.email}>'
    
class Contract(db.Model):
    __tablename__= 'contract'
    contract_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    term = db.Column(db.Integer, db.CheckConstraint('term > 0'), nullable=False)
    annual_amount = db.Column(db.Numeric(10,2), db.CheckConstraint('annual_amount > 0'), nullable=False)
    original_start = db.Column(db.Date)
    current_start = db.Column(db.Date)
    current_end = db.Column(db.Date)
    churned = db.Column(db.Date)
    auto_renew = db.Column(db.Boolean)
    price_increase = db.Column(db.Integer)

    customer = db.relationship('Customer', backref='contracts')
    service = db.relationship('Service', backref='contracts')

    def __repr__(self):
        return f'<Contract id: {self.contract_id}, Customer id: {self.customer_id}, Service id: {self.service_id}>'
    

class Schedule(db.Model):
    __tablename__ = 'recognition_schedule'
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.contract_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    date = db.Column(db.Date)
    increase = db.Column(db.Numeric(9,2), db.CheckConstraint('increase > 0'))
    decrease = db.Column(db.Numeric(9,2), db.CheckConstraint('decrease > 0'))
    income = db.Column(db.Numeric(9,2), db.CheckConstraint('income > 0'))
    balance = db.Column(db.Numeric(9,2))

    customer = db.relationship('Customer', backref='schedules')
    service = db.relationship('Service', backref='schedules')
    contracts = db.relationship('Contract', backref='schedules')

    def __repr__(self):
        return f'<Event id: {self.event_id}, Contract id: {self.contract_id}, Customer id: {self.customer_id}, Service id: {self.service_id}>'
    