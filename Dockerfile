FROM panubo/python-bureaucrat

RUN yum -y install bind bind-utils && \
    # Allow www user to enter the directory
    chmod o+x /var/named && \
    # Cleanup \
    yum clean all

COPY . /srv/git

USER www

RUN source /srv/ve27/bin/activate && cd /srv/git && pip install -r requirements.txt

USER root

COPY rndc.conf /etc/rndc.conf
COPY voltgrid.conf /usr/local/etc/voltgrid.conf

ENTRYPOINT ["/srv/git/entry.sh"]
# Because we've defined the entry point we need to redefine the default CMD
CMD ["/usr/local/bin/voltgrid.py", "/srv/ve27/bin/bureaucrat", "init", "--no-create-pid", "--venv", "/srv/ve27", "--envfile", "/srv/env", "--app", "/srv/git", "--logpath", "-"]
