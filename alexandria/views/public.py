from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_required, logout_user, current_user, login_user

from alexandria.extensions import db, login_manager, bcrypt
from alexandria.forms import LoginForm, RegisterForm, EmailForm
from alexandria.utils import flash_errors
from alexandria.models.users import User

blueprint = Blueprint("public", __name__,
                      static_folder="../static")

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@blueprint.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm(request.form)

    if current_user.is_authenticated:
        return redirect(url_for('users.user_profile', id=current_user.id))
    
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            form.user.authenticated = True
            db.session.add(form.user)
            db.session.commit()
            login_user(form.user, remember=True)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("users.user_profile", id=form.user.id)
            return redirect(url_for('public.home'))
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form)


@blueprint.route('/about')
def about():
    #form = LoginForm(request.form)
    return render_template('public/about.html' 
                            #form=form
                            )


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(
                        email=form.email.data,
                        user_name=form.username.data,
                        first_name=None,
                        last_name=None, 
                        password=form.password.data
                        )
        new_user.authenticated=True
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash("Thank you for registering. You are now logged in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    user = current_user
    print(user.first_name, user.authenticated)
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))

# @blueprint.route('/reset', methods=["GET", "POST"])
# def reset():
#     form = EmailForm()
#     if form.validate_on_submit():
#         # emailuser = User.query.filter_by(email=form.email.data).first_or_404()

#         # subject = "Password reset requested"
#         # from docufind.settings import Config

#         # ts = URLSafeTimedSerializer(Config.SECRET_KEY)
#         # token = ts.dumps(emailuser.email, salt='recover-key')

#         # recover_url = url_for('user.reset_with_token', token=token, _external=True)
#         # html = render_template('email/recover.html', recover_url=recover_url)

#         # msg = Message(html=html, recipients=[emailuser.email], subject=subject)
#         # mail.send(msg)

#         return redirect(url_for('home'))
#     else:
#         flash_errors(form)

#     return render_template('public/reset.html', resetform=form)

