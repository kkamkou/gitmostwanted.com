FROM python:3.4

RUN groupadd -r gitmostwanted \
  && useradd -r -g gitmostwanted gitmostwanted \
  && mkdir /opt/gitmostwanted

WORKDIR /opt/gitmostwanted

VOLUME ["/opt/gitmostwanted"]

ADD requirements.txt ./

ENV PYTHONPATH /opt

RUN pip install -U pip \
  && pip install git+https://github.com/jcgregorio/httplib2 \
  && pip install -r requirements.txt
