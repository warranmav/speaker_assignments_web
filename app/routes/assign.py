from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Record, TalkAssignment, Theme, Topic
from datetime import datetime, timedelta
from sqlalchemy.orm import aliased
from sqlalchemy import and_, or_, func

bp = Blueprint('assign', __name__, url_prefix='/assign')

# Manage Assignments Menu
@bp.route('/manage_assignments_menu', methods=['GET'])
def manage_assignments_menu():
    return render_template('manage_assignments_menu.html')

# Route to assign a talk
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

    # Calculate the cutoff date (150 days ago)
    cutoff_date = datetime.today() - timedelta(days=150)

    # Aliased instance for filtering based on the last talk date
    LastTalk = aliased(TalkAssignment)

    # Subquery to get the last talk date for each speaker
    last_talk_subquery = db.session.query(
        LastTalk.speaker_id,
        func.max(LastTalk.date).label('last_talk_date')
    ).group_by(LastTalk.speaker_id).subquery()

    # Query to filter speakers based on the last talk date and exception status
    eligible_names = db.session.query(Record).outerjoin(
        last_talk_subquery, Record.id == last_talk_subquery.c.speaker_id
    ).filter(
        or_(
            last_talk_subquery.c.last_talk_date == None,
            last_talk_subquery.c.last_talk_date < cutoff_date
        ),
        or_(
            Record.exception == None,
            Record.exception == 'Available'
        )
    ).order_by(Record.name).all()

    return render_template('assign_talk.html', names=eligible_names)


# Route to manage assignments (view all assignments)
@bp.route('/manage', methods=['GET'])
def manage_assignments():
    assignments = TalkAssignment.query.all()
    return render_template('manage_assignments.html', assignments=assignments)

# Route to update an assignment
@bp.route('/update/<int:assignment_id>', methods=['GET', 'POST'])
def update_assignment(assignment_id):
    assignment = TalkAssignment.query.get_or_404(assignment_id)
    if request.method == 'POST':
        assignment.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        assignment.speaker_pos = request.form['speaker_pos']
        assignment.talk_length = request.form['talk_length']
        db.session.commit()
        flash('Assignment updated successfully.', 'success')
        return redirect(url_for('assign.manage_assignments'))

    records = Record.query.all()
    return render_template('update_assignment.html', assignment=assignment, records=records)

# Route to delete an assignment
@bp.route('/delete/<int:assignment_id>', methods=['POST'])
def delete_assignment(assignment_id):
    assignment = TalkAssignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    flash('Assignment deleted successfully.', 'success')
    return redirect(url_for('assign.manage_assignments'))
