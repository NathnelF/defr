from flask import(
    Blueprint
)

from .tables import db, Customer, Service, User, Contract, Schedule  # Import the db and models

bp = Blueprint('contracts', __name__)

