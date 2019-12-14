from flask import render_template, url_for, redirect, request, current_app, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required

from flask_app import db, bcrypt
from flask_app.models import Listing
from flask_app.listings.forms import CreateForm


listings = Blueprint('listings', __name__)

@listings.route("/create-listing", methods=['GET', 'POST'])
@login_required
def create_listing():
    form = CreateForm()

    if form.validate_on_submit():
        listing = Listing(title=form.item_name.data, description=form.item_desc.data, price_in_pennies=form.price.data, picture_url=form.item_picture_url.data, user_id=current_user.id)
        db.session.add(listing)
        db.session.commit()

        return redirect(url_for('users.account'))
    
    return render_template('create_listing.html', title='Create Listing', form=form)
