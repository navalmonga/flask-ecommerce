from flask import render_template, Blueprint, request, current_app, redirect, url_for
from flask_login import current_user
from flask_app.models import Listing, User

import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json


def create_plot():
  N = 40
  x = np.linspace(0, 1, N)
  y = np.random.randn(N)
  df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


  data = [
      go.Bar(
          x=df['x'], # assign x as the dataframe column 'x'
          y=df['y']
      )
  ]
  print(data)
  graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

  return graphJSON

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

@main.route("/plotly")
def plotly():
  listings = Listing.query.all()
  users = User.query.all()
  numUsers = len(users)
  numListings = len(listings)
  fig = go.Figure(
    data=[go.Bar(y=[numListings])],
    layout_title_text="Active Listings"
  )
  fig2 = go.Figure(
    data=[go.Bar(y=[numUsers])],
    layout_title_text="Active Users"
  )
  fig.show()
  fig2.show()
  #bar = create_plot()
  return render_template('plotly.html', title='Plotly')

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