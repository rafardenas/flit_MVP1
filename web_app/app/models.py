from hashlib import md5
from datetime import datetime, timedelta
from web_app.app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from web_app.config2 import Config
from time import time
import jwt
from web_app.app import login, db
from web_app.app.search import add_to_index, remove_from_index, query_index

db.metadata.clear()


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        print(cls, expression)
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for ob in session._changes['delete']:
            if isinstance(SearchableMixin, obj):
                remove_from_index(obj.__tablename__, obj)    
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

#db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
#db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

followers = db.Table('followers', 
            db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
            db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
            )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    rol = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('FletesTransportistas', backref='user', lazy='dynamic')
    posts2 = db.relationship('CargasEmbarcadores', backref='user', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow() - timedelta(hours=5, minutes=0))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    #relations table
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    
    #The "c" is an attribute of SQLAlchemy tables that are not defined as models. 
    #For these tables, the table columns are all exposed as sub-attributes of this "c" attribute

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed =  Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)     
        own = Post.query.filter_by(user_id=self.id)  #in order to displays one's own Posts
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password':self.id, 'exp':time() + expires_in}, Config.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    __tablename__ = 'post'
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow() - timedelta(hours=5, minutes=0))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class FletesTransportistas(db.Model):
    __tablename__ = 'fletestransportistas'
    __searchable__ = ['origen', 'destino', 'descripcion']
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(140))
    destino = db.Column(db.String(140))
    equipo = db.Column(db.String(140), default=None)
    helper = db.Column(db.String(140), default=None) #columna para que ambas tablas tengan el mismo numero de columnas y hacer UNION
    precio_total_deseado = db.Column(db.Float, default=0.0)
    precio_por_unidad_deseado = db.Column(db.Float, default=0.0)
    descripcion = db.Column(db.String(140))
    contacto = db.Column(db.String(140), default="Sin m??s informaci??n")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow() - timedelta(hours=5, minutes=0))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('CommentsFletesTransportistas', backref='fletestransportistas', lazy='dynamic')

    def __repr__(self):
        return '<FletesTransportistas {}>'.format(self.descripcion)


class CargasEmbarcadores(SearchableMixin, db.Model):
    __tablename__ = 'cargasembarcadores'
    __searchable__ = ['origen', 'destino', 'descripcion']
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(140))
    destino = db.Column(db.String(140))
    equipo_solicitado = db.Column(db.String(140), default="Sin m??s informaci??n")   #caja seca, redilas, plataforma, etc
    carga = db.Column(db.String(140), default="Sin m??s informaci??n")
    precio_total_ofertado = db.Column(db.Float, default=0.0)
    forma_de_pago = db.Column(db.String(200), default=0.0)
    descripcion = db.Column(db.String(140))
    contacto = db.Column(db.String(140), default="Sin m??s informaci??n")
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow() - timedelta(hours=5, minutes=0))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('CommentsCargasEmbarcadores', backref='cargasembarcadores', lazy='dynamic')

    def __repr__(self):
        return '<CargasEmbarcadores {}>'.format(self.descripcion)
    
class ContactTable(db.Model):
    __tablename__ = 'contacto'
    id = db.Column(db.Integer, primary_key=True)
    asunto = db.Column(db.String(140))
    body = db.Column(db.String(140))
    contacto = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow() - timedelta(hours=5, minutes=0))

class CommentsFletesTransportistas(db.Model):
    __tablename__ = 'comentariosfletestransportistas'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username = db.Column(db.String(300))
    flete_id = db.Column(db.Integer, db.ForeignKey('fletestransportistas.id'))

class CommentsCargasEmbarcadores(db.Model):
    __tablename__ = 'comentarioscargasembarcadores'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow() - timedelta(hours=5, minutes=0))
    username = db.Column(db.String(300))
    carga_id = db.Column(db.Integer, db.ForeignKey('cargasembarcadores.id'))


    

