#!/usr/bin/env bash
set -e

set -a
source .env
set +a

# remove supa param if present
CLEAN_DB_URL=$(echo "$POSTGRES_URL" | sed 's/[?&]supa=[^&]*//')

psql "$CLEAN_DB_URL" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
alembic -c app/db/alembic.ini upgrade head