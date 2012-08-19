from django.views.generic.base import TemplateView


class WorshipMapView(TemplateView):
    """The index view of kirchenreich.org which shows the map with places of
    worship."""

    template_name = "worshipmap.html"
