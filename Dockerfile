FROM python:3.4

RUN mkdir /opt/gitmostwanted
WORKDIR /opt/gitmostwanted

ENV PYTHONPATH $PYTHONPATH:/opt

VOLUME ["/opt/gitmostwanted"]

ADD requirements.txt /opt/gitmostwanted/

RUN pip install -r requirements.txt