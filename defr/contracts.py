from flask import(
    Blueprint, flash, redirect, render_template, request, url_for
)
from .tables import db, Contract, Customer, Service  # Import the db and models
from .auth import login_required
from datetime import datetime

bp = Blueprint('contracts', __name__)

@bp.route('/')
def direct_to_login():
    return redirect(url_for('auth.login'))

@bp.route('/index')
@login_required
def index():
    contracts = Contract.query.all()
    current_month = datetime.now().month
    current_year = datetime.now().year
    return render_template('contracts/index.html', contracts=contracts, current_month=current_month, current_year=current_year)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        service_name = request.form['service_name']
        term = request.form['term']
        annual_amount = request.form['annual_amount']
        original_start = request.form['original_start']
        current_start = request.form['current_start']
        current_end = request.form['current_end']
        auto_renew = 'auto_renew' in request.form  # Checkbox returns 'on' if checked
        price_increase = request.form['price_increase']
        error = None

        if not customer_name:
            error = 'Customer is required'

        elif not service_name:
            error = 'Service is required'

        elif not annual_amount:
            error = 'Annual Amount is required'
        
        elif not term:
            error = 'Term is required'

        #lookup customer id from name
        customer = Customer.query.filter(Customer.customer_name == customer_name).first()
        if customer:
            customer_id = customer.customer_id
        else:
            new_customer = Customer(customer_name=customer_name)
            db.session.add(new_customer)
            db.session.commit()
            customer = Customer.query.filter(Customer.customer_name == customer_name).first()
            customer_id = customer.customer_id
        
        #lookup service id from name
        service = Service.query.filter(Service.service_name == service_name).first()
        if service:
            service_id = service.service_id
        else:
            new_service = Service(service_name=service_name)
            db.session.add(new_service)
            db.session.commit()
            service = Service.query.filter(Service.service_name == service_name).first()
            service_id = service.service_id
        
        if error is not None:
            flash(error)
        else:
            new_contract = Contract(
                customer_id=customer_id,
                service_id=service_id,
                term=term,
                annual_amount=annual_amount,
                original_start=original_start,
                current_start=current_start,
                current_end=current_end,
                auto_renew=auto_renew,
                price_increase=price_increase)
            db.session.add(new_contract)
            db.session.commit()

            flash('Created contract successfully')
            return redirect(url_for('contracts.index'))
    return render_template('contracts/create.html')


@bp.route('/<int:contract_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(contract_id):
    contract = Contract.query.get_or_404(contract_id)

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        service_id = request.form['service_id']
        term = request.form['term']
        annual_amount = request.form['annual_amount']
        original_start = request.form['original_start']
        current_start = request.form['current_start']
        current_end = request.form['current_end']
        auto_renew = 'auto_renew' in request.form 
        price_increase = request.form['price_increase']
        error = None

        if not customer_id:
            error = 'Customer is required'

        elif not service_id:
            error = 'Service is required'

        elif not annual_amount:
            error = 'Annual Amount is required'
        
        elif not term:
            error = 'Term is required'
        
        if error is not None:
            flash(error)
        else:
            contract.customer_id=customer_id
            contract.service_id=service_id
            contract.term=term
            contract.annual_amount=annual_amount
            contract.original_start=original_start
            contract.current_start=current_start
            contract.current_end=current_end
            contract.auto_renew=auto_renew
            contract.price_increase=price_increase
            db.session.commit()

            flash('Created contract successfully')
            return redirect(url_for('contracts.index'))
    return render_template('contracts/edit.html', contract=contract)


@bp.route('/<int:contract_id>/delete', methods=('POST',))
@login_required
def delete(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    db.session.delete(contract)
    db.session.commit()
    flash("Contract deleted successfully")
    return redirect(url_for('contracts.index'))