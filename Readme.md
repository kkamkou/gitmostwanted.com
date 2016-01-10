[![wercker status](https://app.wercker.com/status/7767a5325ebf378ede0ac3016c992ebc/s/master "wercker status")](https://app.wercker.com/project/bykey/7767a5325ebf378ede0ac3016c992ebc)
[![Code Climate](https://codeclimate.com/github/kkamkou/gitmostwanted.com/badges/gpa.svg)](https://codeclimate.com/github/kkamkou/gitmostwanted.com)
[![Coverage Status](https://coveralls.io/repos/kkamkou/gitmostwanted.com/badge.svg?branch=HEAD&service=github)](https://coveralls.io/github/kkamkou/gitmostwanted.com?branch=HEAD)

# gitmostwanted
Advanced explorer of github.com. The main goal is to highlight the most interesting repositories and exclude others. You can find some concepts in the [Wiki](https://github.com/kkamkou/gitmostwanted.com/wiki).

## Donation
If you would like to help the project, please consider these topics:
- GMW uses [Google BigQuery](https://cloud.google.com/bigquery/pricing) and the service is pretty expensive.
- GMW is located on a private machine and hosted by [ProfitBricks](https://www.profitbricks.de/).

## Run (Python3)

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
The first time [it'll fail](https://github.com/docker/compose/issues/374)

```bash
[sudo] docker-compose up -d
```

## Contribution
- Fork this repo
- Modify the source code and create a Pull Request
- Please, follow [these code standards](https://github.com/amontalenti/elements-of-python-style)

## License
The MIT License (MIT)
Copyright (c) 2015-2016 Kanstantsin Kamkou <2ka.by>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
