# @todo! refactor this part. most probably it should be moved to the Repo model
def repository_filtered(request, languages, model, q):
    lang = request.args.get('lang')
    if lang != 'All' and (lang,) in languages:
        q = q.filter(model.language == lang)

    status = request.args.get('status')
    if status in ('promising', 'hopeless'):
        q = q.filter(model.status == status)

    if bool(request.args.get('mature')):
        q = q.filter(model.mature.is_(True))

    return q
