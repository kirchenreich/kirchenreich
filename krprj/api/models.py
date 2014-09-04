from django.db import models


class Changes(models.Model):
    """ in this table all changes from daily OSM updates are saved until
        processed.
    """

    data_xml = models.TextField()
    # modify, delete, insert
    verb = models.CharField(max_length=10, blank=True, null=True)

    timestamp = models.DateTimeField()

    last_update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%d [%s] (%s)" % (self.id, self.verb or '',
                                 len(self.data_xml))
