![CI](https://github.com/kkamkou/gitmostwanted.com/workflows/CI/badge.svg)
[![Code Climate](https://codeclimate.com/github/kkamkou/gitmostwanted.com/badges/gpa.svg)](https://codeclimate.com/github/kkamkou/gitmostwanted.com)
[![Coverage Status](https://coveralls.io/repos/github/kkamkou/gitmostwanted.com/badge.svg?branch=HEAD)](https://coveralls.io/github/kkamkou/gitmostwanted.com?branch=HEAD)
[![0pdd](https://www.0pdd.com/svg?name=kkamkou/gitmostwanted.com)](https://www.0pdd.com/p?name=kkamkou/gitmostwanted.com)

# gitmostwanted
Advanced explore of github.com. Our goal is to highlight the most interesting repositories and exclude others. You can find some concepts in the [Wiki](https://github.com/kkamkou/gitmostwanted.com/wiki).

If you would like to help the project, please consider these topics:
- GMW uses [Google BigQuery](https://cloud.google.com/bigquery/pricing) and the service is **pretty** expensive.
- GMW is located on a private machine.

## Run (Python3)

```bash
# export PYTHONPATH="`pwd`:${PYTHONPATH}"
# export GMW_APP_ENV=production
cp instance.cfg.distr /path/to/instance.cfg
export GMW_APP_SETTINGS=/path/to/instance.cfg
python gitmostwanted/web.py
```

## Tests

```bash
export GMW_APP_ENV=testing
pip install pytest pytest-pep8 responses
py.test --pep8 gitmostwanted tests/unit
# py.test --pep8 --cov . --cov-report annotate gitmostwanted tests/unit
```

## Docker
Run it two times as the first time **it'll fail** (see: #224). Default port is `5000`.

```bash
cp instance.cfg.distr instance.cfg
# modify instance.cfg if needed
```

### Non-persistent
```bash
[sudo] docker-compose up --detach
```

### Persistent variant
```bash
# modify paths and envs in docker-compose-persistent.yml
[sudo] docker-compose \
    -f docker-compose.yml -f docker-compose-persistent.yml up --detach
```

## Backup tools
```bash
# gitmostwantedcom-gmw_db-1 - docker image tag for the db instance
# gitmostwantedcom_default - the network of the db docker instance
[sudo] docker run --rm --link gitmostwantedcom-gmw_db-1:db --network=gitmostwantedcom_default -p 8081:8080 adminer
```

## Contribution
- Fork this repo.
- Modify the source code and create a new Pull Request.
- Please follow [these code standards](https://github.com/amontalenti/elements-of-python-style).
