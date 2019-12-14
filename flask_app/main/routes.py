from flask import render_template, Blueprint, request, current_app, redirect, url_for
from flask_login import current_user
from flask_app.models import Listing, User

import json

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/listings")
def index():
  if not current_user.is_authenticated:
    return redirect(url_for('main.welcome'))
  listings = Listing.query.all()
  return render_template('index.html', title='Home', listings=listings)

@main.route("/welcome")
def welcome():
  return render_template('splash.html', title='Welcome')

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/user/<username>")
def user_detail(username):
    user = User.query.filter_by(username=username).first()
    
    return render_template('user_detail.html', user=user, listings=user.listings)

@main.route("/csp_error_handling", methods=["POST"])
def report_handler():
    """
    Receives POST requests from the browser whenever the Content-Security-Policy 
    is violated. Processes the data and logs an easy-to-read version of the message
    in your console.
    """
    report = json.loads(request.data.decode())["csp-report"]

    # current_app.logger.info(json.dumps(report, indent=2))

    violation_desc = "\nViolated directive: %s, \nBlocked: %s, \nOriginal policy: %s \n" % (
        report["violated-directive"],
        report["blocked-uri"],
        report["original-policy"]
    )

    current_app.logger.info(violation_desc)
    return redirect(url_for("main.index"))