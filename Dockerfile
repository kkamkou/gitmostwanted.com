FROM python:3.4
RUN mkdir /opt/gitmostwanted
VOLUME ["/opt/gitmostwanted"]
WORKDIR /opt/gitmostwanted
ADD requirements.txt /opt/gitmostwanted/
RUN pip install -r requirements.txt