import argparse
import sys

from celeryconfig import beat_schedule
from gitmostwanted.app import celery, log


def parse_tasks(argv: list[str]) -> list[str]:
    choices = sorted(beat_schedule.keys())
    parser = argparse.ArgumentParser(
        description='Run scheduled Celery tasks synchronously.',
        epilog='Available tasks: ' + ', '.join(choices)
    )
    parser.add_argument(
        '-t', '--task',
        action='append',
        choices=choices,
        dest='opt_tasks',
        metavar='TASK',
        help='Task name from beat_schedule to execute'
    )
    parser.add_argument(
        'pos_tasks',
        nargs='*',
        choices=choices,
        metavar='TASK',
        help='Task name(s) from beat_schedule to execute'
    )
    args = parser.parse_args(argv)
    selected = (args.opt_tasks or []) + (args.pos_tasks or [])
    if not selected:
        parser.print_help()
        sys.exit(1)
    return selected


def run_task(name: str) -> None:
    celery.loader.import_default_modules()
    cfg = beat_schedule[name]
    task = celery.tasks[cfg['task']]
    args = cfg.get('args', ())
    log.info('Running task %s (%s) with args %s', name, cfg['task'], args)
    task.apply(args=args, throw=True)
    log.info('Task %s completed', name)


if __name__ == '__main__':
    for item in parse_tasks(sys.argv[1:]):
        run_task(item)
