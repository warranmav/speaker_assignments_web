from flask import Blueprint, render_template
from datetime import datetime
from app.models import TalkAssignment, Record

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    today = datetime.today()
    current_year_month = today.strftime('%Y-%m')  # Format: '2024-08'

    # Fetch assignments for the current month
    assignments = TalkAssignment.query.filter(
        TalkAssignment.date.startswith(current_year_month)
    ).order_by(TalkAssignment.date).all()

    return render_template('index.html', assignments=assignments)
