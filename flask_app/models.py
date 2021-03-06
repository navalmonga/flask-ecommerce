from datetime import datetime
from flask_app import db, login_manager
from flask_login import UserMixin

import pyotp

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)
  otp_secret = db.Column(db.String(16), nullable=False)
  picture_url = db.Column(db.String(60), nullable=True)

  listings = db.relationship('Listing', backref='author', lazy=True)
  cart = db.relationship('CartItem', backref='user', lazy=True)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    # self.otp_secret = base64.b32encode(os.urandom(10)).decode()
    self.otp_secret = pyotp.random_base32()
    
  def get_auth_uri(self):
    servicer = 'SOLDBY.IO'

    return ('otpauth://totp/{0}:{1}?secret={2}&issuer={0}'.format(
        servicer, self.username, self.otp_secret
    ))
  
  def verify_totp(self, token):
    totp_client = pyotp.TOTP(self.otp_secret)
    return totp_client.verify(token)

  def __repr__(self):
    return "User('%s','%s')" % (self.username, self.email)

class Listing(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  description = db.Column(db.Text, nullable = False)
  price_in_pennies = db.Column(db.Integer, nullable = False)
  picture_url = db.Column(db.String(60), nullable=False)
  date = db.Column(db.DateTime, nullable=False, default=datetime.now)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  cart = db.relationship('CartItem', backref='listing', lazy=True)
  
  def __repr__(self):
    return "Listing('%s','%s','%s')" % (self.title, self.description, self.price_in_pennies)

class CartItem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  counter = db.Column(db.Integer)
  price = db.Column(db.Integer)
  listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)