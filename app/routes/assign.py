from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Record, TalkAssignment, Theme, Topic
from datetime import datetime

bp = Blueprint('assign', __name__, url_prefix='/assign')

@bp.route('/talk', methods=['GET', 'POST'])
def assign_talk():
    if request.method == 'POST':
        record_id = request.form['record_id']
        date_str = request.form['date']
        speaker_pos = request.form['speaker_pos']
        talk_length = request.form['talk_length']

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD.', 'error')
            return redirect(url_for('assign.assign_talk'))

        # Find the speaker and check if they exist
        speaker = Record.query.get(record_id)
        if speaker:
            # Create a new TalkAssignment entry
            new_assignment = TalkAssignment(
                speaker_id=speaker.id,
                date=date,
                speaker_pos=speaker_pos,
                talk_length=talk_length
            )
            db.session.add(new_assignment)
            db.session.commit()
            flash('Talk assigned successfully.', 'success')
        else:
            flash('Name not found in the database.', 'error')
        return redirect(url_for('assign.assign_talk'))

    # Fetch names from the database, sorted alphabetically
    names = Record.query.filter(Record.included_in_pool == True).order_by(Record.name).all()

    return render_template('assign_talk.html', names=names)
