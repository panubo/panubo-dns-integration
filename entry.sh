#!/usr/bin/env bash

set -ex

# alias docker links variables

# COUCHDB SERVICE
export COUCHDB_NAME="${COUCHDB_ENV_COUCHDB_DATABASE}"
export COUCHDB_USER="${COUCHDB_ENV_COUCHDB_USER}"
export COUCHDB_PASS="${COUCHDB_ENV_COUCHDB_PASS}"
export COUCHDB_HOST="http://${COUCHDB_PORT_5984_TCP_ADDR}:${COUCHDB_PORT_5984_TCP_PORT}"

# BIND SERVICE
export RNDC_SERVER="$BIND_PORT_953_TCP_ADDR"
export RNDC_PORT="${BIND_PORT_953_TCP_PORT-953}"
export RNDC_KEY="${BIND_ENV_RNDC_KEY-$RNDC_KEY}"

echo "Exec'ing $@"
exec "$@"
