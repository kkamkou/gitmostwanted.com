from flask import\
    abort, Blueprint, g, make_response, request, render_template_string, render_template
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models.repo import Repo
from gitmostwanted.app import db

user_attitude = Blueprint('user_attitude', __name__)


def verify_attitude(attitude):
    return attitude in ['like', 'dislike', 'neutral']


@user_attitude.before_request
def verify_user():
    if not g.user:
        return abort(403)


def query(filter_by):
    q = Repo.query.filter(filter_by).outerjoin(
        UserAttitude,
        db.and_(
            UserAttitude.user_id == g.user.id,
            UserAttitude.repo_id == Repo.id
        )
    )

    languages = Repo.language_distinct()

    lang = request.args.get('lang')
    if lang != 'All' and (lang,) in languages:
        q = q.filter(Repo.language == lang)

    return q


@user_attitude.route('/attitude/<int:repo_id>/<attitude>')
def change(repo_id, attitude):
    if not verify_attitude(attitude):
        return abort(403)

    if not Repo.query.get(repo_id):
        return abort(404)

    db.session.merge(UserAttitude(user_id=g.user.id, repo_id=repo_id, attitude=attitude))
    db.session.commit()

    return make_response(render_template_string('Ok'), 204)


@user_attitude.route('/unchecked/', defaults={'page': 1})
@user_attitude.route('/unchecked/<int:page>')
def unchecked(page):
    entries = query(UserAttitude.repo_id.is_(None))\
        .add_columns(db.null())\
        .paginate(page if page > 0 else 1, per_page=20, error_out=False)
    if entries.pages and entries.pages < entries.page:
        return unchecked(entries.pages)
    return render_template(
        'attitude.html', repos=entries, languages=Repo.language_distinct()
    )


@user_attitude.route('/attitude/<attitude>', defaults={'page': 1})
@user_attitude.route('/attitude/<attitude>/<int:page>')
def list_by_attitude(attitude, page):
    if not verify_attitude(attitude):
        return abort(403)

    entries = query(UserAttitude.attitude == attitude) \
        .add_columns(UserAttitude.attitude)\
        .paginate(page if page > 0 else 1, per_page=20, error_out=False)
    if entries.pages and entries.pages < entries.page:
        return list_by_attitude(attitude, entries.pages)

    return render_template('attitude.html', repos=entries, attitude=attitude)
