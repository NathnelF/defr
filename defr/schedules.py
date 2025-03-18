from flask import(
    Blueprint, flash, redirect, render_template, request, url_for
)
from .tables import db, Contract, Schedule  # Import the db and models
from .auth import login_required

bp = Blueprint('schedule', __name__)

def generate_schedule(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    date = contract.current_start
    increase = contract.annual_amount
    income = int(increase) / int(contract.term)
    decrease = int(income) / -1
    balance = int(increase) - int(income)
    for x in range(0,contract.term):
        if date != contract.current_start:
            increase = 0
        new_event = Schedule(
        contract_id=contract_id, 
        customer_id=contract.customer.customer_id, 
        service_id=contract.service.service_id,
        date=date,
        increase = increase,
        decrease = decrease,
        income = income,
        balance = balance
    )
        db.session.add(new_event)
        db.session.commit()
        balance -= income
    flash("Schedule generated successfully")
    return

@bp.route('/<int:contract_id/recognition_schedule', methods=('GET','POST'))
@login_required
def show_schedule(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    recognition_events = Schedule.query.filter_by(contract_id=contract_id).all()
    #if there are no events associated with contract id... we should generate
    if not recognition_events:
        generate_schedule(contract_id)

    # if there are we display
    return render_template('schedules/display.html', contract=contract, recognition_events=recognition_events)

    #code to get schedule associated with contract_id!


