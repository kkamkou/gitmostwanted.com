from flask import abort, Blueprint, render_template
from gitmostwanted.models.repo import Repo, RepoMean

repo_information = Blueprint('repo_information', __name__)


@repo_information.route('/repository/details/<int:repo_id>')
def details(repo_id):
    repo = Repo.query.get(repo_id)
    if not repo:
        return abort(404)

    means = RepoMean.query.filter(RepoMean.repo_id == repo_id)

    return render_template('repository/details.html', entry=repo, means=means)
