from flask import Blueprint, render_template, request, redirect, url_for, flash
import csv
from io import TextIOWrapper
from datetime import datetime
from app.models import db, Record

bp = Blueprint('import_names', __name__, url_prefix='/import')

@bp.route('/names', methods=['GET', 'POST'])
def import_names():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('import_names.import_names'))

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('import_names.import_names'))

        if file and file.filename.endswith('.csv'):
            csv_file = TextIOWrapper(file, encoding='utf-8')
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                if len(row) < 1:
                    continue

                name = row[0].strip()
                date_last_spoken = row[1].strip() if len(row) > 1 else None

                existing_record = Record.query.filter(db.func.lower(Record.name) == name.lower()).first()
                if existing_record:
                    flash(f"Name '{name}' already exists in the database.", 'error')
                    continue

                if date_last_spoken:
                    try:
                        # Parse the date string into a date object
                        date_last_spoken = datetime.strptime(date_last_spoken, '%Y-%m-%d').date()
                    except ValueError:
                        flash(f"Invalid date format for '{name}'. Use YYYY-MM-DD.", 'error')
                        continue
                else:
                    date_last_spoken = None

                new_record = Record(name=name, date_last_spoken=date_last_spoken, exception='None', included_in_pool=True)
                db.session.add(new_record)

            db.session.commit()
            flash('Names imported successfully', 'success')
            return redirect(url_for('import_names.import_names'))
        else:
            flash('Invalid file format. Please upload a CSV file.', 'error')
            return redirect(url_for('import_names.import_names'))

    return render_template('import_names.html')
