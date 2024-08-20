from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Record

bp = Blueprint('name_management', __name__, url_prefix='/name_management')


@bp.route('/menu', methods=['GET'])
def name_management_menu():
    return render_template('name_management_menu.html')


@bp.route('/add', methods=['GET', 'POST'])
def add_name():
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            flash('Name is required!', 'error')
            return redirect(url_for('name_management.add_name'))

        existing_record = Record.query.filter(db.func.lower(Record.name) == name.lower()).first()
        if existing_record:
            flash(f"Name '{name}' already exists in the database.", 'error')
        else:
            new_record = Record(name=name)
            db.session.add(new_record)
            db.session.commit()
            flash(f"Name '{name}' added to database.", 'success')

        return redirect(url_for('name_management.add_name'))

    return render_template('add_name.html')

@bp.route('/delete', methods=['GET', 'POST'])
def delete_name():
    if request.method == 'POST':
        record_id = request.form['record_id']
        record = db.session.get(Record, record_id)  # Updated to use Session.get()
        if record:
            db.session.delete(record)
            db.session.commit()
            flash(f"Name '{record.name}' deleted from the database.", 'success')
        else:
            flash('Record not found.', 'error')

        return redirect(url_for('name_management.delete_name'))

    records = Record.query.all()
    return render_template('delete_name.html', records=records)


@bp.route('/view', methods=['GET'])
def view_database():
    records = Record.query.all()
    return render_template('view_database.html', records=records)


@bp.route('/exceptions', methods=['GET'])
def manage_exceptions():
    return render_template('manage_exceptions.html')
