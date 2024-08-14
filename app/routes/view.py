from flask import Blueprint, render_template
from app.models import Record
from datetime import datetime

bp = Blueprint('view', __name__, url_prefix='/view')

@bp.route('/assignments', methods=['GET'])
def view_assignments():
    records = Record.query.filter(Record.date_last_spoken != None).order_by(Record.date_last_spoken).all()

    assignments = {}
    for record in records:
        date = record.date_last_spoken
        year_month = date.strftime('%Y %B')  # Format: '2024 August'
        if year_month not in assignments:
            assignments[year_month] = []
        assignments[year_month].append(record)

    return render_template('view_assignments.html', assignments=assignments)
