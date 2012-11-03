
How to import new data
======================


Download latest planet
----------------------

For example here: http://ftp5.gwdg.de/pub/misc/openstreetmap/planet.openstreetmap.org/pbf/


Convert planet to o5m
---------------------

(using http://wiki.openstreetmap.org/wiki/Osmconvert )

::

  bzcat planet-latest.osm.bz2 | ./osmconvert - -o=planet-latest.o5m

or

:: 

  ./osmconvert planet-latest.osm.pbf -o=planet-latest.o5m


Filtering
---------

Now filter all nodes and relations with place_of_worship from the planet using
http://wiki.openstreetmap.org/wiki/Osmfilter

::

  ./osmfilter planet-latest.o5m --keep="amenity=place_of_worship" --drop-author -o=planet-latest-pow.osm


Get only the nodes from the planet (improves speed of update_refs a lot)

::

  ./osmfilter planet-latest.o5m --drop-ways --drop-relations --drop-author -o=planet-latest-nodes.osm


Importing
---------

::

  # activate virtualenv
  workon kr
  cd ~/kirchenreich
  # run shell
  ./manage.py shell

::

  # do stuff
  import krprj.osm.tasks as t
  t.add_churches("/srv/spielwiese/planet-latest-pow.osm")
  t.update_refs("/srv/spielwiese/planet-latest-nodes.osm")
