from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_required, current_user

from alexandria.extensions import db
#from alexandria.forms import LoginForm, EmailForm, ChangePasswordForm
from alexandria.forms import NewDocumentForm
from alexandria.utils import flash_errors
#from alexandria.models.users import User
from alexandria.models.documentlinks import DocumentLink, Tag

blueprint = Blueprint("documents", __name__, url_prefix='/documents',
                      static_folder="../static")

@blueprint.route('/')
@login_required
def document_list():
    document_list = DocumentLink.query.all()
    return render_template('documents/document_list.html', documents=document_list)

@blueprint.route('/new_document', methods=['GET', 'POST'])
@login_required
def new_document():
    form = NewDocumentForm()
    if form.validate_on_submit():
        print(form.url.data)
        url = form.url.data
        title = form.title.data
        tags = form.tags.data
        description = form.description.data
        
        flash('Document Added', 'success')
        return redirect(url_for('documents.new_document'))
    else:
        flash_errors(form)

    return render_template('documents/new_document.html', form=form)