DATE=$(date +%F_%H%M)
PGUSER=${POSTGRES_USER}
PGDB=${POSTGRES_DB}
PGPASSWORD=${POSTGRES_PASSWORD}
HOST=${PGHOST:-postgres}
mkdir -p /backups
PGPASSWORD=$PGPASSWORD pg_dump -h $HOST -U $PGUSER -F c -b -v -f /backups/$PGDB-$DATE.dump $PGDB

