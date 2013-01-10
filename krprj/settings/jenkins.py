from .default import *

INSTALLED_APPS.append("django_jenkins")

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
)
