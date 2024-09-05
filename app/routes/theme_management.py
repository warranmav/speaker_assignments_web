from flask import Blueprint, render_template

bp = Blueprint('theme_management', __name__, url_prefix='/theme_management')

@bp.route('/')
def index():
    return render_template('theme_management/index.html')

@bp.route('/add', methods=['GET', 'POST'])
def add_theme():
    # Logic for adding a theme will go here
    return render_template('theme_management/add_theme.html')

@bp.route('/update', methods=['GET', 'POST'])
def update_theme():
    # Logic for updating a theme will go here
    return render_template('theme_management/update_theme.html')

@bp.route('/delete', methods=['GET', 'POST'])
def delete_theme():
    # Logic for deleting a theme will go here
    return render_template('theme_management/delete_theme.html')
