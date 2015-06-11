FROM debian:jessie

WORKDIR /app

EXPOSE 8000
CMD ["./bin/run-docker.sh"]
ENV LC_ALL=C.UTF-8  LANG=C.UTF-8

RUN adduser --uid 1000 --disabled-password --gecos '' --no-create-home webdev

COPY ./bin/peep.py /app/bin/peep.py
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update &&\
    apt-get install -y --no-install-recommends python3 python3.4 python3-setuptools python3-pkg-resources python3-pip build-essential python3.4-dev libpq-dev gettext libjpeg62-turbo libjpeg62-turbo-dev postgresql-client sharutils &&\
    ln -s /usr/bin/python3 /usr/bin/python && \
    ln -s /usr/bin/pip3 /usr/bin/pip && \
    pip install --upgrade pip==6.0.0 && \
    ./bin/peep.py install --no-cache-dir -r requirements.txt && \
    apt-get purge -y build-essential libpq-dev libjpeg62-turbo-dev python3.4-dev python3-pip build-essential && \
    apt-get autoremove -y && \
    rm -rf /usr/share/doc/* && \
    rm -rf /var/lib/apt/lists/*

ADD https://github.com/mozilla/masterfirefoxos-l10n/archive/master.tar.gz /tmp/locale.tar.gz
RUN mkdir -p /app/locale && tar zxf /tmp/locale.tar.gz -C /app/locale --strip-components 1
COPY . /app

RUN chown webdev.webdev -R .
USER webdev
