from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_required, current_user

from alexandria.extensions import db
from alexandria.forms import LoginForm, EmailForm, ChangePasswordForm
from alexandria.utils import flash_errors
from alexandria.models.users import User

blueprint = Blueprint("users", __name__, url_prefix='/users',
                      static_folder="../static")


@blueprint.route('/')
@login_required
def user_list():
    if not current_user.is_admin:
        return render_template('401_admin.html')

    user_list = User.query.all()
    return render_template('users/user_list.html', users=user_list)

@blueprint.route('/<id>', methods=['GET'])
@login_required
def user_profile(id):
    user = User.query.filter_by(id=id).first()
    user_emails = [user_email.email for user_email in user.emails]
    return render_template('users/user_profile.html', user=user, emails=user_emails)

@blueprint.route('/add_email', methods=['GET', 'POST'])
@login_required
def add_email():
    email_form = EmailForm()
    user = current_user
    if request.method == 'POST':
        if email_form.validate_on_submit():
            print(request.form)
            user.add_email(request.form['email'])
            db.session.commit()
        else:
            flash_errors(email_form)

    user_emails = [user_email.email for user_email in user.emails]
    return render_template('users/add_email.html', user=user, emails=user_emails, email_form=email_form)

@blueprint.route('/reset', methods=["GET", "POST"])
@login_required
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        # emailuser = User.query.filter_by(email=form.email.data).first_or_404()

        # subject = "Password reset requested"
        # from docufind.settings import Config

        # ts = URLSafeTimedSerializer(Config.SECRET_KEY)
        # token = ts.dumps(emailuser.email, salt='recover-key')

        # recover_url = url_for('user.reset_with_token', token=token, _external=True)
        # html = render_template('email/recover.html', recover_url=recover_url)

        # msg = Message(html=html, recipients=[emailuser.email], subject=subject)
        # mail.send(msg)
        flash("Recovery email sent.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)

    return render_template('users/reset.html', resetform=form)

@blueprint.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password():
    user = current_user
    form = ChangePasswordForm()
    form.add_user(user)
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.user_profile', id=user.id))
    else:
        flash_errors(form)
    return render_template('users/change_password.html',
                            form=form)


