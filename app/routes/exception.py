from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Record

bp = Blueprint('exception', __name__, url_prefix='/exception')

EXCEPTIONS = ["Inactive", "Health", "Refusal", "Available"]


@bp.route('/add', methods=['GET', 'POST'])
def add_exception():
    if request.method == 'POST':
        record_id = request.form['record_id']
        exception = request.form['exception']

        if exception not in EXCEPTIONS:
            flash('Invalid exception selected.', 'error')
            return redirect(url_for('exception.add_exception'))

        record = Record.query.get(record_id)
        if record:
            record.exception = exception
            if exception != "Available":
                record.date_last_spoken = None
            record.included_in_pool = exception == "Available"
            db.session.commit()
            flash(f"Exception '{exception}' added to {record.name}.", 'success')
        else:
            flash('Record not found.', 'error')

        return redirect(url_for('exception.add_exception'))

    records = Record.query.all()
    return render_template('add_exception.html', records=records, exceptions=EXCEPTIONS)


@bp.route('/update', methods=['GET', 'POST'])
def update_exception():
    if request.method == 'POST':
        record_id = request.form['record_id']
        exception = request.form['exception']

        if exception not in EXCEPTIONS:
            flash('Invalid exception selected.', 'error')
            return redirect(url_for('exception.update_exception'))

        record = Record.query.get(record_id)
        if record:
            record.exception = exception
            if exception != "Available":
                record.date_last_spoken = None
            record.included_in_pool = exception == "Available"
            db.session.commit()
            flash(f"Exception '{exception}' updated for {record.name}.", 'success')
        else:
            flash('Record not found.', 'error')

        return redirect(url_for('exception.update_exception'))

    records = Record.query.all()
    return render_template('update_exception.html', records=records, exceptions=EXCEPTIONS)


@bp.route('/remove', methods=['GET', 'POST'])
def remove_exception():
    if request.method == 'POST':
        record_id = request.form['record_id']

        record = Record.query.get(record_id)
        if record:
            record.exception = None
            record.included_in_pool = True
            db.session.commit()
            flash(f"Exception removed for {record.name}.", 'success')
        else:
            flash('Record not found.', 'error')

        return redirect(url_for('exception.remove_exception'))

    records = Record.query.all()
    return render_template('remove_exception.html', records=records)


@bp.route('/available', methods=['GET', 'POST'])
def set_available():
    if request.method == 'POST':
        record_id = request.form['record_id']

        record = Record.query.get(record_id)
        if record:
            record.exception = "Available"
            record.included_in_pool = True
            db.session.commit()
            flash(f"{record.name} is now set as 'Available'.", 'success')
        else:
            flash('Record not found.', 'error')

        return redirect(url_for('exception.set_available'))

    records = Record.query.all()
    return render_template('set_available.html', records=records)
