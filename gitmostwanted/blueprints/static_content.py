from flask import Blueprint, render_template

static_content = Blueprint('static_content', __name__)


@static_content.route('/static/donations/')
def donations():
    return render_template('static/donations.html')
