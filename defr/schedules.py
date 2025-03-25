from flask import(
    Blueprint, flash, redirect, render_template, request, url_for
)
from .tables import db, Contract, Schedule  # Import the db and models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract, and_
import calendar
from .auth import login_required
import logging

logging.basicConfig(level=logging.DEBUG)

bp = Blueprint('schedules', __name__)

def generate_schedule(contract_id, start):
    contract = Contract.query.get_or_404(contract_id)
    if start == 'initial':
        start_date = contract.original_start
    else:
        start_date = contract.current_start
    date = start_date
    control = 0
    count = 0
    while date < contract.current_end:
        increase = contract.annual_amount
        logging.debug(f"increase is {increase}")
        logging.debug(f"term is {contract.term}")
        income = float(increase) / float(contract.term)
        decrease = float(income) / -1
        balance = float(increase) - float(income)
        for x in range(0,contract.term):
            if control > 100:
                break
            if x == 0:
                increase = contract.annual_amount
            else:
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
            control+=1
            count+=1
    flash("Schedule generated successfully")
    return
    

@bp.route('/<int:contract_id>/recognition_schedule', methods=('GET','POST'))
@login_required
def recognition_schedule(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    recognition_events = Schedule.query.filter_by(contract_id=contract_id).all()
    #if there are no events associated with contract id... we should generate
    if not recognition_events:
        generate_schedule(contract_id, 'initial')
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

@bp.route('/<int:contract_id>/update_schedule', methods=('POST',))
def update_schedule(contract_id):
    contract = Contract.query.get_or_404(contract_id)
    recognition_events = Schedule.query.filter_by(contract_id=contract_id).all()
    #we want to check if the current start date has an associated recognition_event before making more
    current_start = contract.current_start
    event = Schedule.query.filter(Schedule.date == current_start, Schedule.contract_id==contract_id).first()
    if event:
        #current start is in our schedule table so we just display it again
        flash('Schedule is already up to date.')
        return render_template('schedules/display.html', contract = contract, recognition_events=recognition_events)
    else:
        #current start is not in our schedule table so we generate based on the current contract data and display it.
        generate_schedule(contract_id, 'renewal')
        recognition_events = Schedule.query.filter_by(contract_id=contract_id).all()
    return render_template('schedules/display.html', contract = contract, recognition_events=recognition_events)

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

@bp.route('/sort_range', methods=['GET'])
@login_required
def sort_by_range():
    start = request.args.get('start-date')
    end = request.args.get('end-date')
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    #get all events within the range of start to end.
    recognition_events = []
    while start_date <= end_date:
        recognition_events += Schedule.query.filter(
        and_(
            extract('month', Schedule.date) == start_date.month,
            extract('year', Schedule.date) == start_date.year,)

        ).all()
        start_date += relativedelta(months=1)
    return render_template('schedules/sorted_report.html', recognition_events=recognition_events, start=start, end=end)    

    


    

    




