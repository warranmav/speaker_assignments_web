# app/routes/tools.py

from flask import Blueprint, render_template, redirect, url_for
from app import db
from app.models import Record

bp = Blueprint('tools', __name__, url_prefix='/tools')

@bp.route('/tools')
def tools_menu():
    return render_template('tools_menu.html')

@bp.route('/tools/cleanup_db', methods=['GET', 'POST'])
def cleanup_db():
    with app.app_context():
        # Update all records where exception is the string 'None' to None
        records_to_update = Record.query.filter(Record.exception == 'None').all()

        for record in records_to_update:
            record.exception = None

        db.session.commit()
    return redirect(url_for('tools.tools_menu'))
