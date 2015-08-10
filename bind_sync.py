#!/usr/bin/env python

import os
import ssl
import subprocess
import click
from couchdbkit import Server
from couchdbkit.changes import ChangesStream
from couchdbkit.resource import CouchdbResource
from restkit import BasicAuth


def exit_with_error(msg):
    click.secho("Error: %s" % msg)
    exit(128)


def sequence_read(sequence_file):
    with open(sequence_file, 'r') as f:
        sequence = f.read()
    if sequence == '':
        return 0
    else:
        return int(sequence)


def sequence_write(sequence_file, sequence):
    with open(sequence_file, 'w') as f:
        f.write(str(sequence))


def zone_update(name, data, zone_dir):
    """ Write out zone file and reload bind """

    zone_file = os.path.join(zone_dir, "%s.zone" % name)

    if os.path.isfile(zone_file):
        created = False
    else:
        created = True

    with open("%s.tmp" % zone_file, 'w+') as f:
        f.write(data)
    os.rename("%s.tmp" % zone_file, zone_file)

    if created:
        cmd = ['/usr/sbin/nsd-control', 'addzone', name, 'zone']
        try:
            subprocess.check_call(cmd, cwd=zone_dir, shell=False, env=os.environ.copy())
        except subprocess.CalledProcessError as e:
            raise Exception("Error running '%s'. Return %s" % (cmd, e.returncode))
    else:
        cmd = ['/usr/sbin/nsd-control', 'reload', name]
        try:
            subprocess.check_call(cmd, cwd=zone_dir, shell=False, env=os.environ.copy())
        except subprocess.CalledProcessError as e:
            raise Exception("Error running '%s'. Return %s" % (cmd, e.returncode))


def zone_delete(name, zone_dir):
    zone_file = os.path.join(zone_dir, "%s.zone" % name)
    cmd = ['/usr/sbin/nsd-control', 'delzone', name]
    try:
        subprocess.check_call(cmd, cwd=zone_dir, shell=False, env=os.environ.copy())
    except subprocess.CalledProcessError as e:
        raise Exception("Error running '%s'. Return %s" % (cmd, e.returncode))
    os.remove(zone_file)


@click.command()
@click.option('--db-name', help='CouchDB Name', required=True, envvar='COUCHDB_NAME')
@click.option('--db-user', help='CouchDB User', required=True, envvar='COUCHDB_USER')
@click.option('--db-pass', help='CouchDB Password', required=True, envvar='COUCHDB_PASS')
@click.option('--db-host', help='CouchDB HOST URI', required=True, envvar='COUCHDB_URI')
@click.option('--ca_certs', help='TLS CA Cert', envvar='TLS_CACERT')
@click.option('--certfile', help='TLS Client Cert', envvar='TLS_CLIENT_CERT')
@click.option('--keyfile', help='TLS Client Key', envvar='TLS_CLIENT_KEY')
@click.option('--sequence-file', help='Sequence File', default='/var/tmp/bind_sync.sequence')
@click.option('--zone-dir', help='Zone File Directory', default='/var/named/masters/')
def main(db_name, db_user, db_pass, db_host, sequence_file, zone_dir, **tls_args):
    # Starting Sequence for change stream
    sequence = sequence_read(sequence_file)
    click.echo('Skipping %s changes.' % sequence)
    # CouchDB Connection
    tls_args['cert_reqs'] = ssl.CERT_REQUIRED
    tls_args['ssl_version'] = ssl.PROTOCOL_TLSv1_2
    auth = CouchdbResource(filters=[BasicAuth(db_user, db_pass)], **tls_args)
    server = Server(uri=db_host, resource_instance=auth)
    db = server[db_name]

    with ChangesStream(db, since=sequence, feed='continuous', heartbeat=True) as stream:
        click.echo('Waiting for changes...')

        for change in stream:
            domain = change['id']
            if change.get('deleted', False) is True:
                click.echo("Deleted %s." % domain)
                try:
                    zone_delete(domain, zone_dir)
                except Exception, e:
                    click.echo(e)
            else:
                click.echo("Got change for %s." % domain)
                doc = db.get(docid=domain)
                try:
                    zone_update(domain, doc['data'], zone_dir)
                except Exception, e:
                    click.echo(e)

            sequence_write(sequence_file, change['seq'])   # Keep track of our sync point

if __name__ == '__main__':
    main()
