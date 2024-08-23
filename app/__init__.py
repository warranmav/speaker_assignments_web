from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes import main, add, assign, delete, exception, view, name_management, import_names, tools
    app.register_blueprint(main.bp)
    app.register_blueprint(add.bp)
    app.register_blueprint(assign.bp)
    app.register_blueprint(delete.bp)
    app.register_blueprint(exception.bp)
    app.register_blueprint(view.bp)
    app.register_blueprint(name_management.bp)
    app.register_blueprint(import_names.bp)
    app.register_blueprint(tools.bp)

    # Ensure the database and tables are created
    with app.app_context():
        db.create_all()

    return app
