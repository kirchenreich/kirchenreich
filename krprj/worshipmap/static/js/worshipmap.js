kr = {'request_id': 0};

kr.buildMap = function(target_div, center, zoom, use_geolocate){
    var osm_layer = new OpenLayers.Layer.OSM("OSM Map Layer");
    kr.map = new OpenLayers.Map({
        div: target_div,
        layers: [osm_layer],
        center: center,
        zoom: zoom
    });

    // Base marker layer
    kr.markers = new OpenLayers.Layer.Markers( "Markers" );
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
    if (use_geolocate) {
        var geolocate = new OpenLayers.Control.Geolocate({
            bind: true
        });
        geolocate.events.register("locationupdated", geolocate, function(e) {
            kr.map.zoomTo(13);
        });

        kr.map.addControl(geolocate);
        geolocate.activate();
    }

    kr.on_marker_click = function(e){
       window.location = "/" + e.object.place_id;
    };

    kr.refresh_markers = function(){
        $("#nav_status").html('<span class="label label-warning">Loading...</span>');
        kr.request_id++;
        xhr = $.getJSON("/api/v1/places/?epsg=900913&in_bbox=" + kr.map.getExtent().toBBOX() + "&request_id=" + kr.request_id, function(response, status, xhr){
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
            }
        }).error(function(){
            if (xhr.status == 422) {
                $("#nav_status").html('<span class="label label-important"><strong>Please zoom in.</strong> There are to many places of worship to display.</span>');
                kr.markers.clearMarkers();
            }
        });
    };

    kr.map.events.register("moveend", map, kr.refresh_markers);
};