from flask import Blueprint, g, request, render_template

from gitmostwanted.app import db
from gitmostwanted.models import report
from gitmostwanted.models.repo import Repo
from gitmostwanted.models.user import UserAttitude

repo_trending = Blueprint('repo_trending', __name__)


@repo_trending.route('/trending/', defaults={'rng': 'week'})
@repo_trending.route('/trending/<rng>/')
def list_by_range(rng):
    map_list = {'week': 'ReportAllWeekly', 'month': 'ReportAllMonthly'}
    model = getattr(report, map_list.get(rng, map_list.get('week')))

    query = Repo.filter_by_args(model.query, request.args)\
        .join(Repo)\
        .order_by(model.cnt_watch.desc())

    if not g.user:
        query = query.add_columns(db.null())
    else:
        query = UserAttitude.join_by_user_and_repo(query, g.user.id, Repo.id)\
            .with_entities(model, UserAttitude.attitude)

    return render_template('index.html', entries=query, languages=Repo.language_distinct(), rng=rng)
