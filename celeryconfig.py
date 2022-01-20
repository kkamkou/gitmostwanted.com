from celery.schedules import crontab


timezone = 'Europe/Berlin'

include = (
    'gitmostwanted.tasks.repo_most_starred', 'gitmostwanted.tasks.repo_stars',
    'gitmostwanted.tasks.repo_metadata', 'gitmostwanted.tasks.repo_status',
    'gitmostwanted.tasks.github'
)

# celery beat
beat_schedule = {
    'metadata-refresh': {
        'task': 'gitmostwanted.tasks.repo_metadata.metadata_refresh',
        'schedule': crontab(minute=30, hour=0),
        'args': [14]
    },
    'metadata-erase': {
        'task': 'gitmostwanted.tasks.repo_metadata.metadata_erase',
        'schedule': crontab(minute=50, hour=0)
    },
    'metadata-maturity': {
        'task': 'gitmostwanted.tasks.repo_metadata.metadata_maturity',
        'schedule': crontab(minute=30, hour=1),
        'args': [3]
    },
    'metadata-trend': {
        'task': 'gitmostwanted.tasks.repo_metadata.metadata_trend',
        'schedule': crontab(minute=0, hour=5, day_of_month=1),
        'args': [56]
    },
    'most-starred-day': {
        'task': 'gitmostwanted.tasks.repo_most_starred.most_starred_day',
        'schedule': crontab(minute=0, hour=8)
    },
    'most-starred-week': {
        'task': 'gitmostwanted.tasks.repo_most_starred.most_starred_week',
        'schedule': crontab(minute=0, hour=9, day_of_week=0)
    },
    'most-starred-month': {
        'task': 'gitmostwanted.tasks.repo_most_starred.most_starred_month',
        'schedule': crontab(minute=0, hour=10, day_of_month=1)
    },
    'status-refresh': {
        'task': 'gitmostwanted.tasks.repo_status.status_refresh',
        'schedule': crontab(minute=0, hour=3),
        'args': [28]
    },
    'status-detect': {
        'task': 'gitmostwanted.tasks.repo_status.status_detect',
        'schedule': crontab(minute=30, hour=4),
        'args': [28, 4]
    },
    'stars-mature': {
        'task': 'gitmostwanted.tasks.repo_stars.stars_mature',
        'schedule': crontab(minute=30, hour=3, day_of_week='*/2'),
        'args': [28]
    }
}
