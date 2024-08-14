from flask import Blueprint, render_template
from datetime import datetime
from app.models import Record

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    today = datetime.today()
    current_year_month = today.strftime('%Y-%m')  # Format: '2024-08'

    records = Record.query.filter(
        Record.date_last_spoken != None,
        Record.date_last_spoken.startswith(current_year_month)
    ).order_by(Record.date_last_spoken).all()

    return render_template('index.html', assignments=records)
