from flask import Blueprint, g, request, render_template
from gitmostwanted.models.repo import Repo
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models import report
from gitmostwanted.app import db

repo_trending = Blueprint('repo_trending', __name__)


@repo_trending.route('/', defaults={'rng': 'day'})
@repo_trending.route('/trending/<rng>/')
def list_by_range(rng):
    map_list = {'day': 'ReportAllDaily', 'week': 'ReportAllWeekly', 'month': 'ReportAllMonthly'}
    model = getattr(report, map_list.get(rng, map_list.get('day')))

    query = model.query.join(Repo).order_by(model.cnt_watch.desc())
    if not g.user:
        return list_by_range_filtered(query.add_columns(db.null()))

    return list_by_range_filtered(
        query.add_columns(UserAttitude.attitude).outerjoin(
            UserAttitude,
            (UserAttitude.user_id == g.user.id) & (UserAttitude.repo_id == Repo.id)
        )
    )


def list_by_range_filtered(query):
    langs = Repo.language_distinct()

    lang = request.args.get('lang')
    if lang != 'All' and (lang,) in langs:
        query = query.filter(Repo.language == lang)

    status = request.args.get('status')
    if status in ('promising', 'hopeless'):
        query = query.filter(Repo.status == status)

    if bool(request.args.get('mature')):
        query = query.filter(Repo.mature.is_(True))

    return render_template('index.html', entries=query, languages=langs)
