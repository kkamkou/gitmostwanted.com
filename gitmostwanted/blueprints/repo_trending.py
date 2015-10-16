from flask import Blueprint, g, request, render_template
from gitmostwanted.blueprints.mixin import repository_filtered
from gitmostwanted.models.repo import Repo
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models import report
from gitmostwanted.app import db

repo_trending = Blueprint('repo_trending', __name__)


@repo_trending.route('/', defaults={'rng': 'day'})
@repo_trending.route('/trending/<rng>/')
def list_by_range(rng):
    map_list = {'day': 'ReportAllDaily', 'week': 'ReportAllWeekly', 'month': 'ReportAllMonthly'}
    if rng not in map_list:
        rng = 'day'

    model = getattr(report, map_list[rng])
    lngs = Repo.language_distinct()

    if not g.user:
        query = model.query.join(Repo).add_columns(db.null())
    else:
        query = model.query\
            .join(Repo)\
            .add_columns(UserAttitude.attitude)\
            .outerjoin(
                UserAttitude,
                (UserAttitude.user_id == g.user.id) & (UserAttitude.repo_id == Repo.id)
            )

    query = repository_filtered(request, lngs, Repo, query)\
        .order_by(model.cnt_watch.desc())

    return render_template('index.html', entries=query, languages=lngs)
