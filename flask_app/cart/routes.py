from flask import render_template, url_for, redirect, request, current_app, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required

from flask_app import db, bcrypt
from flask_app.models import CartItem
from flask_app.cart.forms import AddToCartForm
from flask_login import current_user

cart = Blueprint('cart', __name__)

@cart.route("/cart", methods=['GET'])
@login_required
def user_cart():
    #form = PurchaseForm()

    #if form.validate_on_submit():
    #   return redirect(url_for('users.account'))
    user_cart_listings = current_user.cart
    print(user_cart_listings)
    return render_template('cart.html', title='Cart', cart=user_cart_listings)

@cart.route("/remove_from_cart/<listing_id>")
def remove_from_cart(listing_id):
    cart_item = CartItem.query.filter_by(id=listing_id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    return redirect(url_for('cart.user_cart'))


@cart.route("/cart/<listing_id>")
@login_required
def add_to_cart(listing_id):
   cart = CartItem(listing_id=listing_id, user_id=current_user.id)
   db.session.add(cart)
   db.session.commit()
   return redirect(url_for('cart.user_cart'))

