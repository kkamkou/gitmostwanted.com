from datetime import datetime
from urllib.parse import urlparse

from flask import abort, Blueprint, flash, g, redirect, render_template, request, url_for

from gitmostwanted.app import app, db, log
from gitmostwanted.lib.github import api
from gitmostwanted.lib.regex import RepoFullName
from gitmostwanted.models.repo import Repo, RepoMean, RepoTopics

repo_information = Blueprint('repo_information', __name__)


@repo_information.route('/repository/details/<int:repo_id>')
def details(repo_id):
    repo = db.session.get(Repo, repo_id)
    if not repo:
        return abort(404)

    means = RepoMean.query.filter(RepoMean.repo_id == repo_id)

    return render_template('repository/details.html', entry=repo, means=means)


@repo_information.route('/repository', methods=['POST'])
def add():
    if not g.user:
        return abort(403)
    try:
        repo = create(RepoFullName(request.form.get('full_name', '')))
        log.info('Repository %s(%s) has been added by user %s', repo.id, repo.full_name, g.user.id)
        flash('The repository has been successfully added', 'success')
    except ValueError as err:
        flash(str(err), 'alert')
    return redirect(
        request.referrer
        if request.referrer and urlparse(request.referrer).netloc in ('', request.host)
        else url_for('repo_rating.top')
    )


def create(name: RepoFullName) -> Repo:
    if Repo.get_one_by_full_name(str(name)):
        raise ValueError('The repository is already in the database')
    info, _ = api.repo_info(str(name))
    return persist(validate(info))


def validate(info: dict) -> dict:
    if not info:
        raise ValueError('The repository is not found on GitHub')
    if db.session.get(Repo, info['id']) or Repo.get_one_by_full_name(info['full_name']):
        raise ValueError('The repository is already in the database')
    if info.get('fork') or info.get('archived') or info.get('disabled'):
        raise ValueError('Forked, archived, or disabled repositories are not supported')
    if info.get('stargazers_count', 0) < app.config['REPOSITORY_STARS_MIN']:
        raise ValueError(
            'The repository must have at least {} stars'.format(app.config['REPOSITORY_STARS_MIN'])
        )
    return info


def persist(info: dict) -> Repo:
    repo = Repo(
        id=info['id'],
        checked_at=datetime.now(),
        created_at=datetime.strptime(info['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
        description=info.get('description'),
        forks_count=info.get('forks_count', 0),
        full_name=info['full_name'],
        homepage=info.get('homepage'),
        html_url=info['html_url'],
        language=info.get('language'),
        license=info['license'].get('key', 'unlicense')[:20] if info.get('license') else None,
        mature=True,
        name=info['name'],
        open_issues_count=info.get('open_issues_count', 0),
        size=info.get('size', 0),
        stargazers_count=info.get('stargazers_count', 0),
        subscribers_count=info.get('subscribers_count', 0),
        topics=[
            RepoTopics(title=t) for t in sorted({t[:30] for t in (info.get('topics') or []) if t})
        ]
    )
    db.session.add(repo)
    db.session.commit()
    return repo
