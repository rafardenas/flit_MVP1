from flask import Blueprint, render_template, flash, redirect, url_for, request, g
from flask.globals import current_app
from flask_login import current_user, login_user, logout_user, login_required
from web_app.app.forms import SearchForm, PostTransportistas, PostEmbarcadores    
from web_app.app.models import FletesTransportistas, CargasEmbarcadores
from werkzeug.urls import url_parse
from web_app.config2 import Config
from web_app.app import db

main_bp = Blueprint('main_bp', __name__, template_folder='templates')


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
def index():    
    return render_template('main/index.html', title='Inicio')


"""
@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Listing is posted now!")
        return redirect(url_for('main_bp.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, Config.POSTS_PER_PAGE, False)   
    #calling a'all' in the last query triggers the execution, we call 'pagination' here instead
    next_url = url_for('main_bp.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main_bp.index', page=posts.prev_num) if posts.has_prev else None

    return render_template('main/index.html', title='Inicio', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)
"""

@main_bp.route('/transportistas', methods=['GET', 'POST'])  
def transportistas():
    form = PostTransportistas()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Regístrate para encontrar cargas!")
            return redirect(url_for('user_bp.register'))
        post = FletesTransportistas(origen=form.origen.data, destino=form.destino.data, equipo=form.equipo.data, \
            precio_total_deseado=form.precio_total_deseado.data, precio_por_unidad_deseado=form.precio_por_unidad_deseado.data, descripcion=form.descripcion.data, \
            contacto=form.contacto.data, user_id=current_user.id)
        print(form.__dict__)
        print(post.__dict__)
        db.session.add(post)
        db.session.commit()
        flash("Listo, en poco tiempo alguien te contactará")
        return redirect(url_for('main_bp.transportistas'))
    page = request.args.get('page', 1, type=int)
    posts = CargasEmbarcadores.query.order_by(CargasEmbarcadores.timestamp.desc()).paginate(page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('main_bp.transportistas', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main_bp.transportistas', page=posts.prev_num) if posts.has_prev else None
    return render_template('main/transportistas.html', title='Encuentra carga, rápido', posts=posts.items, next_url=next_url, prev_url=prev_url, form=form, user=current_user.username)


@main_bp.route('/embarcadores', methods=['GET', 'POST'])  
def embarcadores():
    #TODO: change the query to the correct table
    form = PostEmbarcadores()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Regístrate para encontrar transportistas!")
            return redirect(url_for('user_bp.register'))
        post = CargasEmbarcadores(origen=form.origen.data, destino=form.destino.data, equipo_solicitado=form.equipo_solicitado.data, \
            precio_total_ofertado=form.precio_total_ofertado.data, precio_por_unidad_ofertado=form.precio_por_unidad_ofertado.data, descripcion=form.descripcion.data, \
            contacto=form.contacto.data, user=current_user)
        print(current_user)
        db.session.add(post)
        db.session.commit()
        flash("Listo, en poco tiempo encontrarás un transportista")
        return redirect(url_for('main_bp.embarcadores'))
    page = request.args.get('page', 1, type=int)
    posts = FletesTransportistas.query.order_by(FletesTransportistas.timestamp.desc()).paginate(page, Config.POSTS_PER_PAGE, False)
    next_url = url_for('main_bp.embarcadores', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main_bp.embarcadores', page=posts.prev_num) if posts.has_prev else None
    return render_template('main/embarcadores.html', title='Envía tu mercancía, facil', posts=posts.items, next_url=next_url, prev_url=prev_url, form=form)



@main_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()

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
