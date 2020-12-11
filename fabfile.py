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
        # restart nginx
        conn.run('systemctl restart nginx')
