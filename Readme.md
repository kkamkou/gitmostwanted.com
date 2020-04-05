![CI](https://github.com/kkamkou/gitmostwanted.com/workflows/CI/badge.svg)
[![Code Climate](https://codeclimate.com/github/kkamkou/gitmostwanted.com/badges/gpa.svg)](https://codeclimate.com/github/kkamkou/gitmostwanted.com)
[![Coverage Status](https://coveralls.io/repos/github/kkamkou/gitmostwanted.com/badge.svg?branch=HEAD)](https://coveralls.io/github/kkamkou/gitmostwanted.com?branch=HEAD)

# gitmostwanted
Advanced explore of github.com. Our goal is to highlight the most interesting repositories and exclude others. You can find some concepts in the [Wiki](https://github.com/kkamkou/gitmostwanted.com/wiki).

If you would like to help the project, please consider these topics:
- GMW uses [Google BigQuery](https://cloud.google.com/bigquery/pricing) and the service is **pretty** expensive.
- GMW is located on a private machine and hosted by [ProfitBricks](https://www.profitbricks.de/).

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
Run it two times as the first time **it'll fail** (see: #224).

```bash
cp instance.cfg.distr instance.cfg
[sudo] docker-compose up -d
# open http://127.0.0.1:5000/ in your browser
```

## Contribution
- Fork this repo.
- Modify the source code and create a new Pull Request.
- Please follow [these code standards](https://github.com/amontalenti/elements-of-python-style).
