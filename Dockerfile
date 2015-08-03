FROM panubo/python-bureaucrat

COPY . /srv/git

RUN yum -y install bind bind-utils && yum clean all

USER www

RUN source /srv/ve27/bin/activate && cd /srv/git && pip install -r requirements.txt

USER root

ENTRYPOINT ["/srv/git/entry.sh"]
# Because we've defined the entry point we need to redefine the default CMD
CMD ["/usr/local/bin/voltgrid.py", "/srv/ve27/bin/bureaucrat", "init", "--no-create-pid", "--venv", "/srv/ve27", "--envfile", "/srv/env", "--app", "/srv/git", "--logpath", "-"]
