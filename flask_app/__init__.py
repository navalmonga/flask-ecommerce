from logging.config import dictConfig

from flask import Flask
from flask_talisman import Talisman
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

csp = {
  'default-src': [
    '\'self\'',
  ],
  'script-src': [
    'https://code.jquery.com/',
    'https://cdn.jsdelivr.net/',
    'https://stackpath.bootstrapcdn.com/bootstrap/',
    'https://kit.fontawesome.com/f69b7244e9.js',
    'https://use.fontawesome.com/',
    '\'self\''
  ],
  'style-src': [
    'https://stackpath.bootstrapcdn.com/bootstrap/',
    'https://kit-free.fontawesome.com',
    'https://fonts.googleapis.com/',
    'https://use.fontawesome.com/',
    '\'self\'',
    '\'unsafe-inline\''
  ],
  'font-src': [
    'https://fonts.googleapis.com/',
    'https://fonts.gstatic.com/',
    'https://kit-free.fontawesome.com/',
    'https://use.fontawesome.com/',
    'data:',
    '\'self\'',
    '\'unsafe-inline\''
  ],
  'style-src-elem': [
    '\'self\'',
    '\'unsafe-inline\'',
    '*'
  ],
  'img-src': [
    '\'self\'',
    'data:',
    '*',
  ],
  'media-src': [
    'https://jlassets.s3.amazonaws.com/',
  ],
}

dictConfig(
  {
    "version": 1,
    "formatters": {
      "default": {
        "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
      }
    },
    "handlers": {
      "wsgi": {
        "class": "logging.StreamHandler",
        "stream": "ext://flask.logging.wsgi_errors_stream",
        "formatter": "default",
      }
    },
    "root": {"level": "INFO", "handlers": ["wsgi"]},
  }
)

talisman = Talisman(content_security_policy=csp)
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = b'0)\x08\xe3\xc9\xc8\x83\xb8\xf1\xda\xdb\xd7\xb3\x0eT\x17'

  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  talisman.init_app(app)
  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)

  talisman.content_security_policy = csp
  talisman.content_security_policy_report_uri = '/csp_error_handling'

  from flask_app.main.routes import main
  from flask_app.users.routes import users
  from flask_app.listings.routes import listings
  from flask_app.cart.routes import cart

  app.register_blueprint(main)
  app.register_blueprint(users)
  app.register_blueprint(listings)
  app.register_blueprint(cart)

  with app.app_context():
    db.create_all()
  return app