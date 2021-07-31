from flask import Blueprint, render_template, flash, redirect, url_for, request, g
from flask.globals import current_app
from flask_login import current_user, login_user, logout_user, login_required
from web_app.app.forms import SearchForm, PostTransportistas, PostEmbarcadores, ContactForm, Comments    
from web_app.app.models import FletesTransportistas, CargasEmbarcadores, ContactTable, CommentsFletesTransportistas, CommentsCargasEmbarcadores
from werkzeug.urls import url_parse
from web_app.config2 import Config
from web_app.app import db

main_bp = Blueprint('main_bp', __name__, template_folder='templates')


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
def index():
    form= PostTransportistas()    
    return render_template('main/index.html', title='Carga rápido, ahorra más', form=form)


@main_bp.route('/transportistas', methods=['GET', 'POST'])  
def transportistas():
    form = PostTransportistas()
    if form.validate_on_submit():
        print(form.__dict__)
        if not current_user.is_authenticated:
            flash("Regístrate para encontrar cargas!")
            return redirect(url_for('user_bp.register'))
        post = FletesTransportistas(origen=form.origen.data, destino=form.destino.data, equipo=form.equipo.data, \
            precio_total_deseado=form.precio_total_deseado.data, precio_por_unidad_deseado=form.precio_por_unidad_deseado.data, descripcion=form.descripcion.data, \
            contacto=form.contacto.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Listo, en poco tiempo encontrarás carga")
        return redirect(url_for('main_bp.transportistas'))
    page = request.args.get('page', 1, type=int)
    posts = CargasEmbarcadores.query.order_by(CargasEmbarcadores.timestamp.desc()).paginate(page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('main_bp.transportistas', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main_bp.transportistas', page=posts.prev_num) if posts.has_prev else None
    return render_template('main/transportistas.html', title='Encuentra carga, rápido', posts=posts.items, next_url=next_url, prev_url=prev_url, form=form)


@main_bp.route('/embarcadores', methods=['GET', 'POST'])  
def embarcadores():
    form = PostEmbarcadores()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Regístrate para encontrar transportistas!")
            return redirect(url_for('user_bp.embarcadores'))
        post = CargasEmbarcadores(origen=form.origen.data, destino=form.destino.data, equipo_solicitado=form.equipo_solicitado.data, \
            carga= form.carga.data, precio_total_ofertado=form.precio_total_ofertado.data, precio_por_unidad_ofertado=form.precio_por_unidad_ofertado.data, descripcion=form.descripcion.data, \
            contacto=form.contacto.data, user=current_user)
        
        db.session.add(post)
        db.session.commit()
        flash("Listo, en poco tiempo encontrarás un transportista")
        return redirect(url_for('main_bp.embarcadores'))
    page = request.args.get('page', 1, type=int)
    posts = FletesTransportistas.query.order_by(FletesTransportistas.timestamp.desc()).paginate(page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('main_bp.embarcadores', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main_bp.embarcadores', page=posts.prev_num) if posts.has_prev else None
    return render_template('main/embarcadores.html', title='Envía tu mercancía, facil', posts=posts.items, next_url=next_url, prev_url=prev_url, form=form)

@main_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactForm()
    if form.validate_on_submit():
        feedback = ContactTable(asunto=form.asunto.data, body=form.body.data)
        db.session.add(feedback)
        db.session.commit()
        flash("Gracias por tus comentarios!")
        return redirect(url_for('main_bp.contacto'))
    return render_template('main/contacto.html', title='Contáctanos', form=form)

#@main_bp.before_app_request
#def before_request():
#    if current_user.is_authenticated:
#        g.search_form = SearchForm()

@main_bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('.transportistas'))
    page = request.args.get('page', 1, type=int)
    Post.reindex()
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    print(posts, total)
    print(posts, total)
    next_url = url_for('.search', q=g.search_form.q.data, page=page+1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('.search', q=g.search_form.q.data, page=page-1) if page > 1 else None
    return render_template('main/search.html', title = 'Buscar Fletes', posts=posts, next_url=next_url, prev_url=prev_url)


@main_bp.route('/posts/<role>/<post_id>', methods=['GET', 'POST'])
def posts(role, post_id):
    
    form = Comments()
    page = request.args.get('page', 1, type=int)
    if role== "cargasembarcadores":
        oferta = CargasEmbarcadores.query.filter_by(id=post_id).first_or_404()
        comments = db.session.query(CommentsCargasEmbarcadores).filter(CommentsCargasEmbarcadores.carga_id==post_id).order_by(CommentsCargasEmbarcadores.timestamp.desc()).paginate(page, Config.POSTS_PER_PAGE, False)
    elif role =="fletestransportistas":
        oferta = FletesTransportistas.query.filter_by(id=post_id).first_or_404()
        comments = db.session.query(CommentsFletesTransportistas).filter(CommentsFletesTransportistas.flete_id==post_id).order_by(CommentsFletesTransportistas.timestamp.desc()).paginate(page, Config.POSTS_PER_PAGE, False)
    if request.method == 'GET':
        next_url = url_for('main_bp.posts', role=oferta.__tablename__, post_id=oferta.id, page=comments.next_num) if comments.has_next else None
        prev_url = url_for('main_bp.posts', role=oferta.__tablename__, post_id=oferta.id, page=comments.prev_num) if comments.has_prev else None
        return render_template('main/oferta.html', oferta=oferta, comments=comments.items, next_url=next_url, prev_url=prev_url, form=form)

    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('auth_bp.login'))
        if 'delete' in request.form:
            db.session.delete(oferta)
            db.session.commit()
            if role == "cargasembarcadores":
                flash("Tu anuncio se ha borrado correctamente")
                return redirect(url_for('.transportistas'))
            elif role == "fletestransportistas":
                flash("Tu anuncio se ha borrado correctamente")
                return redirect(url_for('.embarcadores'))
        if 'comment' in request.form and form.validate_on_submit():
            if role== "cargasembarcadores":
                comment = CommentsCargasEmbarcadores(body=form.comment.data, username=current_user.username, carga_id=post_id)
            elif role =="fletestransportistas":
                comment = CommentsFletesTransportistas(body=form.comment.data, username=current_user.username, flete_id=post_id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('main_bp.posts', role=oferta.__tablename__, post_id=oferta.id))
        elif 'comment_id'in list(request.args):
            print('deleting')
            comment_id = request.args.get('comment_id')
            if role == 'fletestransportistas':
                comment_to_delete = CommentsFletesTransportistas.query.filter_by(id=comment_id).first_or_404()
            elif role == 'cargasembarcadores':
                comment_to_delete = CommentsCargasEmbarcadores.query.filter_by(id=comment_id).first_or_404()
            db.session.delete(comment_to_delete)
            db.session.commit()
            return redirect(url_for('main_bp.posts', role=oferta.__tablename__, post_id=oferta.id))







# @TODO - implement edit
@main_bp.route('/edit_post', methods=['GET', 'POST'])
def edit_post():
    if request.method == 'POST':
        if 'edit' in request.form:
            print('edit')
        if 'delete' in request.form:
            print('delete')
    return render_template('main/index.html')

@main_bp.route('/trial', methods=['GET', 'POST'])
def trial():
    return render_template('main/trial.html', title='trial')


@main_bp.route('/API_FB_login', methods=['POST'])
def API_FB_login():
    print('request received')
    return request


@main_bp.route('/privacidad')
def privacidad():
    return render_template('main/privacidad.html', title="Aviso de Privacidad")