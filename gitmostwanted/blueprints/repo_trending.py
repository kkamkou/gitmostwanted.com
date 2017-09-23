from flask import abort, Blueprint, g, request, render_template
from gitmostwanted.models.repo import Repo, RepoMean
from gitmostwanted.models.user import UserAttitude
from gitmostwanted.models import report
from gitmostwanted.app import db

repo_trending = Blueprint('repo_trending', __name__)


@repo_trending.route('/trending/', defaults={'rng': 'day'})
@repo_trending.route('/trending/<rng>/')
def list_by_range(rng):
    map_list = {'day': 'ReportAllDaily', 'week': 'ReportAllWeekly', 'month': 'ReportAllMonthly'}
    model = getattr(report, map_list.get(rng, map_list.get('day')))

    query = Repo.filter_by_args(model.query, request.args)\
        .join(Repo)\
        .order_by(model.cnt_watch.desc())

    if not g.user:
        query = query.add_columns(db.null())
    else:
        query = UserAttitude.join_by_user_and_repo(query, g.user.id, Repo.id)\
            .add_columns(UserAttitude.attitude)

    return render_template('index.html', entries=query, languages=Repo.language_distinct(), rng=rng)


@repo_trending.route('/trending/details/<int:repo_id>')
def details(repo_id):
    repo = Repo.query.get(repo_id)
    if not repo:
        return abort(404)

    means = RepoMean.query.filter(RepoMean.repo_id == repo_id)

    return render_template('repository/details.html', entry=repo, means=means)
