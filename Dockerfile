## MySQL 5.6 with Percona Xtrabackup

## Pull the mysql:5.6 image
FROM mysql:8.0

# Add a database
ENV MYSQL_DATABASE company

# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./scripts/sql/ /docker-entrypoint-initdb.d/
