from sqlalchemy import select, func

from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_required, current_user

from alexandria.extensions import db
#from alexandria.forms import LoginForm, EmailForm, ChangePasswordForm
from alexandria.forms import NewDocumentForm, SearchForm
from alexandria.utils import flash_errors, parse_search_params
#from alexandria.models.users import User
from alexandria.models.documentlinks import DocumentLink, Tag
from alexandria.parsers import DocumentParser

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

        doc = DocumentParser(url, title, tags, description)
        doc.build_profile()

        new_document = DocumentLink(current_user, doc.url, doc.title, doc.description, doc.document_string)

        for tag in doc.tags:
            stored_tag = Tag.query.filter_by(tag=tag).first()
            if stored_tag is None:
                new_tag = Tag(tag)
                db.session.add(new_tag)
                new_document.tags.append(new_tag)
            else:
                new_document.tags.append(stored_tag)

        new_document.document_vector = func.to_tsvector(doc.document_string)
        db.session.add(new_document)
        db.session.commit()
        
        flash('Document Added', 'success')
        return redirect(url_for('documents.new_document'))
    else:
        flash_errors(form)

    return render_template('documents/new_document.html', form=form)

@blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        print(search_form.search.data)
        return redirect(url_for('documents.search_results', search_form_input=request.form['search']))
    else:
        flash_errors(search_form)
    return render_template('documents/search.html', form=search_form)


@blueprint.route('/search-results', methods=['GET', 'POST'])
@blueprint.route('/search-results/<int:page>', methods=['GET', 'POST'])
def search_results(page=1):
    search_form=SearchForm(search=request.args['search_form_input'])
    search_params = parse_search_params(request.args['search_form_input'])
    
    documents = DocumentLink.query.with_entities(
                        DocumentLink.title,
                        DocumentLink.url,
                        (
                            db.func.ts_rank(
                                DocumentLink.document_vector, 
                                db.func.to_tsquery(search_params)
                            )
                        ).label("search_rank")
                    ).filter(
                        DocumentLink.document_vector.match(search_params)
                    ).order_by(
                        db.func.ts_rank(
                            DocumentLink.document_vector, db.func.to_tsquery(search_params)
                                       ).desc()
                    ).paginate(page,current_app.config['POSTS_PER_PAGE'],False)

    if request.method == "POST":
        search_params = parse_search_params(request.form['search'])
        print(search_params)
        return redirect(url_for('documents.search_results', search_form_input=request.form['search']))
    
    return render_template('documents/search_results.html', 
                           title='Search',
                           form=search_form,
                           documents=documents)


