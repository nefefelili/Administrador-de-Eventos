from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#carga usuario desde el login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#roles(admin, organizador, participante)
class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    users = db.relationship('User', backref='role', lazy=True)

#uusuarios
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    eventos = db.relationship('Evento', backref='organizador', lazy=True)

    def set_password(self, password: str):
        """Generates and stores the hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks if the given password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

#eventos
class Evento(db.Model):
    __tablename__ = 'evento'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    organizador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)