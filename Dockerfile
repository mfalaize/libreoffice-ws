FROM debian:stretch
MAINTAINER Maxime Falaize <maxime.falaize@gmail.com>

RUN apt-get update && apt-get install -y libreoffice-calc libreoffice-l10n-fr python3-uno python3-setuptools ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /

RUN chmod +x /etc/init.d/soffice && update-rc.d soffice defaults \
    && chmod +x /docker_entrypoint.sh \
    && easy_install3 pip && pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["/docker_entrypoint.sh"]