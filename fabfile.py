from fabric import task


@task
def deploy(conn):
    with conn.cd('~/iati-datastore'):
        # pull latest copy of code in version control
        conn.run('git pull origin master')
        # start the virtual environment
        conn.run('source pyenv/bin/activate')
        # install dependencies
        conn.run('pip install -r requirements.txt')
        # run database migrations
        conn.run('alembic upgrade head')
        # build the docs
        conn.run('iati build-docs')
        # stop everything
        conn.run('systemctl stop iati-datastore')
        conn.run('systemctl stop iati-datastore-queue')
        # start everything again
        conn.run('systemctl start iati-datastore')
        conn.run('systemctl start iati-datastore-queue')
