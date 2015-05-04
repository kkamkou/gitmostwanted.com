[![wercker status](https://app.wercker.com/status/7767a5325ebf378ede0ac3016c992ebc/s "wercker status")](https://app.wercker.com/project/bykey/7767a5325ebf378ede0ac3016c992ebc)
[![Code Health](https://landscape.io/github/Letscodeit/gitmostwanted.com/master/landscape.svg?style=flat-square)](https://landscape.io/github/Letscodeit/gitmostwanted.com/initial-design)
# gitmostwanted
More advanced explore for the github.com

## Run

```bash
# export PYTHONPATH="`pwd`:${PYTHONPATH}"
export GMW_APP_SETTINGS=/path/to/instance.cfg
python gitmostwanted/web.py
```

## Tests

```bash
py.test --pep8 --clearcache --cov gitmostwanted tests/unit
```

## Docker

```bash
[sudo] docker-compose up -d  # The first time it'll fail
```
