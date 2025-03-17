from flask import Blueprint, jsonify
from .tables import db, Customer, Service, User, Contract, Schedule  # Import the db and models

bp = Blueprint('test', __name__)

@bp.route('/customers')
def list_customers():
    customers = Customer.query.all()
    return jsonify([customer.customer_name for customer in customers])

@bp.route('/services')
def list_services():
    services = Service.query.all()
    return jsonify([service.service_name for service in services])

@bp.route('/users')
def list_users():
    users = User.query.all()
    return jsonify([user.email for user in users])

@bp.route('/contracts')
def list_contracts():
    contracts = Contract.query.all()
    return jsonify([contracts.contract_id for contracts in contracts])

@bp.route('/events')
def list_schedules():
    events = Schedule.query.all()
    return jsonify([events.event_id for event in events])
