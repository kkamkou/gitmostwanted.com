from flask import Blueprint, render_template

static_content = Blueprint('static_content', __name__)


@static_content.route('/static/sponsorship/')
def sponsorship():
    return render_template('static/sponsorship.html')
