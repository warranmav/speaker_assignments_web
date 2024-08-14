# cleanup_script.py

from app import app, db
from app.models import Record

with app.app_context():
    # Update all records where exception is the string 'None' to None
    records_to_update = Record.query.filter(Record.exception == 'None').all()

    for record in records_to_update:
        record.exception = None

    db.session.commit()

    # Verification step
    inconsistent_records = Record.query.filter(Record.exception == 'None').all()
    if not inconsistent_records:
        print("Database cleanup completed successfully.")
    else:
        print("There are still records with inconsistent exception values.")
