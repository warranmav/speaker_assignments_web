from flask import Blueprint, render_template
from app.models import TalkAssignment
from datetime import datetime

bp = Blueprint('view', __name__, url_prefix='/view')

@bp.route('/assignments', methods=['GET'])
def view_assignments():
    # Query TalkAssignment instead of Record
    assignments_query = TalkAssignment.query.filter(TalkAssignment.date != None).order_by(TalkAssignment.date).all()

    assignments = {}
    for assignment in assignments_query:
        date = assignment.date
        year_month = date.strftime('%Y %B')  # Format: '2024 August'
        if year_month not in assignments:
            assignments[year_month] = []
        assignments[year_month].append(assignment)

    return render_template('view_assignments.html', assignments=assignments)
