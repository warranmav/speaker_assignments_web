# app/routes/add.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Record

bp = Blueprint('add', __name__, url_prefix='/add')


@bp.route('/name', methods=['GET', 'POST'])
def add_name():
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            flash('Name is required!', 'error')
            return redirect(url_for('add.add_name'))

        # Check if the name already exists (case-insensitive)
        existing_record = Record.query.filter(db.func.lower(Record.name) == name.lower()).first()

        if existing_record:
            flash(f"Name '{name}' already exists in the database.", 'error')
        else:
            new_record = Record(name=name, exception='None', included_in_pool=True)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Name '{name}' added to database.", 'success')

        return redirect(url_for('add.add_name'))

    return render_template('add_name.html')
