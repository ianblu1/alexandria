# manage.py

from flask_script import Manager, prompt_bool
from flask_migrate import MigrateCommand

from alexandria.app import create_app
from alexandria.extensions import db, bcrypt
from alexandria.models.users import User, UserEmail

app = create_app()

manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def hello():
    print("hello")

@manager.command
def create_dev_user():
    email = 'test@test.com'
    first_name = 'Testy'
    last_name = 'McTesterson'
    user_name = 'tmct'
    password = 'testing_123'
    new_user = User(email, user_name, first_name, last_name, password)
    db.session.add(new_user)
    db.session.commit()
    return

@manager.command
def delete_users():
    for user_email in UserEmail.query.all():
        db.session.delete(user_email)
    
    for user in User.query.all():
        db.session.delete(user)

    db.session.commit()
    return

@manager.command
def drop_db():
    "Drop database tables"
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()
        db.engine.execute('drop table alembic_version;')


if __name__ == "__main__":
    manager.run()
    