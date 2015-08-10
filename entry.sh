#!/usr/bin/env bash

set -ex

# alias docker links variables

# COUCHDB SERVICE
export COUCHDB_NAME="${COUCHDB_ENV_COUCHDB_DATABASE}"
export COUCHDB_USER="${COUCHDB_ENV_COUCHDB_USER}"
export COUCHDB_PASS="${COUCHDB_ENV_COUCHDB_PASS}"
export COUCHDB_URI="${COUCHDB_URI-http://${COUCHDB_PORT_5984_TCP_ADDR}:${COUCHDB_PORT_5984_TCP_PORT}}"

[ ! -f "/var/lib/nsd/sync.sequence" ] && touch /var/lib/nsd/sync.sequence

echo "Exec'ing $@"
exec "$@"
