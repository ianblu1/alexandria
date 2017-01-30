from sqlalchemy import select, func, and_
from collections import namedtuple

from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_required, current_user

from alexandria.extensions import db
#from alexandria.forms import LoginForm, EmailForm, ChangePasswordForm
from alexandria.forms import NewDocumentForm, SearchForm, EditDocumentForm
from alexandria.utils import flash_errors, parse_search_params
#from alexandria.models.users import User
from alexandria.models.documentlinks import DocumentLink, Tag
from alexandria.parsers import DocumentParser, parse_tags

blueprint = Blueprint("documents", __name__, url_prefix='/documents',
                      static_folder="../static")

@blueprint.route('/')
@login_required
def document_list():
    document_list = current_user.documents
    return render_template('documents/document_list.html', documents=document_list)

@blueprint.route('/new_document', methods=['GET', 'POST'])
@login_required
def new_document():
    form = NewDocumentForm()
    form.add_user(current_user)
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

@blueprint.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit_document(id):
    #return "Hello {}!".format(name)
    queried_document = DocumentLink.query.filter_by(id=id).first()
    #print([tag.tag for tag in queried_link.tags])
    linktype = namedtuple('linktype', ['url', 'title', 'description', 'tags'])
    l = linktype(
        url = queried_document.url,
        title = queried_document.title,
        description = queried_document.description,
        tags = ','.join([tag.tag for tag in queried_document.tags])
        #slug = queried_link.slug,
        #document_vector = queried_link.document_vector
        )
    form = EditDocumentForm(obj=l)
    #if request.method == 'POST':
    if form.validate_on_submit():
        print(request.form)
        new_url = request.form['url']
        new_title = request.form['title']
        new_description = request.form['description']
        new_tags = request.form['tags']
        doc = DocumentParser(new_url, new_title, new_tags, new_description)
        doc.build_profile()

        queried_document.title = doc.title
        queried_document.url = doc.url
        queried_document.description = doc.description
        queried_document.slug = doc.document_string
        document_tags = [tag.tag for tag in queried_document.tags]
        for tag in doc.tags:
            if tag not in document_tags:
                stored_tag = Tag.query.filter_by(tag=tag).first()
                if stored_tag is None:
                    new_tag = Tag(tag)
                    db.session.add(new_tag)
                    queried_document.tags.append(new_tag)
                else:
                    queried_document.tags.append(stored_tag)

        queried_document.document_vector = func.to_tsvector(doc.document_string)
        db.session.add(queried_document)
        db.session.commit()

        
        #new_document_text = request.form['document_text']
        #new_document_string = request.form['document_string']
        #t = edit_documentlink(queried_link, new_url, new_title, new_description, new_tags, new_document_text)
        #print(new_url, new_title)
        #print(new_tags)
        #print(url_for('document_link', id = id))
        return redirect(url_for('documents.search'))
    else:
        flash_errors(form)
        
    return render_template('documents/edit_document.html', 
        title = 'Edit Document Info',
        form=form,
        document_id=id
        #document_info=l
        )

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
                        DocumentLink.id,
                        DocumentLink.title,
                        DocumentLink.url,
                        (
                            db.func.ts_rank(
                                DocumentLink.document_vector, 
                                db.func.to_tsquery(search_params)
                            )
                        ).label("search_rank")
                    ).filter(
                        and_(
                        DocumentLink.document_vector.match(search_params),
                        DocumentLink.creating_user == current_user.user_name
                        )
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


