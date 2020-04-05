FROM python:latest

RUN groupadd -r gitmostwanted \
  && useradd -r -g gitmostwanted gitmostwanted \
  && mkdir /opt/gitmostwanted

WORKDIR /opt/gitmostwanted

VOLUME ["/opt/gitmostwanted"]

ADD requirements.txt ./

ENV PYTHONPATH /opt/gitmostwanted

RUN pip install -U pip \
  && pip install -r requirements.txt
