from flask import(
    Blueprint, flash, redirect, render_template, request, url_for
)
from .tables import db, Contract, Schedule  # Import the db and models
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract, and_
import calendar
from .auth import login_required

bp = Blueprint('schedules', __name__)

def generate_schedule(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    date = contract.current_start
    increase = contract.annual_amount
    income = float(increase) / float(contract.term)
    decrease = float(income) / -1
    balance = float(increase) - float(income)
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
        date = date + relativedelta(months=1)
    flash("Schedule generated successfully")
    return
    

@bp.route('/<int:contract_id>/recognition_schedule', methods=('GET','POST'))
@login_required
def recognition_schedule(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    recognition_events = Schedule.query.filter_by(contract_id=contract_id).all()
    #if there are no events associated with contract id... we should generate
    if not recognition_events:
        generate_schedule(contract_id)
        recognition_events = Schedule.query.filter_by(contract_id=contract_id).all()
        return render_template('schedules/display.html', contract=contract, recognition_events=recognition_events)

    # if there are we display
    return render_template('schedules/display.html', contract=contract, recognition_events=recognition_events)

@bp.route('/<int:contract_id>/delete_schedule', methods = ('POST',))
@login_required
def delete_schedule(contract_id):
    Schedule.query.filter_by(contract_id=contract_id).delete()
    db.session.commit()
    flash("Successfully deleted schedule")
    return redirect(url_for('contracts.index'))

@bp.route('/<int:month>/<int:year>monthly_report')
@login_required
def monthly_report(month, year):
    recognition_events = Schedule.query.filter(
        and_(
            extract('month', Schedule.date) == month,
            extract('year', Schedule.date) == year,)

        ).all()
        
    error = None

    if month > 12 or month < 1:
        error = "Please enter a valid month"
    if not recognition_events:
        error = "No data for {month}"

    if error is not None:
            flash(error)
    else:
        month_str = calendar.month_name[month]
        return render_template('schedules/monthly_report.html', recognition_events=recognition_events, month_str=month_str, year=year)    

    


    

    




