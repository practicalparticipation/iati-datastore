#!/bin/bash

set -e

# Locale
echo "en_GB.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen

# Ubuntu Packages
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-virtualenv python3-pip postgresql-12 libpq-dev redis-server gcc make libxml2-dev libxslt1-dev libevent-dev python3-dev

# NPM
curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs

# VE
cd /vagrant
virtualenv .ve -p python3
source .ve/bin/activate;
# pip install can fail if .ve already exists, and we don't want errors to stop building totally. So always pass.
pip3 install -r requirements_dev.txt  || true

# Database
su --login -c "psql -c \"CREATE USER app WITH PASSWORD 'password' CREATEDB;\"" postgres
su --login -c "psql -c \"CREATE DATABASE app WITH OWNER app ENCODING 'UTF8'  LC_COLLATE='en_GB.UTF-8' LC_CTYPE='en_GB.UTF-8'  TEMPLATE=template0 ;\"" postgres

su --login -c "psql -c \"CREATE USER test WITH PASSWORD 'password' CREATEDB;\"" postgres
su --login -c "psql -c \"CREATE DATABASE test WITH OWNER test ENCODING 'UTF8'  LC_COLLATE='en_GB.UTF-8' LC_CTYPE='en_GB.UTF-8'  TEMPLATE=template0 ;\"" postgres

# Shell commands
echo "alias db='psql -U  app app  -hlocalhost'" >> /home/vagrant/.bashrc
echo "localhost:5432:app:app:password" > /home/vagrant/.pgpass
chown vagrant:vagrant /home/vagrant/.pgpass
chmod 0600 /home/vagrant/.pgpass

# Env vars
echo "export IATI_DATASTORE_DATABASE_URL=postgresql://app:password@localhost/app" >> /home/vagrant/.bashrc
echo "export NUXT_TELEMETRY_DISABLED=1" >> /home/vagrant/.bashrc
echo "export TEST_SQLALCHEMY_DATABASE_URI=postgresql://test:password@localhost/test" >> /home/vagrant/.bashrc

# Shell setup
echo "cd /vagrant" >> /home/vagrant/.bashrc
echo "source .ve/bin/activate" >> /home/vagrant/.bashrc
