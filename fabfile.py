#
# Deployment for kirchenreich.org private server
# This is only an example for other installations
#

import os
import time

from fabric.api import task, env, sudo, cd, prefix, run
from fabric.utils import puts
from fabric.colors import yellow, green

env.hosts = ["spatz.madflex.de"]

env.remote_workdir = '/home/%s/virtualenvs/kirchenreich' % env.user
env.virtualenv_dir = env.remote_workdir + '/kr_env'


def in_rwd(path):
    """Complete relative path to full path on remote system"""
    return os.path.join(env.remote_workdir, path)

env.source_dir = in_rwd('kirchenreich/')
env.requirements_file = in_rwd('kirchenreich/requirements.d/prod.txt')


def django_manage(*args):
    """Use the remote django manage.py"""

    with cd(env.source_dir):
        with prefix('source %s' % os.path.join(env.virtualenv_dir, 'bin/activate')):
            args_string = ' '.join(args + ('--settings=krprj.settings.prod',))
            run('python manage.py ' + args_string)


@task
def git_pull():
    """Pull the lastest source from master branch"""

    puts(yellow("Pull master from GitHub"))
    with cd(env.source_dir):
        run('git reset --hard HEAD')
        run('git pull')


@task
def build_virtualenv():
    """Install the dependencies from requirements file and link project
    package into virtualenv"""

    puts(yellow("Install dependencies from requirements.txt"))
    with cd(env.source_dir):
        with prefix('source %s' % in_rwd('bin/activate')):
            sudo('pip install -r %s' % env.requirements_file,
                 user=env.app_user)
            sudo('python setup.py develop', user=env.app_user)


@task
def collectstatic():
    """Collect the statics and link this into the static path"""
    puts(yellow("Collect statics"))
    django_manage('collectstatic', '-l', '--noinput')


@task
def migrate():
    """Run the South migrations"""
    puts(yellow("Run South migrations"))
    django_manage('migrate')


@task
def reload_gunicorn():
    """Reload the gunicorn graceful"""
    puts(yellow("Reload gunicorn graceful"))
    sudo('kill -HUP `cat %s`' % (env.gunicorn_pidpath), user=env.app_user)


@task
def restart_celery():
    """Restart the celery worker"""
    puts(yellow("Restart celery worker"))
    with prefix('source %s' % in_rwd('bin/activate')):
        sudo('supervisorctl restart celery-worker', user=env.app_user)
        time.sleep(1)
        sudo('supervisorctl status', user=env.app_user)


@task
def deploy():
    """Get source and update virtualenv, statics and run South migrations"""
    git_pull()
#    build_virtualenv()
#    collectstatic()
    migrate()
#    reload_gunicorn()
#    restart_celery()
    puts(green("Deployment done!"))
