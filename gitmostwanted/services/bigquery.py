from gitmostwanted.lib.bigquery.service import ServiceGmw


def instance(app):
    """:rtype: ServiceGmw"""
    cfg = app.config['GOOGLE_BIGQUERY']
    return ServiceGmw(cfg['json_key_path'], cfg['project_id'])
