#! /bin/sh

# drop completely the db (with the triggers, sequences, etc.)
sudo -u postgres dropdb shelter
sudo -u postgres createdb shelter --no-password
echo "ALTER USER pgsqluser WITH ENCRYPTED PASSWORD 'pgsqlpwd';" | sudo -u postgres psql
echo "GRANT ALL PRIVILEGES ON DATABASE shelter TO pgsqluser;" | sudo -u postgres psql
