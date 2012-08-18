kirchenreich
============

This is a Django Dash 2012 project.

Install How-to
--------------

* clone github repo

::

  # create virtualenv
  virtualenv env_kr
  # activate
  . env_kr/bin/activate
  # install requirements
  pip install -r requirements.d/dev-standalone.txt


 * set in krprj/settings/local.py::

  # SECRET_KEY - see http://www.miniwebtool.com/django-secret-key-generator/
  # DATABASES - see settings.py for template without user/pw


Run locally
-----------

* you need postgresql with postgis support!
* download world to world/data/::

  mkdir world/data
  cd world/data
  wget http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip
  unzip TM_WORLD_BORDERS-0.3.zip
  rm TM_WORLD_BORDERS-0.3.zip

* import worlddata (in django shell)::

  from world import load
  load.run()

* ./manage.py runserver
