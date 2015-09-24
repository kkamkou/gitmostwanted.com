from flask import Blueprint, make_response

user_profile = Blueprint('user_profile', __name__)


@user_profile.route('/<name>')
def profile_view(name):
    return make_response(name, 404)
