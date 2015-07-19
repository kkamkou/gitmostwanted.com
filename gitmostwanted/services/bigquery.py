from gitmostwanted.bigquery.service import ServiceGmw


def instance(app):
    cfg = app.config['GOOGLE_BIGQUERY']
    return ServiceGmw(cfg['account_name'], cfg['private_key_path'], cfg['project_id'])
