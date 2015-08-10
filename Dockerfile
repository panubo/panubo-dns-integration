FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN groupadd -g 108 nsd && \
  apt-get update && \
  apt-get -y install nsd openssl && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY entry.sh /
ENTRYPOINT ["/entry.sh"]

COPY bind_sync.py /usr/src/app/

USER nsd
CMD ["./bind_sync.py","--zone-dir","/var/lib/nsd/zones","--sequence-file","/var/lib/nsd/sync.sequence"]
