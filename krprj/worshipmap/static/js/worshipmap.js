kr = {'request_id': 0};

kr.session = {};

kr.session.has_zoom = function(){
    return sessionStorage && sessionStorage.kr_zoom;
};

kr.session.has_possition = function(){
    return sessionStorage && sessionStorage.kr_lon && sessionStorage.kr_lat;
};

kr.session.get_possition = function(){
    return new OpenLayers.LonLat(sessionStorage.kr_lon, sessionStorage.kr_lat);
};

kr.session.set_possition = function(possition){
    sessionStorage.kr_lon = possition.lon;
    sessionStorage.kr_lat = possition.lat;
};

kr.session.set_zoom = function(zoom){
    sessionStorage.kr_zoom = zoom;
};

kr.session.get_zoom = function(){
    return sessionStorage.kr_zoom;
};

kr.refresh_markers = function(){
    $("#nav_status").html('<span class="label label-warning">Loading...</span>');
    kr.request_id++;
    xhr = $.getJSON("/api/v1/places/?epsg=3857&in_bbox=" + kr.map.getExtent().toBBOX() + "&request_id=" + kr.request_id, function(response, status, xhr){
        $("#zoom_in_alert").hide();
        if (response.request_id == kr.request_id) {
            kr.markers.clearMarkers();
            for (var i in response.places_of_worship) {
                place = response.places_of_worship[i];

                var icon;
                if (place.religion in kr.marker_icons) {
                    icon = kr.marker_icons[place.religion].clone();
                } else {
                    icon = kr.marker_icons['default'].clone();
                }

                var marker = new OpenLayers.Marker(new OpenLayers.LonLat(place.lon, place.lat), icon);
                marker.place_id = place.id;

                if (place.name === null) {
                    place.name = "unknown";
                }
                if (place.religion === null) {
                    place.religion = "unknown";
                }
                tooltip = OpenLayers.String.format("${name} (${religion})", place);

                $(marker.events.element).tooltip({
                    'title': tooltip
                });

                marker.events.register("click", marker, kr.on_marker_click);

                kr.markers.addMarker(marker);
            }
            $("#nav_status").html('<span class="label label-success">'+ response.places_of_worship_count + ' places</span>');
            var religion = $.map(response.statistics['religion'],
                function(key, value) {
                    return "<li>" + value + ": <b>" + key + "</b></li>";
                }
            );
            $("#stats_ul").html('<li class="nav-header">Statistics</li><li class="active"><a href="#"><b>religion</b></a></li>' + religion.join(""));
        }
    }).error(function(){
        if (xhr.status == 422) {
            $("#nav_status").html('<span class="label label-important"><strong>Please zoom in.</strong> There are to many places of worship to display.</span>');
            kr.markers.clearMarkers();
        }
    });
};

kr.run_geolocate = function(){
    kr.map_geolocate.activate();
    kr.map_geolocate.getCurrentLocation();
};

kr.on_marker_click = function(e){
   window.location = "/" + e.object.place_id;
};

kr.buildMap = function(target_div, center, zoom, use_session){
    if (use_session) {
        if (kr.session.has_possition()) {
            center = kr.session.get_possition();
        }
        if (kr.session.has_zoom()) {
            zoom = kr.session.get_zoom();
        }
    }

    var osm_layer = new OpenLayers.Layer.OSM("OSM Map Layer");
    kr.map = new OpenLayers.Map({
        div: target_div,
        layers: [osm_layer],
        center: center,
        zoom: zoom
    });

    // Base marker layer
    kr.markers = new OpenLayers.Layer.Markers("Markers");
    kr.map.addLayer(kr.markers);

    kr.marker_icons = {
        'default': [STATIC_URL + 'icons/pin.png', new OpenLayers.Size(15, 24)],
        'christian': [STATIC_URL + 'icons/christianity_church.png', new OpenLayers.Size(24, 25)],
        'islam': [STATIC_URL + 'icons/islam.png', new OpenLayers.Size(25, 24)],
        'muslim': [STATIC_URL + 'icons/islam.png', new OpenLayers.Size(25, 24)],
        'hindu': [STATIC_URL + 'icons/hindu.png', new OpenLayers.Size(24, 24)],
        'budddhist': [STATIC_URL + 'icons/buddhist.png', new OpenLayers.Size(28, 22)]
    };

    for (var name in kr.marker_icons) {
        var url = kr.marker_icons[name][0];
        var size = kr.marker_icons[name][1];
        kr.marker_icons[name] = new OpenLayers.Icon(
            url,
            size,
            new OpenLayers.Pixel(-(size.w/2), -size.h)
        );
    }

    // Geolocation
    kr.map_geolocate = new OpenLayers.Control.Geolocate({
        bind: true
    });
    kr.map_geolocate.events.register("locationupdated", kr.map_geolocate, function(e) {
        kr.map.zoomTo(13);
    });

    kr.map.addControl(kr.map_geolocate);

    kr.map.events.register("moveend", map, function(e){
        kr.refresh_markers();
        if (use_session && sessionStorage) {
            kr.session.set_possition(e.object.getCenter());
            kr.session.set_zoom(e.object.getZoom());
        }
    });

    if (use_session && (kr.session.has_possition() || kr.session.has_zoom())) {
        kr.refresh_markers();
    }

};
