[![wercker status](https://app.wercker.com/status/399c14de0d935628b87623cc0d46ad34/s/master "wercker status")](https://app.wercker.com/project/byKey/399c14de0d935628b87623cc0d46ad34)
[![Code Climate](https://codeclimate.com/github/kkamkou/gitmostwanted.com/badges/gpa.svg)](https://codeclimate.com/github/kkamkou/gitmostwanted.com)
[![Coverage Status](https://coveralls.io/repos/github/kkamkou/gitmostwanted.com/badge.svg?branch=HEAD)](https://coveralls.io/github/kkamkou/gitmostwanted.com?branch=HEAD)

# gitmostwanted
Advanced explore of github.com. The main goal is to highlight the most interesting repositories and exclude others. You can find some concepts in the [Wiki](https://github.com/kkamkou/gitmostwanted.com/wiki).

## Donation
If you would like to help the project, please consider these topics:
- GMW uses [Google BigQuery](https://cloud.google.com/bigquery/pricing) and the service is pretty expensive.
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
The first time [it'll fail](https://github.com/docker/compose/issues/374)

```bash
cp instance.cfg.distr instance.cfg
[sudo] docker-compose up -d
# open http://127.0.0.1:5000/ in your browser
```

## Contribution
- Fork this repo
- Modify the source code and create a Pull Request
- Please, follow [these code standards](https://github.com/amontalenti/elements-of-python-style)

## License
The MIT License (MIT)

Copyright (c) 2015-2017 Kanstantsin Kamkou <2ka.by>
