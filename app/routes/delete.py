# app/routes/delete.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Record

bp = Blueprint('delete', __name__, url_prefix='/delete')


@bp.route('/entry', methods=['GET', 'POST'])
def delete_entry():
    if request.method == 'POST':
        record_id = request.form['record_id']
        record = db.session.get(Record, record_id)  # Updated line
        if record:
            db.session.delete(record)
            db.session.commit()
            flash(f"Name '{record.name}' deleted from the database.", 'success')
        else:
            flash('Record not found.', 'error')

        return redirect(url_for('delete.delete_entry'))

    records = Record.query.all()
    return render_template('delete_entry.html', records=records)
